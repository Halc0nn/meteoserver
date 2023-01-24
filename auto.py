#!/usr/bin/python

import sqlite3
import Adafruit_DHT
import time
from datetime import datetime, date

conn = sqlite3.connect("meteodatabase.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE if not exists data_meteo (humi text, temp text, date_time text)")

def get_data():
    humidity,temperature = Adafruit_DHT.read_retry(11, 4)
    date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor.execute("""INSERT INTO data_meteo VALUES (?, ?, ?)""", (humidity, temperature, date_time))
    conn.commit()
    print(humidity,temperature, date_time)
    print("get_data: OK")

while(True):
    get_data()
    time.sleep(5)
