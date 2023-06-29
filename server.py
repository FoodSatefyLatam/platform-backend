from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def print_date_time():
    dir_list = os.listdir("data")
    for file in dir_list:
        file = file[:-5]
        print(file)
    


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=86400)
scheduler.start()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'grupo1'
app.config['MYSQL_PASSWORD'] = 'gq0xf7vk'
app.config['MYSQL_DB'] = 'grupo1'

mysql = MySQL(app)

import alimentos, calculadora, reporte, contaminantes

if __name__ == "__main__":
    app.run(port = '5001',  host= '0.0.0.0', debug=True, threaded=True)