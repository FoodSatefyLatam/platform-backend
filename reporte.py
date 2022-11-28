from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["POST"])
def reporte():
    if request.method != "POST":
        return "error"
    reporte = {}
    cur = mysql.connection.cursor()
    contaminantes = []
    alimentos = []
    request_json = request.get_json()
    sexo = request_json["sexo"]
    min_edad = request_json["min_edad"]
    max_edad = request_json["max_edad"]
    min_peso = request_json["min_peso"]
    max_peso = request_json["max_peso"]
    min_altura = request_json["min_altura"]
    max_altura = request_json["max_altura"]
    for contaminante in request_json.get("contaminantes"):
        contaminantes.append(contaminante)
    for alimento in request_json.get("alimentos"):
        alimentos.append(alimento)
    for contaminante in contaminantes:
        #MySQLdb.ProgrammingError: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'JOIN consumo ON persona.id_folio=consumo.id_folio JOIN alimento ON consumo.id_al' at line 1")
        cur.execute("SELECT * FROM (SELECT * FROM persona WHERE sexo=%s AND edad > %s AND edad < %s AND peso > %s AND peso < %s AND altura > %s AND altura < %s) AS p LEFT JOIN consumo ON p.id_folio=consumo.id_folio LEFT JOIN alimento ON consumo.id_alimento=alimento.id_alimento LEFT JOIN muestreo ON p.id_region=muestreo.id_region LEFT JOIN contaminante ON contaminante.id_contaminante=muestreo.id_contaminante WHERE contaminante.nombre = %s",[sexo,min_edad,max_edad,min_peso,max_peso,min_altura,max_altura,contaminante])
        reporte[contaminante] = cur.fetchall()
    return reporte