from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["POST"])
def reporte():
    if request.method != "POST":
        return "error"
    reporte = {}
    cur = mysql.connection.cursor()
    request_json = request.get_json()
    sexo = request_json["sexo"]
    min_edad = request_json["min_edad"]
    max_edad = request_json["max_edad"]
    min_peso = request_json["min_peso"]
    max_peso = request_json["max_peso"]
    min_altura = request_json["min_altura"]
    max_altura = request_json["max_altura"]
    alimentos = request_json.get("alimentos")
    contaminantes = request_json.get("contaminantes")
    for alimento in alimentos:
        reporte[alimento] = []
        for contaminante in contaminantes: 
            cur.execute("SELECT AVG(p.peso), AVG(consumo.cantidad) FROM (SELECT * FROM persona WHERE sexo=%s AND edad > %s AND edad < %s AND peso > %s AND peso < %s AND altura > %s AND altura < %s) AS p LEFT JOIN consumo ON p.id_folio=consumo.id_folio LEFT JOIN alimento ON consumo.id_alimento=alimento.id_alimento WHERE alimento.especie=%s",[sexo,min_edad,max_edad,min_peso,max_peso,min_altura,max_altura,alimento])
            avgs = cur.fetchall()
            peso_promedio = avgs[0][0]
            consumo_promedio = avgs[0][0]
            print("["+ alimento +"]["+ contaminante + "]")
            reporte[alimento][contaminante] = consumo_promedio
    return jsonify(reporte)