# 02 — Web Scraping | Books to Scrape → Neon

Ethical scraper built with **Playwright (headless Chromium)** that extracts books from `books.toscrape.com` and loads them into **PostgreSQL Serverless (Neon)** in the `scraped_books` table.

## What `books_scrapper.py` does

1. **Secure Neon connection (hardened path):**
   - Resolves `.env` by going 2 levels up from the script (`Projects/02_web_scraping_/` → `PY_data_science/` root).
   - Fails explicitly if `.env` is missing (`FileNotFoundError`) or `DATABASE_URL` is unset (`EnvironmentError`).
   - Converts `postgresql://` → `postgresql+psycopg://` (psycopg v3).

2. **Scraper (`scrape_books(max_pages=3)`):**
   - Iterates `https://books.toscrape.com/catalogue/page-{i}.html`.
   - For each `article.product_pod` it extracts:
     - `producto`: `h3 > a[title]` (truncated to 80 chars)
     - `monto`: `.price_color` cleaned with `re.sub(r'[^\d.]', '', ...)` → `float`
     - `categoria`: last class of `p.star-rating` (e.g. `Three`, `Five`)
     - `descripcion`: rating `title` or `"N/A"` (150 chars)
     - `cantidad`: `1`, `fecha`: `2024-01-{i:02d}`
   - `page.goto(..., wait_until="networkidle", timeout=30000)` + `time.sleep(2)` as an ethical rate limit.
   - `try/except` per page: if one fails, it moves on to the next.
   - Current result: **~60 books (3 pages × 20)**.

3. **Load into Neon with correct types:**
   - Explicit conversion before insert (avoids Postgres `DatatypeMismatch`):
     ```python
     df['fecha'] = pd.to_datetime(df['fecha'])
     df['monto'] = df['monto'].astype(float)
     df['cantidad'] = df['cantidad'].astype(int)
     ```
   - Creates the table if missing:
     ```sql
     CREATE TABLE IF NOT EXISTS scraped_books (
         id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
         producto VARCHAR(100),
         descripcion TEXT,
         categoria VARCHAR(20),
         monto DECIMAL(10,2),
         cantidad INT,
         fecha DATE
     );
     ```
   - Inserts with `df.to_sql('scraped_books', engine, if_exists='append', index=False)`.

## Structure

```
02_web_scraping_/
├── books_scrapper.py  # Main script (connection + scraper + load)
└── README.md
```

## How to reproduce

```bash
# 1. Environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install playwright pandas sqlalchemy psycopg[binary] python-dotenv
playwright install chromium

# 2. Credential (DO NOT commit, already in .gitignore)
# Create PY_data_science/.env with:
# DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Run (from the repo root)
python Projects/02_web_scraping_/books_scrapper.py
```

## Security

- No hardcoded credentials, only `os.getenv("DATABASE_URL")`.
- `.env` ignored by `.gitignore` and out of git history.
- The target site is a public scraping sandbox (`books.toscrape.com`). Respected with `sleep(2)` and `headless=True`.

## Key dependencies

`playwright`, `pandas`, `sqlalchemy`, `psycopg[binary]`, `python-dotenv`
