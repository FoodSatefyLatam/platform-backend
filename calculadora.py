
@app.route("/calculadora", methods = ["POST"])
def calculadora():
    try:
    weight = 0
    height = 0
    food = " "   
        request_json = request.get_json()
        if(request_json.get("weight"))
            weight = request_json["weight"]
        if(request_json.get("height"))
            height = request_json["height"]
        if(request_json.get("food"))
            food = request_json["food"]

        