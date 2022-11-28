from __main__ import app, mysql, jsonify, request

@app.route("/alimentos", methods=["GET", "POST"])
def alimentos():
    lista_alimentos = []
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT especie FROM alimento")
        #consulta
        _alimentos = cur.fetchall()
        for alimento in _alimentos:
            lista_alimentos.append(alimento[0])
        
    else:
        dict_alimentos = {}
        request_json = request.get_json()
        contaminantes = []
        if(request_json.get("contaminantes").size != 0):
            for contaminante in request_json.get("contaminantes"):
                contaminantes.append(contaminante)
        for contaminante in contaminantes:
            cur = mysql.connection.cursor()
            cur.execute("SELECT especie FROM alimento LEFT JOIN muestreo WHERE nombre = %s AND cantidad != 0",[contaminante])
            _alimentos = cur.fetchall()
            for alimento in _alimentos:
                dict_alimentos[alimento[0]] = True

        lista_alimentos = dict_alimentos.keys

    return jsonify(lista_alimentos)
