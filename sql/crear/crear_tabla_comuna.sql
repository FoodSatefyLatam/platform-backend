CREATE TABLE IF NOT EXISTS Comuna (
    id INT NOT NULL,
    nombre TEXT,
    id_region INT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_region) REFERENCES Region(id) ON DELETE CASCADE,
);
