from __main__ import app, mysql, request

@app.route("/reporte", methods=["POST"])
def reporte():
    sexo = 0
    min_age = 0
    max_age = 1000
    min_peso = 0
    max_peso = 1000
    min_altura = 0
    max_altura = 1000
    contaminantes = []
    alimentos = []
    try:
        request_json = request.get_json()
        if request_json.get("min_age"):
            min_age = request_json["min_age"]
        if request_json.get("max_age"):
            max_age = request_json["max_age"]
        
    except:
        return "Error"
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT valor_referencia FROM contaminante WHERE nombre= %s",[contaminante])