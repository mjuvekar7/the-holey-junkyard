import RPi.GPIO as GPIO
import time

def blink(out, delay):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(out, GPIO.OUT)
    while True:
        GPIO.output(out, 1)
        time.sleep(delay)
        GPIO.output(out, 0)
        time.sleep(delay)

