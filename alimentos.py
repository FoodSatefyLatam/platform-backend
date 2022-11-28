from __main__ import app, mysql, jsonify, request

@app.route("/alimentos", methods=["GET", "POST"])
def alimentos():
    cur = mysql.connection.cursor()
    lista_alimentos = []
    if request.method == 'GET':
        cur.execute("SELECT especie FROM alimento")
        #consulta
        _alimentos = cur.fetchall()
        for alimento in _alimentos:
            lista_alimentos.append(alimento[0])
        
    else:
        dict_alimentos = {}
        request_json = request.get_json()
        contaminantes = []
        if(request_json.get("contaminantes")):
            for contaminante in request_json.get("contaminantes"):
                contaminantes.append(contaminante)
            print(contaminantes)
            for contaminante in contaminantes:
                cur = mysql.connection.cursor()
                cur.execute("SELECT especie FROM alimento LEFT JOIN muestreo ON alimento.id_alimento=muestreo.id_alimento LEFT JOIN contaminante ON contaminante.id_contaminante=muestreo.id_contaminante WHERE contaminante.nombre = %s AND muestreo.cantidad != 0",[contaminante])
                _alimentos = cur.fetchall()
                for alimento in _alimentos:
                    dict_alimentos[alimento[0]] = True
            for alimento in dict_alimentos.keys():
                lista_alimentos.append(alimento)
    return jsonify(lista_alimentos)
