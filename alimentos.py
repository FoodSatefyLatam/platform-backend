from flask import jsonify

from __main__ import app, mysql

@app.route("/request_alimentos")
def request_alimentos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT especie FROM alimento")
    #consulta
    alimentos = cur.fetchall()
    return 'hola mundo'