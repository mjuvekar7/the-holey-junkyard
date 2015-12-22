from funge.fingerprint import Fingerprint

import os

# XXX should mark as unsafe
class DIRF(Fingerprint):
    'Directory functions extension'

    API = 'PyFunge v2'
    ID = 0x44495246

    @Fingerprint.register('C')
    def command67(self, ip):
        dirname = ip.pop_string()
        try:
            os.chdir(dirname)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('M')
    def command77(self, ip):
        dirname = ip.pop_string()
        try:
            os.mkdir(dirname)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('R')
    def command82(self, ip):
        dirname = ip.pop_string()
        try:
            os.rmdir(dirname)
        except Exception:
            self.reflect(ip)

