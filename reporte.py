from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["POST"])
def reporte():
    reporte = {}
    cur = mysql.connection.cursor()
    sexo = 0
    min_edad = 0
    max_edad = 1000
    min_peso = 0
    max_peso = 1000
    min_altura = 0
    max_altura = 1000
    contaminantes = []
    alimentos = []
    try:
        request_json = request.get_json()
        if request_json.get("sexo"):
            sexo = request_json["sexo"]
        if request_json.get("min_age"):
            min_edad = request_json["min_edad"]
        if request_json.get("max_age"):
            max_edad = request_json["max_edad"]
        if request_json.get("min_peso"):
            min_peso = request_json["min_peso"]
        if request_json.get("max_peso"):
            max_peso = request_json["max_peso"]
        if request_json.get("min_altura"):
            min_altura = request_json["min_altura"]
        if request_json.get("max_altura"):
            max_altura = request_json["max_altura"]            
            
        if(not request_json.get("contaminantes").empty):
            for contaminante in request_json.get("contaminantes"):
                contaminantes.append(contaminante)
        if(request_json.get("alimentos").size != 0):
            for alimento in request_json.get("alimentos"):
                alimentos.append(alimento)
        for contaminante in contaminantes:
            consulta = ("SELECT * FROM persona FULL OUTER JOIN consumo ON id_folio=id_folio FULL OUTER JOIN muestreo ON persona.id_region=muestreo.id_region FULL OUTER JOIN contaminante ON contaminante.id_contaminante=muestreo.id_contaminante WHERE contaminante.nombre = %s",[contaminante])
            cur.execute(consulta)
            reporte[contaminante] = cur.fetchall()
            
    except:
        return "Error"
    
    return jsonify(reporte)