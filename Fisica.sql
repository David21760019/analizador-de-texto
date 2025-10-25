-- Crear la tabla Fisica
CREATE TABLE Fisica (
    id SERIAL PRIMARY KEY,
    concepto VARCHAR(50) NOT NULL
);

-- Insertar los 15 conceptos relacionados con la física
INSERT INTO Fisica (concepto) VALUES
('Energía'),
('Fuerza'),
('Movimiento'),
('Masa'),
('Velocidad'),
('Aceleración'),
('Gravedad'),
('Trabajo'),
('Potencia'),
('Temperatura'),
('Presión'),
('Ondas'),
('Electricidad'),
('Magnetismo'),
('Materia');
