import pandas as pd
import mysql.connector

# Conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="grupo1",
    password="gq0xf7vk",
    database='grupo1'
)

# Cursor para realizar consultas SQL
cursor = mydb.cursor()

# Lectura del archivo csv
col_consumo = ["folio", "g_producto", "consumo_mes", "mg_ml"]
df_consumo = pd.read_csv("/home/grupo1/csv/ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv", sep=',', usecols=col_consumo, header=0)

# Insertar datos en la tabla consumo
for index, row in df_consumo.iterrows():
    folio = row["folio"]
    g_producto = row["g_producto"]
    consumo_mes = row["consumo_mes"]
    mg_ml = row["mg_ml"]

    # Obtener el id de la persona
    cursor.execute("SELECT id_persona FROM persona WHERE folio = %s", (folio,))
    id_persona = cursor.fetchone()[0]

    # Obtener el id del alimento
    cursor.execute("SELECT id_alimento FROM alimentos WHERE g_producto = %s", (g_producto,))
    id_alimento = cursor.fetchone()[0]

    # Insertar en la tabla consumo
    sql = "INSERT INTO consumo (id_persona, id_alimento, consumo, consumo_mes) VALUES (%s, %s, %s, %s)"
    val = (id_persona, id_alimento, consumo_mes, mg_ml)
    cursor.execute(sql, val)

mydb.commit()
