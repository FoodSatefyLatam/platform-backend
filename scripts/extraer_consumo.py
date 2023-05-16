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
col_consumo = ["folio", "homologado","consumo_mes", "mg_ml"]
df_consumo_alimentos = pd.read_csv("../../csv/ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv", sep=",", header=0, usecols=col_consumo, encoding="ISO-8859-1")

# Eliminar las filas donde la columna homologado esté vacía
#df_consumo_alimentos.dropna(subset=['homologado'], inplace=True)

# Actualizar el índice del DataFrame después de eliminar las filas
#df_consumo_alimentos.reset_index(drop=True, inplace=True)

# Imprimir el DataFrame
print(df_consumo_alimentos)

# Inserción de datos en la tabla Consumo
sql_consumo = "INSERT INTO Consumo(id_persona, id_alimento, cantidad, cantidad_mes) VALUES (%s, %s, %s, %s)"

for index, row in df_consumo_alimentos.iterrows():
    print(row["homologado"].strip().lower().replace(",",""))
    # Obtener id categoria desde homologado

    # cursor.execute("SELECT id FROM Categoria WHERE nombre=%s",(row["homologado"],))
    # id_categoria = cursor.fetchall()[0][0]
    
    homologado = row["homologado"].strip().lower().replace(",", "")
    if homologado == "":
        continue
    
    cursor.execute("SELECT id FROM Alimento WHERE nombre=%s", (homologado,))
    id_alimento = cursor.fetchall()
    if not id_alimento:
        continue
    id_alimento = id_alimento[0][0]

    # ROW["col"].isnull() ? 0 : ROW["col"]
    # Insertar la fila en la tabla Consumo
    if pd.isna(row["consumo_mes"]) :
        row["consumo_mes"] = 0
    
    if pd.isna(row["mg_ml"]) :
        row["mg_ml"] = 0

    cursor.execute("SELECT * FROM Consumo WHERE id_persona=%s AND id_alimento=%s",(row["folio"],id_alimento))
    consumo = cursor.fetchall()

    if consumo == []: 
      cursor.execute(sql_consumo, (row["folio"], id_alimento, row["consumo_mes"], row["mg_ml"]))
    else :
        cantidad = consumo[0][2] + row["mg_ml"]
        cantidad_mes = consumo[0][3] + row["consumo_mes"]
        cursor.execute("UPDATE Consumo Set cantidad = %s , cantidad_mes = %s WHERE id_persona = %s AND id_alimento = %s",(cantidad,cantidad_mes,row["folio"],id_alimento))
    # cursor.execute(sql_consumo, (row["folio"], id_alimento, row["consumo_mes"], row["mg_ml"]))   
    mydb.commit()

