from __main__ import app, mysql, request, jsonify

@app.route("/contaminantes", methods=["GET", "POST"])
def contaminantes():
    cur = mysql.connection.cursor()
    lista_contaminantes = []
    if request.method == 'GET':
        cur.execute("SELECT nombre, alias FROM Contaminante")
        contaminantes = cur.fetchall()
        for contaminante in contaminantes:
            lista_contaminantes.append({"nombre":contaminante[0],"alias": contaminante[1]})
    return jsonify(lista_contaminantes)