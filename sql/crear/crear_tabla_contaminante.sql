CREATE TABLE IF NOT EXISTS Contaminante (
    id INT NOT NULL,
    nombre TEXT,
    alias TEXT,
    limite_diario FLOAT,
    PRIMARY KEY(id)
);
