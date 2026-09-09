# 03 — Streamlit Dashboard | Tienda Tech

Dashboard interactivo en **Streamlit + Plotly** que combina ventas internas (`ventas`) con datos de mercado scrapeados (`scraped_books`) desde **Neon**.

## Qué hace `dashboard.py`

1. **Conexión segura a Neon:**
   - `.env` resuelto subiendo 2 niveles (`03_streamlit_dashboard/` → raíz).
   - Valida `DATABASE_URL`: si falta, muestra error genérico + `st.stop()` (sin `AttributeError`).
   - Convierte a `postgresql+psycopg://` y **fuerza `sslmode=require`** si la URL no lo trae.
   - Errores de conexión con mensaje genérico en UI (`No se pudo conectar...`) y solo `type(e).__name__` en log servidor — nunca expone `user:password@host`.

2. **Carga de datos (`@st.cache_data(ttl=300)`):**
   ```python
   ventas = pd.read_sql("SELECT * FROM ventas", engine)
   scraped = pd.read_sql("SELECT * FROM scraped_books", engine)
   ```
   Cache de 5 min para no saturar Neon.

3. **Sidebar con filtros dinámicos:**
   - `multiselect` de `categoria` (default: todas).
   - `slider` de rango de precio sobre `monto` (min → max).

4. **KPIs principales:**
   - Total Ventas (`sum(monto)`), Transacciones (`len`), Ticket Promedio (`mean(monto)`), Productos Top (`nunique(producto)`).

5. **Gráficos Plotly (2 tabs):**
   - **Ventas Internas:** Top 10 Pareto (`px.bar`, color=`monto`) + histograma de montos (`px.histogram`, 20 bins).
   - **Comparativa Mercado:** `px.box(scraped, x='categoria', y='monto', color='categoria')` o warning si la tabla está vacía.

6. **Tabla detallada:**
   - `st.dataframe(df_filtered[['fecha','producto','categoria','monto','cantidad']])`.

## Estructura

```
03_streamlit_dashboard/
├── dashboard.py  # App Streamlit completa
└── README.md
```

## Cómo reproducir

```bash
# 1. Entorno
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install streamlit pandas sqlalchemy psycopg[binary] python-dotenv plotly

# 2. Credencial (NO subir a git)
# Crear PY_data_science/.env con:
# DATABASE_URL=postgresql://usuario:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Ejecutar (desde la raíz)
streamlit run Projects/03_streamlit_dashboard/dashboard.py
```

Para **Streamlit Community Cloud**: no subas `.env`, pega la URL en `App → Settings → Secrets` como `DATABASE_URL`.

## Seguridad

- `.env` en `.gitignore`, sin secretos en código ni historial.
- `sslmode=require` obligatorio.
- Sin `st.error(f"...{e}")`: los errores de SQLAlchemy pueden contener la URL con password.
- App pública por defecto: cualquiera con la URL ve `ventas`. Para datos reales usa despliegue privado o autenticación.

## Dependencias clave

`streamlit`, `pandas`, `sqlalchemy`, `psycopg[binary]`, `python-dotenv`, `plotly`
