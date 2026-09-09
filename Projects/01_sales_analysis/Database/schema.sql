-- schema.sql: Define la estructura de la base de datos
-- Compatible con PostgreSQL 18+

-- Eliminar tabla si existe para permitir re-creación limpia
DROP TABLE IF EXISTS ventas;

-- Crear tabla principal de ventas
CREATE TABLE ventas (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha DATE NOT NULL,
    producto VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    cantidad INT NOT NULL CHECK (cantidad > 0)
);

-- Índices para optimizar consultas futuras
CREATE INDEX idx_ventas_categoria ON ventas(categoria);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);