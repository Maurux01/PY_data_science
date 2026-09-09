# 03_streamlit_dashboard_/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path
import plotly.express as px

# ------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y CONEXIÓN A NEON
# ------------------------------------------------------------------
st.set_page_config(page_title="Dashboard Tienda Tech | Maurux01", layout="wide")
st.title("📊 Análisis de Ventas & Mercado - Tienda Tech")
st.markdown("---")

# Ruta blindada al .env (sube 2 niveles desde este script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)
db_url_raw = os.getenv("DATABASE_URL")
if not db_url_raw:
    st.error("❌ Error de configuración: DATABASE_URL no definida.")
    st.stop()

db_url = db_url_raw.replace("postgresql://", "postgresql+psycopg://")

# Forzar SSL para evitar conexiones sin cifrar a Neon
if "sslmode=" not in db_url:
    db_url += ("&" if "?" in db_url else "?") + "sslmode=require"

@st.cache_data(ttl=300)  # Cache por 5 min para no saturar Neon
def load_data():
    engine = create_engine(db_url)
    ventas = pd.read_sql("SELECT * FROM ventas", engine)
    scraped = pd.read_sql("SELECT * FROM scraped_books", engine)
    return ventas, scraped

try:
    df_ventas, df_scraped = load_data()
except Exception as e:
    # No exponer el detalle en la UI: puede contener user:password@host
    st.error("❌ No se pudo conectar a la base de datos. Intenta más tarde.")
    print(f"[DB ERROR] {type(e).__name__}")  # log servidor sin credenciales
    st.stop()

# ------------------------------------------------------------------
# 2. SIDEBAR CON FILTROS DINÁMICOS
# ------------------------------------------------------------------
st.sidebar.header(" Filtros")
categorias = sorted(df_ventas['categoria'].unique())
selected_cat = st.sidebar.multiselect("Categoría", options=categorias, default=categorias)

rango_precio = st.sidebar.slider(
    "Rango de Precio ($)", 
    min_value=float(df_ventas['monto'].min()), 
    max_value=float(df_ventas['monto'].max()), 
    value=(float(df_ventas['monto'].min()), float(df_ventas['monto'].max()))
)

df_filtered = df_ventas[
    (df_ventas['categoria'].isin(selected_cat)) &
    (df_ventas['monto'] >= rango_precio[0]) &
    (df_ventas['monto'] <= rango_precio[1])
]

# ------------------------------------------------------------------
# 3. KPIs PRINCIPALES
# ------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ventas", f"${df_filtered['monto'].sum():,.2f}")
col2.metric("Transacciones", len(df_filtered))
col3.metric("Ticket Promedio", f"${df_filtered['monto'].mean():,.2f}")
col4.metric("Productos Top", df_filtered['producto'].nunique())

st.markdown("---")

# ------------------------------------------------------------------
# 4. GRÁFICOS INTERACTIVOS (PLOTLY)
# ------------------------------------------------------------------
tab1, tab2 = st.tabs(["📈 Ventas Internas", " Comparativa Mercado"])

with tab1:
    c1, c2 = st.columns(2)
    
    # Pareto Interactivo
    pareto = df_filtered.sort_values('monto', ascending=False).head(10)
    fig_pareto = px.bar(pareto, x='producto', y='monto', title="Top 10 Productos (Pareto)", color='monto')
    c1.plotly_chart(fig_pareto, use_container_width=True)
    
    # Distribución de Precios
    fig_hist = px.histogram(df_filtered, x='monto', nbins=20, title="Distribución de Montos", color_discrete_sequence=['#2ecc71'])
    c2.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    if not df_scraped.empty:
        st.info(f"Datos de mercado: {len(df_scraped)} productos scrappeados")
        fig_comp = px.box(df_scraped, x='categoria', y='monto', title="Precios de Mercado por Categoría", color='categoria')
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.warning("⚠️ Aún no hay datos scrappeados. Ejecuta books_scraper.py primero.")

# ------------------------------------------------------------------
# 5. TABLA DETALLADA
# ------------------------------------------------------------------
st.subheader("📋 Detalle de Transacciones Filtradas")
st.dataframe(df_filtered[['fecha', 'producto', 'categoria', 'monto', 'cantidad']], hide_index=True, use_container_width=True)