#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import uinput #sudo pip install python-uinput ; sudo modprobe uinput
from os import system

channel = 26
quit_game = False

def setup():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def shutdown():
    events = (uinput.KEY_F4,)
    device = uinput.Device(events)
    device.emit(uinput.KEY_F4, 1)
    quit_game = True
    print("\033[31;4mLe système va s'éteindre !\033[0m\n")
    if GPIO.wait_for_edge(channel, GPIO.RISING, bouncetime = 2000, timeout = 30000) is None:
        print("vraiment")
        #system("sudo shutdown -h now")
    else:
        shutdown_cancelled()

def shutdown_cancelled():
    quit_game = False
    print("Arrêt annulé !")
    #system("sudo shutdown -c")

def loop():
    if GPIO.wait_for_edge(channel, GPIO.RISING, bouncetime = 2000):
        shutdown()

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
