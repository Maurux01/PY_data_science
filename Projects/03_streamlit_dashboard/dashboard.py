# 03_streamlit_dashboard_/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path
import plotly.express as px

# ------------------------------------------------------------------
# 1. PAGE CONFIG AND NEON CONNECTION
# ------------------------------------------------------------------
st.set_page_config(page_title="Tech Store Dashboard | Maurux01", layout="wide")
st.title("📊 Sales & Market Analysis - Tech Store")
st.markdown("---")

# Hardened path to .env (goes 2 levels up from this script)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)
db_url_raw = os.getenv("DATABASE_URL")
if not db_url_raw:
    st.error("❌ Configuration error: DATABASE_URL is not set.")
    st.stop()

db_url = db_url_raw.replace("postgresql://", "postgresql+psycopg://")

# Enforce SSL to avoid unencrypted connections to Neon
if "sslmode=" not in db_url:
    db_url += ("&" if "?" in db_url else "?") + "sslmode=require"

@st.cache_data(ttl=300)  # 5-min cache to avoid hammering Neon
def load_data():
    engine = create_engine(db_url)
    ventas = pd.read_sql("SELECT * FROM ventas", engine)
    scraped = pd.read_sql("SELECT * FROM scraped_books", engine)
    return ventas, scraped

try:
    df_ventas, df_scraped = load_data()
except Exception as e:
    # Don't expose details in the UI: they may contain user:password@host
    st.error("❌ Could not connect to the database. Please try again later.")
    print(f"[DB ERROR] {type(e).__name__}")  # server log only, no credentials
    st.stop()

# ------------------------------------------------------------------
# 2. SIDEBAR WITH DYNAMIC FILTERS
# ------------------------------------------------------------------
st.sidebar.header(" Filters")
categorias = sorted(df_ventas['categoria'].unique())
selected_cat = st.sidebar.multiselect("Category", options=categorias, default=categorias)

rango_precio = st.sidebar.slider(
    "Price Range ($)",
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
# 3. MAIN KPIS
# ------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df_filtered['monto'].sum():,.2f}")
col2.metric("Transactions", len(df_filtered))
col3.metric("Average Ticket", f"${df_filtered['monto'].mean():,.2f}")
col4.metric("Top Products", df_filtered['producto'].nunique())

st.markdown("---")

# ------------------------------------------------------------------
# 4. INTERACTIVE CHARTS (PLOTLY)
# ------------------------------------------------------------------
tab1, tab2 = st.tabs(["📈 Internal Sales", " Market Comparison"])

with tab1:
    c1, c2 = st.columns(2)

    # Interactive Pareto
    pareto = df_filtered.sort_values('monto', ascending=False).head(10)
    fig_pareto = px.bar(pareto, x='producto', y='monto', title="Top 10 Products (Pareto)", color='monto')
    c1.plotly_chart(fig_pareto, use_container_width=True)

    # Price distribution
    fig_hist = px.histogram(df_filtered, x='monto', nbins=20, title="Amount Distribution", color_discrete_sequence=['#2ecc71'])
    c2.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    if not df_scraped.empty:
        st.info(f"Market data: {len(df_scraped)} scraped products")
        fig_comp = px.box(df_scraped, x='categoria', y='monto', title="Market Prices by Category", color='categoria')
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.warning("⚠️ No scraped data yet. Run books_scraper.py first.")

# ------------------------------------------------------------------
# 5. DETAIL TABLE
# ------------------------------------------------------------------
st.subheader("📋 Filtered Transaction Details")
st.dataframe(df_filtered[['fecha', 'producto', 'categoria', 'monto', 'cantidad']], hide_index=True, use_container_width=True)
