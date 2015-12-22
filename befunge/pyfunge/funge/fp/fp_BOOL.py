from funge.fingerprint import Fingerprint

class BOOL(Fingerprint):
    'Logic functions'

    API = 'PyFunge v2'
    ID = 0x424F4F4C

    @Fingerprint.register('A')
    def bitwise_and(self, ip):
        b, a = ip.popmany(2)
        ip.push(a & b)

    @Fingerprint.register('N')
    def bitwise_not(self, ip):
        ip.push(~ip.pop())

    @Fingerprint.register('O')
    def bitwise_or(self, ip):
        b, a = ip.popmany(2)
        ip.push(a | b)

    @Fingerprint.register('X')
    def bitwise_xor(self, ip):
        b, a = ip.popmany(2)
        ip.push(a ^ b)

