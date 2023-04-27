CREATE TABLE IF NOT EXISTS Muestra (
    id INT NOT NULL,
    id_alimento INT NOT NULL,
    id_contaminante INT NOT NULL,
    id_comuna INT NOT NULL,
    cantidad INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_alimento) REFERENCES Alimento(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_contaminante) REFERENCES Contaminante(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(id_comuna) REFERENCES Comuna(id) ON DELETE CASCADE ON UPDATE CASCADE
);
