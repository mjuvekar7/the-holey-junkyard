#!/usr/bin/python
# listen.py: listen for claps
# author Shardul C.

import alsaaudio as aa
import audioop

if __name__ == '__main__':
    inp = aa.PCM(aa.PCM_CAPTURE, device='plughw:1')
    inp.setchannels(2)
    inp.setrate(8000)
    inp.setformat(aa.PCM_FORMAT_S16_LE)
    inp.setperoidsize(160)

    while True:
        l, data = inp.read()
        print(audioop.max(data, 2))

