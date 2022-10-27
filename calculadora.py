from __main__ import app, mysql


@app.route("/calculadora", methods = ["POST"])
def calculadora():
    try:
        weight = 0
        amount = 0
        food = "" 
        contaminante= ""  
        request_json = request.get_json()
        if(request_json.get("weight")):
            weight = request_json["weight"]
        if(request_json.get("amount")):
            amount = request_json["amount"]
        if(request_json.get("food")):
            food = request_json["food"]
        if(request_json.get("contaminante")):
            contaminante = request_json["contaminante"]

    except:
        print("request error")

    #aqui saca las weas del contaminante
    cur = mysql.connection.cursor()
    cur.execute("SELECT valor_referencia FROM contaminante WHERE nombre=%s",contaminante)
    valor_referencia = cur.fetchone()[0][0]
    cur.execute("SELECT id_contaminante FROM contaminante WHERE nombre=%s",contaminante)
    id_contaminante=cur.fetchone()[0][0]
    cur.execute("SELECT id_alimento FROM alimento WHERE nombre=%s",food)
    id_alimento=cur.fetchone()[0][0]
    cur.execute("SELECT Avg(cantidad)  FROM  muestreo WHERE id_contaminante=%s AND id_alimento=%s" ,id_contaminante,id_alimento)
    promedio=cur.fetchone()[0][0]
    formula = (amount * promedio)/(valor_referencia * weight)
    return formula

        