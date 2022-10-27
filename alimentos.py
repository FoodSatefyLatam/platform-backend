from flask import jsonify

@app.route("/request_alimentos")
def request_db():
    sql_request_alimetos = "SELECT especie FROM Alimetos"
    #consulta
    alimentos = fetchall()
    return jsonify("alimentos:" + alimentos)