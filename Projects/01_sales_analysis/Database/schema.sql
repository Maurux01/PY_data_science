-- schema.sql: Defines the database structure
-- PostgreSQL 18+ compatible

-- Drop table if exists to allow a clean re-creation
DROP TABLE IF EXISTS ventas;

-- Main sales table
CREATE TABLE ventas (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha DATE NOT NULL,
    producto VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
    cantidad INT NOT NULL CHECK (cantidad > 0)
);

-- Indexes to optimize future queries
CREATE INDEX idx_ventas_categoria ON ventas(categoria);
CREATE INDEX idx_ventas_fecha ON ventas(fecha);