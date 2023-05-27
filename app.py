#!/usr/bin/python
import sqlite3
import serial
from datetime import datetime
from flask import Flask, render_template
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
    cursor.execute("CREATE TABLE if not exists data_meteo (temp text, humi text, light text, date_time text)")
    date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    data = ser.readline().decode('utf-8').rstrip()
    line = data.replace('\n', '').split(':')
    print("T = ", line[0], " H = ", line[1], " L = ", line[2], " TIME = ", date_time)
    cursor.execute("INSERT INTO data_meteo VALUES (?, ?, ?, ?)", (line[0], line[1], line[2], date_time))
    conn.commit()
    print("get_data: OK")
    templateData = {
        'temperature' : line[0],
        'humidity' : line[1],
        'light' : line[2],
        'date_time' : date_time
    }
    conn.close()
    return render_template("sensor.html", **templateData)

@app.route("/survey")
def survey():
    dat_temp = []
    dat_humi = []
    dat_light = []
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
    cursor.execute("SELECT light FROM data_meteo")
    rows2 = cursor.fetchall()
    for row2 in rows2:
        dat_light.append(row2[0])
    cursor.execute("SELECT date_time FROM data_meteo")
    rows3 = cursor.fetchall()
    for row3 in rows3:
        dat_time.append(row3[0])
    count_dat = len(dat_time)
    dat_all = list(zip(dat_temp, dat_humi, dat_light, dat_time))
    conn.close()
    return render_template("survey.html", list_data = dat_all)

@app.route("/graph")
def graph():
    dat_temp = []
    dat_humi = []
    dat_light = []
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
    cursor.execute("SELECT light FROM data_meteo")
    rows2 = cursor.fetchall()
    for row2 in rows2:
        dat_light.append(row2[0])
    cursor.execute("SELECT date_time FROM data_meteo")
    rows3 = cursor.fetchall()
    for row3 in rows3:
        dat_time.append(row3[0])
    conn.close()
    
    x = dat_time
    y = dat_temp
    z = dat_humi
    w = dat_light
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.xlabel("Даты")    
    plt.ylabel("Температура, влажность, освещенность")
    plt.grid()

    ax.plot(x, z, label="Влажность")
    ax.plot(x, y, label="Температура")
    ax.plot(x, w, label="Освещенность")
    plt.legend()
    xax = ax.xaxis
    xlabels = xax.get_ticklabels()
    for label in xlabels:
        label.set_rotation(15)
        label.set_fontsize(8)
    fig.savefig('static/graph.png')
    return render_template("graph.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")