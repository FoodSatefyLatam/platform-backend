import openpyxl

from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["GET", "POST"])
def reporte():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        reporte = []
        request_json = request.get_json()
        s = ""
        if(request_json["sexo"] != None):
            sexo = request_json["sexo"]
            s = "sexo = " + sexo.to_string() + " AND"

        min_edad = request_json["edad"][0]
        max_edad = request_json["edad"][1]
        min_peso = request_json["peso"][0]
        max_peso = request_json["peso"][1]
        alimentos = request_json.get("alimentos")
        contaminantes = []
        cur.execute("SELECT id, nombre, limite_diario FROM Contaminante")
        res = cur.fetchall()
        for contaminante in res:
            contaminantes.append({"id":contaminante[0], "nombre": contaminante[1], "limite_diario": contaminante[2]})

        #print(contaminantes)

        for alimento in alimentos:
            cur.execute("SELECT id FROM Alimento WHERE nombre = %s",[alimento["nombre"]])
            res = cur.fetchall()

            if(res[0] is not None):
                alimento["id"] = res[0][0]
            else:
                return "error: alimento " + alimento["nombre"] + " no encontrado."
            
            for contaminante in contaminantes:
                if not contaminante["nombre"] in alimento:
                    cur.execute("SELECT Avg(cantidad)  FROM  Muestra WHERE id_contaminante=%s AND id_alimento=%s" ,([contaminante["id"]],[alimento["id"]]))
                    res = cur.fetchall()
                    alimento[contaminante["nombre"] ] = res[0][0]
        
        #print(alimentos)

        regiones = []
        cur.execute("SELECT id FROM Region")
        res = cur.fetchall()
        for region in res:
            regiones.append({"id": region[0], "comunas": []})

        #print(regiones)

        for region in regiones:
            cur.execute("SELECT id FROM Comuna WHERE id_region =%s",[region["id"]])
            res = cur.fetchall()
            for comuna in res:
                region["comunas"].append(comuna[0])
    
        #print(regiones)

        sql_alimentos = "Consumo.id_alimento = " + str(alimentos[0]["id"])
        for alimento in alimentos:
            if(alimento == alimentos[0]): 
                continue
            else:
                sql_alimentos+= " OR Consumo.id_alimento = " + str(alimento["id"])
        
        #print(sql_alimentos)

        for region in regiones:
            reporte_region = {
                "region":region["id"]
            }
            sql_comunas = "comuna_id = " + str(region["comunas"][0])
            for comuna in region["comunas"]:
                if(comuna == region["comunas"][0]): 
                    continue
                else:
                    sql_comunas += " OR comuna_id = " + str(comuna)
            
            #print(sql_comunas)
            
            cur.execute("SELECT p.id, p.peso, Consumo.cantidad_mes, Consumo.id_alimento FROM (SELECT * FROM Persona WHERE "+ s +" edad > %s AND edad < %s AND peso > %s AND peso < %s AND " + sql_comunas + " ) AS p LEFT JOIN Consumo ON p.id = Consumo.id_persona WHERE Consumo.cantidad_mes != 0.0 AND "+ sql_alimentos + ";",[min_edad, max_edad, min_peso, max_peso])
            res = cur.fetchall()

            personas = {}
            avg_peso = 0.0
            avg_contaminantes = {}
            for consumo in res:
                if not consumo[0] in personas:
                    avg_peso += consumo[1]
                    personas[consumo[0]] = "ok"
                for contaminante in contaminantes:
                    alimento = list(filter(lambda _alimento: _alimento['id'] == consumo[3], alimentos))
                    if not contaminante["nombre"] in avg_contaminantes:
                        avg_contaminantes[contaminante["nombre"]] = 0.0
                    if(alimento[0][contaminante["nombre"]] == None):
                        continue
                    avg_contaminantes[contaminante["nombre"]] += (alimento[0][contaminante["nombre"]] * consumo[2])/(30*1000)

            avg_peso =  avg_peso /len(personas)
            
            formula = {}
            for contaminante in contaminantes:
                avg_contaminantes[contaminante["nombre"]] = avg_contaminantes[contaminante["nombre"]]/ len(personas)
                if contaminante["limite_diario"] == None:
                    formula[contaminante["nombre"]] = "Sin Datos de limite diario"
                else:
                    formula[contaminante["nombre"]] = avg_contaminantes[contaminante["nombre"]] / (avg_peso * contaminante["limite_diario"])


            reporte_region["personas"] = len(personas)
            reporte_region["prom_peso"] = avg_peso
            reporte_region["prom_contaminantes"] = avg_contaminantes
            reporte_region["formula"] = formula

            reporte.append(reporte_region)

        return jsonify(reporte)
    
    elif request.method == "GET":
        respuesta = {}
        nombre_alimentos = {}
        cur.execute("SELECT * FROM Alimento;")
        alimentos = cur.fetchall()
        for alimento in alimentos:
            nombre_alimentos[alimento[0]] = alimento[1]

        cur.execute("SELECT * FROM Consumo;")
        consumos = cur.fetchall()
        for consumo in consumos:
            if consumo[0] in respuesta:
                if(consumo[3] != 0.0):
                    respuesta[consumo[0]][nombre_alimentos[consumo[1]]] = consumo[3]
            else:
                respuesta[consumo[0]] = {}
                if(consumo[3] != 0.0):
                    respuesta[consumo[0]][nombre_alimentos[consumo[1]]] = consumo[3]
        return jsonify(respuesta)
    
    else:
        return "Error"