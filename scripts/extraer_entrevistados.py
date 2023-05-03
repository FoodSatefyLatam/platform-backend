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
    "macrozona",
    "id", #id
    "sex", #sexo
    "ht", #altura
    "wgt", #peso
    "ageyrs", #años
]

#falta le comuna y region 
#para alimentos ajustados
col_entrevistado_aa = [
    "folio",
    "region",
    "g_comuna"
]

df_najustado = pd.read_csv("../../csv/ENCA_Er24h_Nutrientes_AJUSTADO.csv", sep=',', header=0, usecols = col_entrevistado_na)

df_anajustado = pd.read_csv("../../csv/ENCA_ETCC_ALIMENTOS_AGRUPADOS.csv", sep=',', header=0, usecols= col_entrevistado_aa)
df_anajustado.rename(columns={'folio': 'id'}, inplace=True)

print(df_anajustado.shape)

print(df_najustado.shape)

df_entrevistado = pd.merge(df_anajustado, df_najustado, on = "id", how="inner")
df_entrevistado.drop_duplicates(subset=['id'], keep= "first", inplace=True)

print(df_entrevistado.shape)

print(df_entrevistado.head())

df_entrevistado.to_csv("entrevistados.csv", index=False)

sql_persona = "INSERT INTO persona(edad,peso,sexo,altura,id_comuna,id_persona) VALUES (%s,%s,%s,%s,%s,%s)"
#comuna debe tener id auto increment
sql_comuna = "INSERT INTO Comuna(nombre_comuna, id_region) VALUES (%s)"
sql_region = "INSERT INTO Region(id_region, id_macrozona) VALUES (%s)"
#macrozona debe tener id auto increment
sql_macrozona = "INSERT INTO Macrozona(nombre) VALUES(%s)"

for ind in df_entrevistado.index:
    edad = df_entrevistado["ageyrs"][ind]
    peso = df_entrevistado["wgt"][ind]
    # 0 hombre | 1 mujer
    sexo = (0 , 1)[df_entrevistado["sex"][ind] == "Mujer"]
    altura = df_entrevistado["ht"][ind]
    id_persona = df_entrevistado["id"][ind]
    comuna = df_entrevistado["g_comuna"][ind].strip().lower()
    region = df_entrevistado["region"][ind].strip().lower()
    macrozona = df_entrevistado["macrozona"][ind].strip().lower()

    cursor.execute("SELECT * FROM Comuna WHERE nombre=\'{}\'".format(comuna))
    if cursor.fetchall() == []:
        cursor.execute("SELECT * FROM Region WHERE id=\'{}\'".format(region))
        if cursor.fetchall() == []:
            cursor.execute("SELECT * FROM Macrozona WHERE nombre=\'{}\'".format(region))
            if cursor.fetchall() == []:
                cursor.execute(sql_macrozona, [macrozona])
                mydb.commit()
            cursor.execute("SELECT * FROM Macrozona WHERE nombre=\'{}\'".format(region))
            id_macrozona = cursor.fetchall()[0][0]
            cursor.execute(sql_region, [region, id_macrozona])
            mydb.commit()
        cursor.execute(sql_comuna, [comuna, int(region)])
        mydb.commit()

    cursor.execute("SELECT * FROM Comuna WHERE nombre=\'{}\'".format(comuna))
    id_comuna = cursor.fetchall()[0][0]

    cursor.execute(sql_persona, [int(edad), float(peso.replace(",",".")), sexo, float(altura.replace(",",".")), id_comuna, int(id_persona)])
    mydb.commit()