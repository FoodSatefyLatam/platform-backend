from flask import jsonify

from __main__ import app, mysql

@app.route("/request_alimentos")
def request_alimentos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT especie FROM alimento")
    #consulta
    lista_alimentos = []
    alimentos = cur.fetchall()
    for alimento in alimentos:
        lista_alimentos.append(alimento[0])
    return jsonify(lista_alimentos)