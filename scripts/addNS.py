import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="grupo1",
  password="gq0xf7vk",
  database='grupo1'
)

print("Connected to:", mydb.get_server_info())

cursor = mydb.cursor()

#para nutrientes_ajustados
col_entrevistado_na = [
    "id", #id
    "       Nivel socioeconómico    "
]

df_najustado = pd.read_csv("../../csv/ENCA_Er24h_Nutrientes_AJUSTADO.csv", sep=',', header=0, usecols = col_entrevistado_na)

df_najustado.rename(columns={'       Nivel socioeconómico    ': 'ns'}, inplace=True)

sql_persona = "UPDATE Persona SET ns=%s WHERE id = %s;"

for ind in df_najustado.index:
    cursor.execute(sql_persona,[df_najustado["ns"][ind], df_najustado["id"][ind]])
    mydb.commit()

