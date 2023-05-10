import pandas as pd
import mysql.connector

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="grupo1",
    password="gq0xf7vk",
    database='grupo1'
)

# Verificación de la conexión
print("Connected to:", mydb.get_server_info())

# Creación del cursor para realizar consultas SQL
cursor = mydb.cursor()

# Lectura del archivo CSV de consumo de alimentos
col_consumo = ["folio", "g_producto", "consumo_mes", "mg_ml"]
df_consumo_alimentos = pd.read_csv("../../csv/ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv", sep=",", header=0, usecols=col_consumo, encoding="ISO-8859-1")

# Imprimir el DataFrame
print(df_consumo_alimentos)

# Inserción de datos en la tabla Consumo
sql_consumo = "INSERT INTO Consumo(id_persona, id_alimento, consumo, consumo_mes) VALUES (%s, %s, %s, %s)"

for index, row in df_consumo_alimentos.iterrows():
    
    # Obtener el id_alimento a partir del g_producto
    cursor.execute("SELECT id FROM Alimento WHERE nombre=%s", (row["g_producto"],))
    id_alimento = cursor.fetchall()[0][0]
    
    # Insertar la fila en la tabla Consumo
    cursor.execute(sql_consumo, (row["folio"], id_alimento, row["consumo_mes"], row["mg_ml"]))
    mydb.commit()
