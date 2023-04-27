CREATE TABLE IF NOT EXISTS Persona (
    id INT NOT NULL, 
    peso FLOAT,
    altura INT,
    sexo TINYINT,
    edad INT,
    PRIMARY KEY(id),   
    FOREIGN KEY(comuna_id) REFERENCES Comuna(id)
);
