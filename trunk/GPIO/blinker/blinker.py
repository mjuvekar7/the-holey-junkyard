import RPi.GPIO as gpio
import time

def blink(out, delay):
    gpio.setmode(gpio.BOARD)
    gpio.setup(out, gpio.OUT)
    while True:
        gpio.output(out, 1)
        time.sleep(delay)
        gpio.output(out, 0)
        time.sleep(delay)

def blink_alt(out0, out1, delay):
    gpio.setmode(gpio.BOARD)
    gpio.setup(out0, gpio.OUT)
    gpio.setup(out1, gpio.OUT)

    while True:
        gpio.output(out0, 1)
        gpio.output(out1, 0)
        time.sleep(delay)
        gpio.output(out0, 0)
        gpio.output(out1, 1)
        time.sleep(delay)

