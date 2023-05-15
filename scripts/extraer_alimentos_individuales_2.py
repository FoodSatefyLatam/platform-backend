import pandas as pd
import mysql.connector

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="grupo1",
    password="gq0xf7vk",
    database='grupo1'
)

print("Connected to:", mydb.get_server_info())

# Cursor para realizar consultas SQL
cursor = mydb.cursor()

# Lectura del archivo de alimentos individuales
df_alimentos_individuales = pd.read_csv(
    "../../csv/ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv",
    usecols=["homologado"],
    encoding="ISO-8859-1"
)

# Elimina los duplicados y los valores nulos
df_alimentos_individuales.drop_duplicates(subset=["homologado"], inplace=True)
df_alimentos_individuales.dropna(subset=["homologado"], inplace=True)

# Inserción de datos en la tabla Alimento
sql_alimento = "INSERT INTO Alimento(nombre) VALUES (%s)"

registros = [(nombre.strip().lower(),) for nombre in df_alimentos_individuales["homologado"]]
print(len(registros))
cursor.executemany(sql_alimento, registros)
mydb.commit()

