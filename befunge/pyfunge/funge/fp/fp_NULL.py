from funge.fingerprint import Fingerprint

class NULL(Fingerprint):
    'Funge-98 Null Fingerprint'

    API = 'PyFunge v2'
    ID = 0x4e554c4c

    @Fingerprint.register('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    def commands(self, ip):
        self.reflect(ip)

