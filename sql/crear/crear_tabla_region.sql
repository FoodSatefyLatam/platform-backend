CREATE TABLE IF NOT EXISTS Region (        
    id INT NOT NULL,
    nombre TEXT,
    id_macrozona INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_macrozona) REFERENCES Macrozona(id) ON DELETE CASCADE
);
