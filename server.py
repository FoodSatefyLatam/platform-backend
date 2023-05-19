import os
from logging import debug

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL

import alimentos
#import calculadora
import contaminantes
#import reporte

load_dotenv('.env')

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = os.environ.get('DB_HOST')
app.config['MYSQL_USER'] = os.environ.get('DB_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASS')
app.config['MYSQL_DB'] = os.environ.get('DB_NAME')
mysql = MySQL(app)

if __name__ == "__main__":
    app.run(port=5001,  host='0.0.0.0', debug=True, threaded=True)
