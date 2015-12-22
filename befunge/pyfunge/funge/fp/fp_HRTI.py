from funge.fingerprint import Fingerprint

import time

class HRTI(Fingerprint):
    'High-Resolution Timer Interface'

    API = 'PyFunge v2'
    ID = 0x48525449

    def init(self, ip):
        Fingerprint.init(self, ip)

        try:
            self.resolution = ip.program.HRTI_resolution
        except AttributeError:
            # determine clock resolution by calculating GCD of differences.
            curtime = time.time
            result = None
            for step in xrange(100):
                stamp = curtime()
                while stamp == curtime(): pass
                stamp = int((curtime() - stamp) * 1000000) or 1
                if result is None:
                    result = stamp
                else:
                    while stamp:
                        result, stamp = stamp, result % stamp
            self.resolution = ip.program.HRTI_resolution = result

        self.clock = None

    @Fingerprint.register('E')
    def granularity(self, ip):
        self.clock = None

    @Fingerprint.register('G')
    def mark(self, ip):
        ip.push(self.resolution)

    @Fingerprint.register('M')
    def timer(self, ip):
        self.clock = time.clock()

    @Fingerprint.register('S')
    def erase_mark(self, ip):
        ip.push(int((time.time() % 1.) * 1000000 + .5))

    @Fingerprint.register('T')
    def second(self, ip):
        if self.clock is None:
            self.reflect(ip)
        else:
            ip.push(int((time.clock() - self.clock) * 1000000 + .5))

