CREATE TABLE IF NOT EXISTS Alimento (
    id INT NOT NULL,
    nombre TEXT,
    categoria_id INT,
    FOREIGN KEY(categoria_id) REFERENCES Categoria(id) ON DELETE SET NULL,
    PRIMARY KEY(id)
);
