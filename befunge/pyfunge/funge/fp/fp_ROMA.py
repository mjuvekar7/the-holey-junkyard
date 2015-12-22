from funge.fingerprint import Fingerprint

class ROMA(Fingerprint):
    'Funge-98 Roman Numerals'

    API = 'PyFunge v2'
    ID = 0x524f4d41

    @Fingerprint.register('I')
    def push_1(self, ip): ip.push(1)
    @Fingerprint.register('V')
    def push_5(self, ip): ip.push(5)
    @Fingerprint.register('X')
    def push_10(self, ip): ip.push(10)
    @Fingerprint.register('L')
    def push_50(self, ip): ip.push(50)
    @Fingerprint.register('C')
    def push_100(self, ip): ip.push(100)
    @Fingerprint.register('D')
    def push_500(self, ip): ip.push(500)
    @Fingerprint.register('M')
    def push_1000(self, ip): ip.push(1000)

