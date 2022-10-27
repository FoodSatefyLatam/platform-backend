
@app.route("/calculadora", methods = ["POST"])
def calculadora():
    try:
        weight = 0
        amount = 0
        food = " "   
        request_json = request.get_json()
        if(request_json.get("weight")):
            weight = request_json["weight"]
        if(request_json.get("amount")):
            amount = request_json["amount"]
        if(request_json.get("food")):
            food = request_json["food"]

    except:
        print("request error")

    #aqui saca las weas del contaminante
    cur = mysql.connection.cursor()
    cur.execute("")
    formula = (amount * contaminate)/(valor_referencia * weight)    

        