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
col_alimentos = ["g_producto", "homologado"]
df_alimentos_individuales = pd.read_csv("../../csv/ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv", sep=',', header=0, usecols=col_alimentos, encoding="ISO-8859-1")
print(df_alimentos_individuales.shape)

# Inserción de datos en la tabla Categoria
sql_categoria = "INSERT INTO Categoria(nombre) VALUES (%s)"
mydb.commit()

categorias = df_alimentos_individuales["homologado"].unique()
data_categoria = [(categoria,) for categoria in categorias]
cursor.executemany(sql_categoria, data_categoria)
mydb.commit()

# Inserción de datos en la tabla Alimento
sql_alimento = "INSERT INTO Alimento(nombre, categoria_id) VALUES (%s, %s)"

alimentos = df_alimentos_individuales[["g_producto", "homologado"]].drop_duplicates(subset=["g_producto", "homologado"], keep="first")

for ind in alimentos.index:
    nombre = alimentos["g_producto"][ind]
    categoria = alimentos["homologado"][ind]

    cursor.execute("SELECT id FROM Categoria WHERE nombre=%s", (categoria,))
    categoria_id = cursor.fetchall()[0][0]

    cursor.execute(sql_alimento, (nombre, categoria_id))
    mydb.commit()
