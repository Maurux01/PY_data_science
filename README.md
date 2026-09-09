# python-data-analysis-portfolio


Portafolio end-to-end: **PostgreSQL Serverless (Neon) → Web Scraping → Análisis → Dashboard**. Datos de juguete de una Tienda Tech, pipeline reproducible y sin secretos en git.

## Proyectos

| # | Carpeta | Qué hace | Entrada → Salida |
|---|---------|----------|------------------|
| 01 | `Projects/01_sales_analysis/` | Migración SQL + EDA estadístico en Jupyter (`analysis.ipynb`) | `Database/schema.sql` + `seeds.sql` → tabla `ventas` (6 registros) → 4 paneles matplotlib/seaborn |
| 02 | `Projects/02_web_scraping_/` | Scraper Playwright de `books.toscrape.com` (`books_scrapper.py`) | 3 páginas × 20 libros → tabla `scraped_books` (~60 registros) |
| 03 | `Projects/03_streamlit_dashboard/` | Dashboard Streamlit + Plotly (`dashboard.py`) | `ventas` + `scraped_books` → KPIs, filtros, Pareto, histograma, boxplot mercado |

Resultados actuales: **CV 124.8%** (alta dispersión), **Top Pareto: Laptop Gamer ($1,500.00)**, `ventas=6`, `scraped_books=60`.

Ver detalle en cada `README.md` de proyecto.

## Estructura

```
PY_data_science/
├── .env                      # LOCAL, nunca se sube (DATABASE_URL)
├── .gitignore                # ignora .env, secrets, venv, data, csv/db
├── Projects/
│   ├── 01_sales_analysis/
│   │   ├── analysis.ipynb
│   │   ├── Database/schema.sql
│   │   ├── Database/seeds.sql
│   │   └── README.md
│   ├── 02_web_scraping_/
│   │   ├── books_scrapper.py
│   │   └── README.md
│   └── 03_streamlit_dashboard/
│       ├── dashboard.py
│       └── README.md
├── Assets/                   # capturas y previews
├── docs/                     # landing mínima
└── LICENSE                   # MIT
```

## Quickstart

```bash
# 1. Clonar + entorno
git clone https://github.com/Maurux01/PY_data_science.git
cd PY_data_science
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install pandas sqlalchemy psycopg[binary] python-dotenv matplotlib seaborn scipy numpy jupyter streamlit plotly playwright
playwright install chromium

# 2. Credencial local (NO commitear)
# Crear .env en la raíz con:
# DATABASE_URL=postgresql://usuario:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Pipeline
jupyter notebook Projects/01_sales_analysis/analysis.ipynb  # crea tabla ventas + EDA
python Projects/02_web_scraping_/books_scrapper.py           # crea tabla scraped_books
streamlit run Projects/03_streamlit_dashboard/dashboard.py   # dashboard
```

## Stack

`Python · PostgreSQL (Neon) · SQLAlchemy + psycopg v3 · pandas / numpy / scipy · matplotlib / seaborn · Playwright · Streamlit / Plotly · dotenv`

## Seguridad

- Credencial solo vía `os.getenv("DATABASE_URL")`, sin hardcodear.
- `.env` y `.streamlit/secrets.toml` en `.gitignore`, verificados fuera del historial (`git log -- .env` vacío).
- Dashboard fuerza `sslmode=require` y oculta el detalle de excepciones SQL (puede contener `user:password@host`).
- En producción usa Secrets de Streamlit Cloud, no subas `.env`. Limpia outputs del notebook antes de `git add` para no filtrar rutas locales.

## Preview

Capturas en `Assets/` (`result_sales_analysis.png`, `result_web_scrapping.png`, `result_streamlit_dashboard.png`).

## Licencia

MIT — ver `LICENSE`.

## Créditos

Ideas con ayuda de Qwen, el resto del desarrollo por [maurux01](https://github.com/Maurux01).
