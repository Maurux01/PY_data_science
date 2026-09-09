-- seeds.sql: Populates the database with sample data
-- Run AFTER schema.sql

INSERT INTO ventas (fecha, producto, categoria, monto, cantidad) VALUES
('2023-10-01', 'Laptop Gamer', 'Computadoras', 1500.00, 2),
('2023-10-02', 'Mouse Inalámbrico', 'Accesorios', 25.50, 10),
('2023-10-03', 'Teclado Mecánico', 'Accesorios', 89.99, 5),
('2023-10-04', 'Monitor 27"', 'Computadoras', 300.00, 3),
('2023-10-05', 'Laptop Gamer', 'Computadoras', 1500.00, 1),
('2023-10-06', 'Audífonos Bluetooth', 'Accesorios', 50.00, 8);