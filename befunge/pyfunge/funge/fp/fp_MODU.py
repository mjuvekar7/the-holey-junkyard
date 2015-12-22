from funge.fingerprint import Fingerprint

class MODU(Fingerprint):
    'Modulo Arithmetic Extension'

    API = 'PyFunge v2'
    ID = 0x4d4f4455

    @Fingerprint.register('M')
    def signed_modulo(self, ip):
        b, a = ip.popmany(2)
        if b:
            ip.push(a % b)
        else:
            ip.push(0)

    @Fingerprint.register('R')
    def unsigned_modulo(self, ip):
        b, a = ip.popmany(2)
        if b == 0:
            ip.push(0)
        elif a < 0:
            ip.push(-(abs(a) % abs(b)))
        else:
            ip.push(abs(a) % abs(b))

    @Fingerprint.register('U')
    def c_modulo(self, ip):
        b, a = ip.popmany(2)
        if b:
            ip.push(abs(a) % abs(b))
        else:
            ip.push(0)

