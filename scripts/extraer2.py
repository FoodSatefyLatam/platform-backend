import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abcd.1234",
  database='proyectocontaminantes'
)
cursor = mydb.cursor()

col_individuales = ["folio",
"g_producto",
"v3_1", #frecuencia semana
"v3_2", #frecuencia mes
"consumo_mes",
"region",
"homologado"
]

col_ajustado = ["id",
"ageyrs",
"sex",
"wgt",
"ht"
]

df_ajustado = pd.read_csv("ENCA_Er24h_Nutrientes_AJUSTADO.csv", sep=';', header=0, usecols = col_ajustado)

df_individual = pd.read_csv("ENCA_ETCC_ALIMENTOS_INDIVIDUALES.csv", sep=';', header=0, usecols= col_individuales)

#print(df_ajustado)

#print(df_individual)

'''
sql_persona = "INSERT INTO persona(edad,peso,sexo,altura,id_region,id_folio) VALUES (%s,%s,%s,%s,1,%s)"
sql_folio = "INSERT INTO folio(id_folio) VALUES (%s)"
for ind in df_ajustado.index:
    edad = df_ajustado["ageyrs"][ind]
    peso = df_ajustado["wgt"][ind]
    sexo = df_ajustado["sex"][ind]
    altura = df_ajustado["ht"][ind]
    id_folio = df_ajustado["id"][ind]
    cursor.execute("SELECT * FROM folio WHERE id_folio=\'{}\'".format(id_folio))
    if cursor.fetchall() == []:
        cursor.execute(sql_folio, [int(id_folio)])
        mydb.commit()
    
    cursor.execute(sql_persona, [int(edad), float(peso.replace(",",".")), int(sexo), float(altura.replace(",",".")), int(id_folio)])
    mydb.commit()
'''

sql_consumo = "INSERT INTO consumo(cantidad, frecuencia_semanal, frecuencia_mensual, id_alimento, id_folio) VALUES (%s,%s,%s,%s,%s)"
for ind in df_individual.index:
    try:
        cantidad = float((df_individual["consumo_mes"][ind]).strip().replace(",",".")) #cantidad consumida en un mes(u.metrica)
    except:
        cantidad = 0.0
    
    frecuencia_semanal = int(df_individual["v3_1"][ind])  #
    frecuencia_mensual = int(df_individual["v3_2"][ind])
    id_folio = int(df_individual["folio"][ind])
    alimento = df_individual["homologado"][ind].strip().lower()
    alimento =  alimento.replace("pescado","").strip()
    if(alimento == ""):
        alimento = "pescado"
    alimento = alimento.replace("natural","").replace("marisco","").replace("en conserva","").replace("conserva","").strip()
    
    try:
        region = int(df_individual["region"][ind])
    except:
        region = 1

    cursor.execute("UPDATE persona SET id_region =\'{}\'  WHERE id_folio = \'{}\' ".format(region, id_folio))
    mydb.commit()

    if(cantidad == 0.0):
        continue

    cursor.execute("SELECT id_alimento FROM alimento WHERE especie = \'{}\'".format(alimento))
    id_alimento = cursor.fetchone()
    if not id_alimento is None :
        id_alimento = id_alimento[0]
        cursor.execute(sql_consumo, [cantidad,frecuencia_semanal,frecuencia_mensual,id_alimento, id_folio])
        mydb.commit()