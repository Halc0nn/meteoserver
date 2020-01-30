#!/usr/bin/python
import sqlite3
import Adafruit_DHT
import time
from datetime import datetime, date
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/sensor")
def sensor():
    conn = sqlite3.connect("meteodatabase.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE if not exists data_meteo (humi text, temp text, date_time text)")
    humidity,temperature = Adafruit_DHT.read_retry(11, 4)
    date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor.execute("INSERT INTO data_meteo VALUES (?, ?, ?)", (humidity, temperature, date_time))
    conn.commit()
    print(humidity, temperature, date_time)
    print("get_data: OK")
    templateData = {
        'temperature' : temperature,
        'humidity' : humidity
    }
    conn.close()
    return render_template("sensor.html", **templateData)

@app.route("/survey")
def survey():
    conn = sqlite3.connect("meteodatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temp FROM data_meteo")
    rows = cursor.fetchall()
    dat_temp = []
    dat_humi = []
    dat_time = []
    for row in rows:
        dat_temp.append(row)
    print(dat_temp)
    cursor.execute("SELECT humi FROM data_meteo")
    rows1 = cursor.fetchall()
    for row1 in rows1:
        dat_humi.append(row1)
    print(dat_humi)
    cursor.execute("SELECT date_time FROM data_meteo")
    rows2 = cursor.fetchall()
    for row2 in rows2:
        dat_time.append(row2)
    print(dat_time)
    conn.close()
    return render_template("survey.html", list_data_temp = dat_temp, list_data_humi = dat_humi, list_data_time = dat_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
