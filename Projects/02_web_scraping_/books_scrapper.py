# Projects/02_web_scraping_/books_scraper.py
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# ------------------------------------------------------------------
# 1. NEON CONNECTION (HARDENED PATH)
# ------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Go 2 levels up to PY_data_science
ENV_FILE = PROJECT_ROOT / ".env"

print(f"🔍 Looking for .env at: {ENV_FILE}")

if not ENV_FILE.exists():
    raise FileNotFoundError(
        f"❌ .env not found at {ENV_FILE}\n"
        f"   Make sure it exists exactly at: {PROJECT_ROOT}"
    )

load_dotenv(dotenv_path=ENV_FILE)

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise EnvironmentError("❌ DATABASE_URL is not set in .env")

engine = create_engine(db_url.replace("postgresql://", "postgresql+psycopg://"))
print("✅ Connected to Neon Cloud | Starting scraper...")

# ------------------------------------------------------------------
# 2. PLAYWRIGHT SCRAPER
# ------------------------------------------------------------------
def scrape_books(max_pages=3):
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(1, max_pages + 1):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            print(f"️  Page {i}/{max_pages}...")

            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                products = page.query_selector_all("article.product_pod")

                for prod in products:
                    title = prod.query_selector("h3 > a").get_attribute("title").strip()[:80]
                    price_text = prod.query_selector(".price_color").inner_text().strip()
                    price = float(re.sub(r'[^\d.]', '', price_text))
                    rating = prod.query_selector("p.star-rating").get_attribute("class").split()[-1]
                    desc = (prod.query_selector("p.star-rating").get_attribute("title") or "N/A")[:150]

                    data.append({
                        'producto': title,
                        'descripcion': desc,
                        'categoria': rating,
                        'monto': price,
                        'cantidad': 1,
                        'fecha': f'2024-01-{str(i).zfill(2)}'
                    })

                time.sleep(2)  # Ethical rate limit

            except Exception as e:
                print(f"️ Page {i} error: {e}")

        browser.close()

    return pd.DataFrame(data)

# ------------------------------------------------------------------
# 3. LOAD INTO NEON WITH CORRECT TYPES
# ------------------------------------------------------------------
df = scrape_books(max_pages=3)

if not df.empty:
    #  EXPLICIT TYPE CONVERSION (AVOIDS POSTGRES DatatypeMismatch)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['monto'] = df['monto'].astype(float)
    df['cantidad'] = df['cantidad'].astype(int)

    print(f"📊 Fixed types: {df.dtypes.to_dict()}")

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS scraped_books (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                producto VARCHAR(100),
                descripcion TEXT,
                categoria VARCHAR(20),
                monto DECIMAL(10,2),
                cantidad INT,
                fecha DATE
            )
        """))
        conn.commit()

    # Use 'replace' only if you want a clean table restart this time
    df.to_sql('scraped_books', engine, if_exists='append', index=False)
    print(f"\n✅ {len(df)} books successfully loaded to Neon Cloud")
    print(df.head())
else:
    print("❌ No data extracted")
