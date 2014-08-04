import RPi.GPIO as GPIO
import time

def blink_alt(out0, out1, delay):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out0, GPIO.OUT)
    GPIO.setup(out1, GPIO.OUT)

    while True:
        GPIO.output(out0, 1)
        GPIO.output(out1, 0)
        time.sleep(delay)
        GPIO.output(out0, 0)
        GPIO.output(out1, 1)
        time.sleep(delay)

