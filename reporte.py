from __main__ import app, mysql, request, jsonify

@app.route("/reporte", methods=["POST"])
def reporte():
    if request.method != "POST":
        return "error"
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
    if request_json.get("contaminantes"):
        for contaminante in request_json.get("contaminantes"):
            contaminantes.append(contaminante)
    if request_json.get("alimentos"):
        for alimento in request_json.get("alimentos"):
            alimentos.append(alimento)
    for contaminante in contaminantes:
        print(contaminante)
        #MySQLdb.ProgrammingError: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'JOIN consumo ON persona.id_folio=consumo.id_folio JOIN alimento ON consumo.id_al' at line 1")
        cur.execute("SELECT * FROM (SELECT * FROM persona WHERE sexo=%s AND edad > %s AND edad < %s AND peso > %s AND peso < %s AND altura > %s AND altura < %s) AS persona JOIN consumo ON persona.id_folio=consumo.id_folio JOIN alimento ON consumo.id_alimento=alimento.id_alimento JOIN muestreo ON persona.id_region=muestreo.id_region JOIN contaminante ON contaminante.id_contaminante=muestreo.id_contaminante WHERE contaminante.nombre = %s",[sexo,min_edad,max_edad,min_peso,max_peso,min_altura,max_altura,contaminante])
        print(contaminante)
        reporte[contaminante] = cur.fetchall()
        print(reporte)
    print("hola")
    return reporte