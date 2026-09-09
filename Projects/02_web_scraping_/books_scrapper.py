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
# 1. CONEXIÓN A NEON (RUTA BLINDADA)
# ------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Sube 2 niveles hasta PY_data_science
ENV_FILE = PROJECT_ROOT / ".env"

print(f"🔍 Buscando .env en: {ENV_FILE}")

if not ENV_FILE.exists():
    raise FileNotFoundError(
        f"❌ No se encontró .env en {ENV_FILE}\n"
        f"   Verifica que exista exactamente en: {PROJECT_ROOT}"
    )

load_dotenv(dotenv_path=ENV_FILE)

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise EnvironmentError("❌ DATABASE_URL no definida en .env")

engine = create_engine(db_url.replace("postgresql://", "postgresql+psycopg://"))
print("✅ Conectado a Neon Cloud | Iniciando scraper...")

# ------------------------------------------------------------------
# 2. SCRAPER CON PLAYWRIGHT
# ------------------------------------------------------------------
def scrape_books(max_pages=3):
    data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i in range(1, max_pages + 1):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            print(f"️  Página {i}/{max_pages}...")
            
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
                
                time.sleep(2)  # Rate limit ético
                
            except Exception as e:
                print(f"️ Error pág {i}: {e}")
        
        browser.close()
    
    return pd.DataFrame(data)

# ------------------------------------------------------------------
# 3. CARGA A NEON CON TIPOS CORRECTOS
# ------------------------------------------------------------------
df = scrape_books(max_pages=3)

if not df.empty:
    #  CONVERSIÓN EXPLÍCITA DE TIPOS (EVITA DatatypeMismatch EN POSTGRES)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['monto'] = df['monto'].astype(float)
    df['cantidad'] = df['cantidad'].astype(int)
    
    print(f"📊 Tipos corregidos: {df.dtypes.to_dict()}")

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
    
    # Usar 'replace' solo si quieres reiniciar la tabla limpia esta vez
    df.to_sql('scraped_books', engine, if_exists='append', index=False)
    print(f"\n✅ {len(df)} libros cargados exitosamente a Neon Cloud")
    print(df.head())
else:
    print("❌ No se extrajeron datos")