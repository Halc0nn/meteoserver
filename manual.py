#!/usr/bin/python

import sqlite3
import Adafruit_DHT
import time
from datetime import datetime, date
from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Expires'] = '0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

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
    dat_temp = []
    dat_humi = []
    dat_time = []
    conn = sqlite3.connect("meteodatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temp FROM data_meteo")
    rows = cursor.fetchall()
    for row in rows:
        dat_temp.append(row[0])
    cursor.execute("SELECT humi FROM data_meteo")
    rows1 = cursor.fetchall()
    for row1 in rows1:
        dat_humi.append(row1[0])
    cursor.execute("SELECT date_time FROM data_meteo")
    rows2 = cursor.fetchall()
    for row2 in rows2:
        dat_time.append(row2[0])
    count_dat = len(dat_time)
    dat_all = list(zip(dat_time, dat_temp, dat_humi))
    conn.close()
    return render_template("survey.html", list_data = dat_all)

@app.route("/graph")
def graph():
    dat_temp = []
    dat_humi = []
    dat_time = []
    conn = sqlite3.connect("meteodatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temp FROM data_meteo")
    rows = cursor.fetchall()
    for row in rows:
        dat_temp.append(row[0])
    cursor.execute("SELECT humi FROM data_meteo")
    rows1 = cursor.fetchall()
    for row1 in rows1:
        dat_humi.append(row1[0])
    cursor.execute("SELECT date_time FROM data_meteo")
    rows2 = cursor.fetchall()
    for row2 in rows2:
        dat_time.append(row2[0])
    conn.close()
    
    x = dat_time
    y = dat_temp
    z = dat_humi
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.xlabel("Даты")    
    plt.ylabel("Температура и влажность")
    plt.grid()

    ax.plot(x, z, label="Влажность")
    ax.plot(x, y, label="Температура")
    plt.legend()
    xax = ax.xaxis
    xlabels = xax.get_ticklabels()
    for label in xlabels:
        label.set_rotation(15)
        label.set_fontsize(8)
    fig.savefig('static/graph.png')
    return render_template("graph.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
