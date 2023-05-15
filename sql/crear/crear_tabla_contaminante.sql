CREATE TABLE IF NOT EXISTS Contaminante (
    id INT NOT NULL AUTO_INCREMENT,
    nombre TEXT,
    alias TEXT,
    limite_diario FLOAT,
    PRIMARY KEY(id)
);
