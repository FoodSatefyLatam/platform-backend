import os

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

import alimentos
#import calculadora
import contaminantes
#import reporte

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grupo1'
app.config['MYSQL_PASSWORD'] = 'gq0xf7vk'
app.config['MYSQL_DB'] = 'grupo1'

if __name__ == "__main__":
    app.run(port = '5001',  host= '0.0.0.0', debug=True, threaded=True)
