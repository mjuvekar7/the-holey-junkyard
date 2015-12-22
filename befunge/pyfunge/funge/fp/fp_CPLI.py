from funge.fingerprint import Fingerprint

class CPLI(Fingerprint):
    'Complex Integer extension'

    API = 'PyFunge v2'
    ID = 0x43504c49

    @Fingerprint.register('A')
    def add(self, ip):
        d, c, b, a = ip.popmany(4)
        ip.push(a + c)
        ip.push(b + d)

    @Fingerprint.register('D')
    def divide(self, ip):
        d, c, b, a = ip.popmany(4)
        if c == d == 0:
            self.reflect(ip)
        else:
            divisor = c * c + d * d
            ip.push(int(round(float(a * c + b * d) / divisor)))
            ip.push(int(round(float(b * c - a * d) / divisor)))

    @Fingerprint.register('M')
    def multiply(self, ip):
        d, c, b, a = ip.popmany(4)
        ip.push(a * c - b * d)
        ip.push(a * d + b * c)

    @Fingerprint.register('O')
    def output(self, ip):
        b, a = ip.popmany(2)
        self.platform.putstr('(%d%+di)' % (a, b))

    @Fingerprint.register('S')
    def subtract(self, ip):
        d, c, b, a = ip.popmany(4)
        ip.push(a - c)
        ip.push(b - d)

    @Fingerprint.register('V')
    def absolute_value(self, ip):
        a, b = ip.popmany(2)
        ip.push(a * a + b * b)

