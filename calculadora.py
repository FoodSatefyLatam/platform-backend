from __main__ import app, mysql,request



@app.route("/calculadora")
def calculadora():
    try:
    
        weight = 0
        amount = 0
        food = "" 
        request_json = request.get_json()
        if(request_json.get("weight")):
            weight = request_json["weight"]
        if(request_json.get("amount")):
            amount = request_json["amount"]
        if(request_json.get("food")):
            food = request_json["food"]
    
    except:
        print("request error")

    #aqui saca los datos del contaminante
    contaminante="Cd"
    cur = mysql.connection.cursor()
    cur.execute("SELECT valor_referencia FROM contaminante WHERE nombre= %s",[contaminante]) #de momento se trabaja con el cadmio
    valor_referencia = cur.fetchone()
    cur.execute("SELECT id_contaminante FROM contaminante WHERE nombre= %s",[contaminante])
    id_contaminante=cur.fetchone()
    alimento="albacora"
    cur.execute("SELECT id_alimento FROM alimento WHERE especie=%s",[alimento]) #para probar se uso la albacora
    id_alimento=cur.fetchone()
    cur.execute("SELECT Avg(cantidad)  FROM  muestreo WHERE id_contaminante=%s AND id_alimento=%s" ,([id_contaminante],[id_alimento]))
    promedio=cur.fetchone()
    print (promedio[0])
    print (valor_referencia[0])
    formula = (11 * float(promedio[0]))/(float(valor_referencia[0]) * 70)
    if formula < 1.0:
        return "Dentro de lo normal"
    else:
        return "Dañino para la salud"

        