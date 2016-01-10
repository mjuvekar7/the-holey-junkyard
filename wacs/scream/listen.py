import pyaudio

chunk = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
threshold = 3000
max_value = 0
p = pyaudio.PyAudio()

def listen():
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, output=True, frames_per_buffer=chunk)
    while True:
        if max(array('h', stream.read(chunk))) > threshold:
            print('clap')
