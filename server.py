from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'contaminantes'

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