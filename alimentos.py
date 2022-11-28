from flask import jsonify

from __main__ import app, mysql

@app.route("/alimentos")
def alimentos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT especie FROM alimento")
    #consulta
    lista_alimentos = []
    _alimentos = cur.fetchall()
    for alimento in _alimentos:
        lista_alimentos.append(alimento[0])
    return jsonify(lista_alimentos)