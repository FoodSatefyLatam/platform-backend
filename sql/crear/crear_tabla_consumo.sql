CREATE TABLE IF NOT EXISTS Consumo (
    id_persona INT NOT NULL,
    id_alimento INT NOT NULL,
    cantidad FLOAT,
    PRIMARY KEY(id_persona, id_alimento),
    FOREIGN KEY(id_alimento) REFERENCES Alimento(id) ON DELETE CASCADE,
    FOREIGN KEY(id_persona) REFERENCES Persona(id) ON DELETE CASCADE
);
