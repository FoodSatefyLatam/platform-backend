from __main__ import app, mysql, request

@app.route("/reporte", methods=["POST"])
def request_db():
    min_age = 0
    max_age = 140
    try:
        request_json = request.get_json()
        if request_json.get("min_age"):
            min_age = request_json["min_age"]
        if request_json.get("max_age"):
            max_age = request_json["max_age"]
        
        
    except:
        return "request error"