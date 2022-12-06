from __main__ import app, mysql, request, jsonify

@app.route("/contaminantes", methods=["GET", "POST"])
def alimentos():
    cur = mysql.connection.cursor()
    lista_contaminantes = []
    if request.method == 'GET':
        cur.execute("SELECT nombre FROM contaminante")
        contaminantes = cur.fetchall()
        for contaminante in contaminantes:
            lista_contaminantes.append(contaminante[0])
        
    lista_contaminantes.sort()
    return jsonify(lista_contaminantes)