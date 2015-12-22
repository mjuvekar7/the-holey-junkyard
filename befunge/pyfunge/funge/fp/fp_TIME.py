from funge.fingerprint import Fingerprint

import time

class TIME(Fingerprint):
    'Time and Date functions'

    API = 'PyFunge v2'
    ID = 0x54494D45

    def init(self, ip):
        Fingerprint.init(self, ip)
        self.gmtmode = False

    def gettime(self):
        if self.gmtmode:
            return time.gmtime()
        else:
            return time.localtime()

    @Fingerprint.register('D')
    def day(self, ip):
        ip.push(self.gettime().tm_mday)

    @Fingerprint.register('F')
    def day_of_year(self, ip):
        ip.push(self.gettime().tm_yday - 1)

    @Fingerprint.register('G')
    def set_gmtmode(self, ip):
        self.gmtmode = True

    @Fingerprint.register('H')
    def hour(self, ip):
        ip.push(self.gettime().tm_hour)

    @Fingerprint.register('L')
    def set_localmode(self, ip):
        self.gmtmode = False

    @Fingerprint.register('M')
    def minute(self, ip):
        ip.push(self.gettime().tm_min)

    @Fingerprint.register('O')
    def month(self, ip):
        ip.push(self.gettime().tm_mon)

    @Fingerprint.register('S')
    def second(self, ip):
        ip.push(self.gettime().tm_sec)

    @Fingerprint.register('W')
    def day_of_weey(self, ip):
        ip.push((2,3,4,5,6,7,1)[self.gettime().tm_wday])

    @Fingerprint.register('Y')
    def year(self, ip):
        ip.push(self.gettime().tm_year)

