# 01 — Sales Analysis | Tech Store

Exploratory sales analysis project connected to **PostgreSQL Serverless (Neon Cloud)**, with statistical visualization in Python.

## What was done

1.  **Secure cloud connection (Neon):**
    *   `python-dotenv` + `os.getenv("DATABASE_URL")` reads the credential from `.env` at the repo root.
    *   No hardcoded passwords or connection strings. If `DATABASE_URL` is missing, the notebook fails with an explicit `EnvironmentError`.
    *   Connection via `SQLAlchemy + psycopg v3` (`postgresql+psycopg://`).

2.  **Automatic migration from SQL:**
    *   `Database/schema.sql`: creates/recreates the `ventas` table (identity PK id, fecha, producto, categoria, monto > 0, cantidad > 0) + indexes on `categoria` and `fecha`. PostgreSQL 18+ compatible.
    *   `Database/seeds.sql`: inserts 6 sample rows (Laptop Gamer, Mouse, Teclado, Monitor 27", Audífonos).
    *   The notebook resolves paths with `pathlib.Path.cwd()` so it works whether the kernel starts in `01_sales_analysis/` or at the root, and checks `exists()` before running.
    *   Uses mandatory `conn.commit()` on psycopg v3 and verifies with `SELECT COUNT(*)`.

3.  **Statistical analysis with `pandas / numpy / scipy`:**
    *   Loads with `pd.read_sql("SELECT * FROM ventas", engine)`.
    *   Computes `precio_unitario = monto / cantidad`, Pearson correlation (`scipy.stats.pearsonr`), KDE (`scipy.stats.gaussian_kde`) and Coefficient of Variation (`std/mean*100`).
    *   Current result: **CV = 124.8%** (high dispersion) and **Top Pareto product A: Laptop Gamer ($1,500.00)**.
    *   Note: with `n=6` the p-value is illustrative only, not statistically significant.

4.  **Visualization (4 panels with `matplotlib + seaborn`):**
    *   **ABC / Pareto:** monto bars per product + cumulative % line.
    *   **Distribution:** histogram + KDE + mean and median.
    *   **Boxplot by category:** `Computadoras` vs `Accesorios` variability.
    *   **Correlation scatter:** `cantidad` vs `precio_unitario`, size = `monto`, hue = `categoria`, with `r` and `p-value` in the title.

## Structure

```
01_sales_analysis/
├── analysis.ipynb   # Main notebook (connection + migration + analysis + charts)
├── Database/
│   ├── schema.sql   # ventas table DDL
│   └── seeds.sql    # 6 sample rows
└── README.md
```

## How to reproduce

```bash
# 1. Create environment
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install pandas sqlalchemy psycopg[binary] python-dotenv matplotlib seaborn scipy numpy jupyter

# 2. Set credential (DO NOT commit, already in .gitignore)
# Create C:\...\PY_data_science\.env with:
# DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Open notebook
jupyter notebook Projects/01_sales_analysis/analysis.ipynb
```

## Security

*   `.env` ignored by `.gitignore` and **not** in git history (verified with empty `git log -- .env`).
*   Code only references `DATABASE_URL` by name, never prints its value.
*   Recommendation before `git add`: in Jupyter run `Cell > All Output > Clear` to avoid pushing local absolute paths (`C:\Users\...`) that appear in debug `print()` output.

## Key dependencies

`sqlalchemy`, `psycopg`, `python-dotenv`, `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`


# Preview

![01_sales_analysis](../../Assets/01_sales_analysis.png)
