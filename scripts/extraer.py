import pandas as pd
import mysql.connector
import numpy as np
import math

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="abcd.1234",
  database='proyectocontaminantes'
)
cursor = mydb.cursor()


roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000, " ":0}
def romanToInt(S: str) -> int:
    S = S.upper()
    summ= 0
    for i in range(len(S)-1,-1,-1):
        num = roman[S[i]]
        if 3*num < summ: 
            summ = summ-num
        else: 
            summ = summ+num
    return summ

datapath = r"datos.xlsx"

contaminantes = ["As","As i","Cd","Hg", "Pb"]

columnas = ["Año de Muestreo", "N° Asignado por \nLaboratorio","Región","Lugar de Captura o Extracción/País de origen y Marca \n(zona o centro de cultivo, incluyendo nombre, comuna, provincia, región, país)","Categoria","Especie y detalles ","As (mg/kg)","As i (mg/kg)","Cd (mg/kg)","Hg (mg/Kg)","Pb (mg/Kg)"]
data = pd.read_excel(datapath,usecols=columnas)

animales_dic = {}
contaminantes_dic = {}

sql_alimento = "INSERT INTO alimento(categoria,especie) VALUES (%s , %s)"
for index, fila in data.iterrows():
    if columnas[6] in animales_dic.keys():
        continue
    #consultar si existe en la db
    cursor.execute("SELECT * FROM alimento WHERE especie=\'{}\'".format(fila[columnas[5]]))
    if cursor.fetchall() == []:
        cursor.execute(sql_alimento, [fila[columnas[4]], fila[columnas[5]]])
        mydb.commit()

    cursor.execute("SELECT id_alimento FROM alimento WHERE especie =\'{}\'".format(fila[columnas[5]]))
    id_alimento = cursor.fetchall()[0][0]
    animales_dic[fila[columnas[5]]] = id_alimento



sql_contaminante = "INSERT INTO contaminante(nombre, compuesto) VALUES (%s , %s)"
for contaminante in contaminantes:
    cursor.execute("SELECT * FROM contaminante WHERE compuesto=\'{}\'".format(contaminante))
    if cursor.fetchall() == []:
        cursor.execute(sql_contaminante, [contaminante, contaminante])
        mydb.commit()

    cursor.execute("SELECT id_contaminante FROM contaminante WHERE compuesto=\'{}\'".format(contaminante))
    id_contaminante = cursor.fetchall()[0][0]
    contaminantes_dic[contaminante] = id_contaminante

sql_region = "INSERT INTO region(id_region,nombre) VALUES (%s,%s)"
sql_muestreo = "INSERT INTO muestreo(id_region, id_alimento, id_contaminante, cantidad, año, num_lab) VALUES(%s,%s,%s,%s,%s,%s)"
for index, fila in data.iterrows():
    cont_as = 0
    cont_as_i = 0
    cont_cd = 0
    cont_hg = 0
    cont_pb = 0
    if(not pd.isnull(fila[columnas[6]])):
        cont_as = fila[columnas[6]]

    if(not pd.isnull(fila[columnas[7]])):
        cont_as_i = fila[columnas[7]]

    if(not pd.isnull(fila[columnas[8]])):
        cont_cd = fila[columnas[8]]

    if(not pd.isnull(fila[columnas[9]])):
        cont_hg = fila[columnas[9]]

    if(not pd.isnull(fila[columnas[10]])):
        cont_pb = fila[columnas[10]]
        
    cursor.execute("SELECT * FROM region WHERE nombre =\'{}\'".format(fila[columnas[2]]))
    if cursor.fetchall() == []:
        cursor.execute(sql_region,[romanToInt(fila[columnas[2]]), fila[columnas[2]]])
        mydb.commit()
    
    cursor.execute(sql_muestreo, [romanToInt(fila[columnas[2]]) , animales_dic[fila[5]], contaminantes_dic["As"], cont_as, fila[0], fila[1]])
    mydb.commit()
    cursor.execute(sql_muestreo, [romanToInt(fila[columnas[2]]) , animales_dic[fila[5]], contaminantes_dic["As i"], cont_as_i, fila[0], fila[1]])
    mydb.commit()
    cursor.execute(sql_muestreo, [romanToInt(fila[columnas[2]]) , animales_dic[fila[5]], contaminantes_dic["Cd"], cont_cd, fila[0], fila[1]])
    mydb.commit()
    cursor.execute(sql_muestreo, [romanToInt(fila[columnas[2]]) , animales_dic[fila[5]], contaminantes_dic["Hg"], cont_hg, fila[0], fila[1]])
    mydb.commit()
    cursor.execute(sql_muestreo, [romanToInt(fila[columnas[2]]) , animales_dic[fila[5]], contaminantes_dic["Pb"], cont_pb, fila[0], fila[1]])
    mydb.commit()