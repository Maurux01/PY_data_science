# 02 — Web Scraping | Books to Scrape → Neon

Scraper ético con **Playwright (Chromium headless)** que extrae libros de `books.toscrape.com` y los carga a **PostgreSQL Serverless (Neon)** en la tabla `scraped_books`.

## Qué hace `books_scrapper.py`

1. **Conexión segura a Neon (ruta blindada):**
   - Resuelve `.env` subiendo 2 niveles desde el script (`Projects/02_web_scraping_/` → raíz `PY_data_science/`).
   - Falla explícito si no existe `.env` (`FileNotFoundError`) o si falta `DATABASE_URL` (`EnvironmentError`).
   - Convierte `postgresql://` → `postgresql+psycopg://` (psycopg v3).

2. **Scraper (`scrape_books(max_pages=3)`):**
   - Itera `https://books.toscrape.com/catalogue/page-{i}.html`.
   - Por cada `article.product_pod` extrae:
     - `producto`: `h3 > a[title]` (recortado a 80 chars)
     - `monto`: `.price_color` limpiado con `re.sub(r'[^\d.]', '', ...)` → `float`
     - `categoria`: última clase de `p.star-rating` (ej. `Three`, `Five`)
     - `descripcion`: `title` del rating o `"N/A"` (150 chars)
     - `cantidad`: `1`, `fecha`: `2024-01-{i:02d}`
   - `page.goto(..., wait_until="networkidle", timeout=30000)` + `time.sleep(2)` como rate-limit ético.
   - `try/except` por página: si una falla, sigue con las demás.
   - Resultado actual: **~60 libros (3 páginas × 20)**.

3. **Carga a Neon con tipos correctos:**
   - Conversión explícita antes del insert (evita `DatatypeMismatch` en Postgres):
     ```python
     df['fecha'] = pd.to_datetime(df['fecha'])
     df['monto'] = df['monto'].astype(float)
     df['cantidad'] = df['cantidad'].astype(int)
     ```
   - Crea la tabla si no existe:
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
   - Inserta con `df.to_sql('scraped_books', engine, if_exists='append', index=False)`.

## Estructura

```
02_web_scraping_/
├── books_scrapper.py  # Script principal (conexión + scraper + carga)
└── README.md
```

## Cómo reproducir

```bash
# 1. Entorno
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install playwright pandas sqlalchemy psycopg[binary] python-dotenv
playwright install chromium

# 2. Credencial (NO subir a git, ya está en .gitignore)
# Crear PY_data_science/.env con:
# DATABASE_URL=postgresql://usuario:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Ejecutar (desde la raíz del repo)
python Projects/02_web_scraping_/books_scrapper.py
```

## Seguridad

- Sin credenciales hardcodeadas, solo `os.getenv("DATABASE_URL")`.
- `.env` ignorado por `.gitignore` y fuera del historial de git.
- El sitio objetivo es un sandbox público para scraping (`books.toscrape.com`). Se respeta con `sleep(2)` y `headless=True`.

## Dependencias clave

`playwright`, `pandas`, `sqlalchemy`, `psycopg[binary]`, `python-dotenv`
