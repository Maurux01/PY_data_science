# python-data-analysis-portfolio

End-to-end portfolio: **PostgreSQL Serverless (Neon) → Web Scraping → Analysis → Dashboard**. Toy data from a Tech Store, reproducible pipeline, no secrets in git.

## Projects

| # | Folder | What it does | Input → Output |
|---|---------|----------|------------------|
| 01 | `Projects/01_sales_analysis/` | SQL migration + statistical EDA in Jupyter (`analysis.ipynb`) | `Database/schema.sql` + `seeds.sql` → `ventas` table (6 rows) → 4-panel matplotlib/seaborn figure |
| 02 | `Projects/02_web_scraping_/` | Playwright scraper for `books.toscrape.com` (`books_scrapper.py`) | 3 pages × 20 books → `scraped_books` table (~60 rows) |
| 03 | `Projects/03_streamlit_dashboard/` | Streamlit + Plotly dashboard (`dashboard.py`) | `ventas` + `scraped_books` → KPIs, filters, Pareto, histogram, market boxplot |

Current results: **CV 124.8%** (high dispersion), **Top Pareto: Laptop Gamer ($1,500.00)**, `ventas=6`, `scraped_books=60`.

See each project's `README.md` for details.

## Structure

```
PY_data_science/
├── .env                      # LOCAL, never committed (DATABASE_URL)
├── .gitignore                # ignores .env, secrets, venv, data, csv/db
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
├── Assets/                   # screenshots and previews
├── docs/                     # portfolio landing page
└── LICENSE                   # MIT
```

## Quickstart

```bash
# 1. Clone + environment
git clone https://github.com/Maurux01/PY_data_science.git
cd PY_data_science
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install pandas sqlalchemy psycopg[binary] python-dotenv matplotlib seaborn scipy numpy jupyter streamlit plotly playwright
playwright install chromium

# 2. Local credential (DO NOT commit)
# Create .env in the repo root with:
# DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Pipeline
jupyter notebook Projects/01_sales_analysis/analysis.ipynb  # creates ventas table + EDA
python Projects/02_web_scraping_/books_scrapper.py           # creates scraped_books table
streamlit run Projects/03_streamlit_dashboard/dashboard.py   # dashboard
```

## Stack

`Python · PostgreSQL (Neon) · SQLAlchemy + psycopg v3 · pandas / numpy / scipy · matplotlib / seaborn · Playwright · Streamlit / Plotly · dotenv`

## Security

- Credential only via `os.getenv("DATABASE_URL")`, never hardcoded.
- `.env` and `.streamlit/secrets.toml` in `.gitignore`, verified out of history (`git log -- .env` empty).
- Dashboard enforces `sslmode=require` and hides SQL exception details (they may contain `user:password@host`).
- In production use Streamlit Cloud Secrets, don't upload `.env`. Clear notebook outputs before `git add` to avoid leaking local paths.

## Preview

Screenshots in `Assets/` (`result_sales_analysis.png`, `result_web_scrapping.png`, `result_streamlit_dashboard.png`).

## License

MIT — see `LICENSE`.

## Credits

Ideas with help from Qwen, everything else built by [maurux01](https://github.com/Maurux01).
