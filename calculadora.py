from __main__ import app, mysql, request, jsonify

@app.route("/calculadora", methods = ['POST'])
def calculadora():
    contaminante = "Cd"
    weight = 0
    amount = 0
    food = ""
    try:
        request_json = request.get_json()
        if(request_json.get("weight")):
            weight = request_json["weight"]
        if(request_json.get("amount")):
            amount = request_json["amount"]
        if(request_json.get("food")):
            food = request_json["food"]
        if(request_json.get("contaminante")):
            contaminante = request_json["contaminante"]
        amount /= 1000.0
    except:
        return "Error"

    
    #aqui saca los datos del contaminante
    cur = mysql.connection.cursor()
    cur.execute("SELECT limite_diario FROM Contaminante WHERE nombre= %s",[contaminante]) #de momento se trabaja con el cadmio
    #los valores de referencia están en microgramos
    valor_referencia = cur.fetchone()
    if(valor_referencia[0] is None):
        valor_referencia = 0.0
    else:
        valor_referencia = valor_referencia[0]
    print(valor_referencia)
    cur.execute("SELECT id FROM Contaminante WHERE nombre= %s",[contaminante])
    id_contaminante = cur.fetchone()
    cur.execute("SELECT id FROM Alimento WHERE nombre=%s",[food]) 
    id_alimento=cur.fetchone()
    cur.execute("SELECT Avg(cantidad)  FROM  Muestra WHERE id_contaminante=%s AND id_alimento=%s" ,([id_contaminante],[id_alimento]))
    promedio=cur.fetchone()
    if(promedio[0] is None):
        promedio = 0.0
    else:
        promedio = promedio[0]
    print(promedio)
    formula = 0.0
    if(valor_referencia != 0 and weight != 0):
        formula = (float(amount) * float(promedio))/(float(valor_referencia) * float(weight)) #amount es la cantidad de alimento y weight el peso de la persona
    if(formula < 1.0):
        return jsonify({'estado': 'bien', 'formula': formula, 'contaminantes_promedio': promedio})
    else:
        return jsonify({'estado': 'mal', 'formula': formula, 'contaminantes_promedio': promedio})