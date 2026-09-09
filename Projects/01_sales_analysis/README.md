# 01 — Análisis de Ventas | Tienda Tech

Proyecto de análisis exploratorio de ventas conectado a **PostgreSQL Serverless (Neon Cloud)**, con visualización estadística en Python.

## Qué se hizo

1.  **Conexión segura a la nube (Neon):**
    *   Se usa `python-dotenv` + `os.getenv("DATABASE_URL")` para leer la credencial desde el `.env` en la raíz del repo.
    *   No hay contraseñas ni connection strings hardcodeados en el código. Si falta `DATABASE_URL`, el notebook falla con `EnvironmentError` explícito.
    *   Conexión con `SQLAlchemy + psycopg v3` (`postgresql+psycopg://`).

2.  **Migración automática desde SQL:**
    *   `Database/schema.sql`: crea/recrea la tabla `ventas` (id identity PK, fecha, producto, categoria, monto > 0, cantidad > 0) + índices en `categoria` y `fecha`. Compatible PostgreSQL 18+.
    *   `Database/seeds.sql`: inserta 6 registros de prueba (Laptop Gamer, Mouse, Teclado, Monitor 27", Audífonos).
    *   El notebook resuelve las rutas con `pathlib.Path.cwd()` para que funcione tanto si el kernel inicia en `01_sales_analysis/` como en la raíz, y verifica `exists()` antes de ejecutar.
    *   Usa `conn.commit()` obligatorio en psycopg v3 y verifica con `SELECT COUNT(*)`.

3.  **Análisis estadístico con `pandas / numpy / scipy`:**
    *   Carga con `pd.read_sql("SELECT * FROM ventas", engine)`.
    *   Calcula `precio_unitario = monto / cantidad`, correlación de Pearson (`scipy.stats.pearsonr`), KDE (`scipy.stats.gaussian_kde`) y Coeficiente de Variación (`std/mean*100`).
    *   Resultado actual: **CV = 124.8%** (alta dispersión) y **Producto Top Pareto A: Laptop Gamer ($1,500.00)**.

4.  **Visualización (4 paneles con `matplotlib + seaborn`):**
    *   **ABC / Pareto:** barras de monto por producto + línea de % acumulado.
    *   **Distribución:** histograma + KDE + media y mediana.
    *   **Boxplot por categoría:** variabilidad `Computadoras` vs `Accesorios`.
    *   **Scatter Correlación:** `cantidad` vs `precio_unitario`, tamaño = `monto`, hue = `categoria`, con `r` y `p-value` en el título.

## Estructura

```
01_sales_analysis/
├── analysis.ipynb   # Notebook principal (conexión + migración + análisis + gráficos)
├── Database/
│   ├── schema.sql   # DDL tabla ventas
│   └── seeds.sql    # 6 registros de prueba
└── README.md
```

## Cómo reproducir

```bash
# 1. Crear entorno
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install pandas sqlalchemy psycopg[binary] python-dotenv matplotlib seaborn scipy numpy jupyter

# 2. Configurar credencial (NO subir a git, ya está en .gitignore)
# Crear C:\...\PY_data_science\.env con:
# DATABASE_URL=postgresql://usuario:password@ep-xxx.neon.tech/db?sslmode=require

# 3. Abrir notebook
jupyter notebook Projects/01_sales_analysis/analysis.ipynb
```

## Seguridad

*   `.env` ignorado por `.gitignore` y **no** está en el historial de git (verificado con `git log -- .env` vacío).
*   El código solo referencia `DATABASE_URL` por nombre, nunca imprime su valor.
*   Recomendación antes de `git add`: en Jupyter hacer `Cell > All Output > Clear` para no subir rutas locales absolutas (`C:\Users\...`) que aparecen en los `print()` de debug.

## Dependencias clave

`sqlalchemy`, `psycopg`, `python-dotenv`, `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`


# Preview 

![01_sales_analysis](../../Assets/01_sales_analysis.png)