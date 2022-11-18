from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'benjaminF'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'proyectocontaminantes'
mysql = MySQL(app)

import alimentos,calculadora
@app.route("/request_db", methods=["POST"])
def request_db():
    min_age = 0
    max_age = 120
    try:
        request_json = request.get_json()
        if request_json.get("min_age"):
            min_age = request_json["min_age"]
        if request_json.get("max_age"):
            max_age = request_json["max_age"]

        try:
            print("consulta")
            return str(min_age) + " "+ str(max_age)
        except:
            return "db error"
    except:
        return "request error"

if __name__ == "__main__":
    app.run(debug=True)



