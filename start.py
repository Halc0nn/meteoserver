#!/usr/bin/python

import time
import RPi.GPIO as GPIO
import subprocess
GPIO.setmode(GPIO.BCM)
start_pin = 24
GPIO.setup(start_pin, GPIO.IN)
current_state = 0
index_edit = 1

command_f0 = "python3 /home/pi/meteo/auto.py"
command_f1 = "python3 /home/pi/meteo/manual.py"

proc_f0 = subprocess.Popen(command_f0, shell=True) 
proc_f1 = subprocess.Popen(command_f1, shell=True) 

while True:
    current_input = GPIO.input(start_pin)
    if current_input != current_state:
        current_state = current_input
        index_edit = 1
    print(current_input)
    if index_edit == 1:
        if current_input == 0:
            print("f0")
            proc_f1.kill()
            proc_f0 = subprocess.Popen(command_f0, shell=True) 
        if current_input == 1:
            print("f1")
            proc_f0.kill()
            proc_f1 = subprocess.Popen(command_f1, shell=True) 
        index_edit = 0
    time.sleep(1)
