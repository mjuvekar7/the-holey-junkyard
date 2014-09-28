import RPi.GPIO as gpio
global outs
outs = []

def disp_init(out0, out1, out2, out3):
    global outs
    gpio.cleanup()
    gpio.setmode(gpio.BOARD)
    outs.append(out0)
    outs.append(out1)
    outs.append(out2)
    outs.append(out3)
    for out in outs:
        gpio.setup(out, gpio.OUT)

def display(num):
    if num < 0 or num > 9:
        print('Enter a number between 0 and 9!')
        return
    global outs
    for i in range(0, len(outs)):
        gpio.output(outs[i], num & pow(2, i))
