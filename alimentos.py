from __main__ import app, mysql, jsonify, request

@app.route("/alimentos", methods=["GET", "POST"])
def alimentos():
    cur = mysql.connection.cursor()
    lista_alimentos = []
    if request.method == 'GET':
        cur.execute("SELECT nombre FROM Alimento")
        #consulta
        _alimentos = cur.fetchall()
        for alimento in _alimentos:
            lista_alimentos.append(alimento[0])
        
    else:
        dict_alimentos = {}
        request_json = request.get_json()
        contaminantes = []
        if request_json.get("contaminantes"):
            for contaminante in request_json.get("contaminantes"):
                contaminantes.append(contaminante)
            for contaminante in contaminantes:
                cur = mysql.connection.cursor()
                cur.execute("SELECT Alimento.nombre FROM Alimento LEFT JOIN Muestra ON Alimento.id=Muestra.id_alimento LEFT JOIN Contaminante ON Contaminante.id=Muestra.id_contaminante WHERE Contaminante.nombre = %s AND Muesta.cantidad != 0",[contaminante])
                _alimentos = cur.fetchall()
                for alimento in _alimentos:
                    dict_alimentos[alimento[0]] = True
            for alimento in dict_alimentos.keys():
                lista_alimentos.append(alimento)
    lista_alimentos.sort()
    return jsonify(lista_alimentos)
