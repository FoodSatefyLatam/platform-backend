import openpyxl

from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["GET", "POST"])
def reporte():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        reporte = {}
        request_json = request.get_json()
        sexo = request_json["sexo"]
        s = ""
        if(sexo != 0):
            s = "sexo = " + sexo.to_string() - 1 + " AND"
        min_edad = request_json["edad"][0]
        max_edad = request_json["edad"][1]
        min_peso = request_json["peso"][0]
        max_peso = request_json["peso"][1]
        alimentos = request_json.get("alimentos")
        contaminantes = []
        cur.execute("SELECT id, nombre, limite_diario FROM Contaminante")
        res = cur.fetchall()
        for contaminante in res:
            contaminantes.append({"id":res[0], "nombre": res[1], "limite_diario": res[2]})

        print(contaminantes)

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
        
        print(alimentos)

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