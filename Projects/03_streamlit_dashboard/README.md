# 03 — Streamlit Dashboard | Tech Store

Interactive dashboard built with **Streamlit + Plotly** combining internal sales (`ventas`) with scraped market data (`scraped_books`) from **Neon**.

## What `dashboard.py` does

1. **Secure Neon connection:**
   - `.env` resolved 2 levels up (`03_streamlit_dashboard/` → root).
   - Validates `DATABASE_URL`: if missing, shows a generic error + `st.stop()` (no `AttributeError`).
   - Converts to `postgresql+psycopg://` and **enforces `sslmode=require`** when the URL lacks it.
   - Connection errors render a generic UI message (`Could not connect...`) with only `type(e).__name__` in the server log — never exposes `user:password@host`.

2. **Data loading (`@st.cache_data(ttl=300)`):**
   ```python
   ventas = pd.read_sql("SELECT * FROM ventas", engine)
   scraped = pd.read_sql("SELECT * FROM scraped_books", engine)
   ```
   5-minute cache to avoid hammering Neon.

3. **Sidebar with dynamic filters:**
   - `categoria` `multiselect` (default: all).
   - Price-range `slider` over `monto` (min → max).

4. **Main KPIs:**
   - Total Sales (`sum(monto)`), Transactions (`len`), Average Ticket (`mean(monto)`), Top Products (`nunique(producto)`).

5. **Plotly charts (2 tabs):**
   - **Internal Sales:** Top-10 Pareto (`px.bar`, color=`monto`) + monto histogram (`px.histogram`, 20 bins).
   - **Market Comparison:** `px.box(scraped, x='categoria', y='monto', color='categoria')`, or a warning when the table is empty.

6. **Detail table:**
   - `st.dataframe(df_filtered[['fecha','producto','categoria','monto','cantidad']])`.

## Structure

```
03_streamlit_dashboard/
├── dashboard.py  # Complete Streamlit app
└── README.md
```

## How to reproduce

```bash
# 1. Environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install streamlit pandas sqlalchemy psycopg[binary] python-dotenv plotly

# 2. Credential (DO NOT commit)
# Create PY_data_science/.env with:
# DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Run (from the root)
streamlit run Projects/03_streamlit_dashboard/dashboard.py
```

For **Streamlit Community Cloud**: don't upload `.env`; paste the URL under `App → Settings → Secrets` as `DATABASE_URL`.

## Security

- `.env` in `.gitignore`, no secrets in code or history.
- Mandatory `sslmode=require`.
- No `st.error(f"...{e}")`: SQLAlchemy errors may embed the URL with password.
- Public app by default: anyone with the URL sees `ventas`. For real data use private deployment or authentication.

## Key dependencies

`streamlit`, `pandas`, `sqlalchemy`, `psycopg[binary]`, `python-dotenv`, `plotly`
