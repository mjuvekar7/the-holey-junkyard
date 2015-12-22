from funge.fingerprint import Fingerprint
from funge.fp.fp_LONG import pop_long
from funge.fp.fp_FPSP import pop_float
from funge.fp.fp_FPDP import pop_double

import struct

class FPRT(Fingerprint):
    'Formatted print'

    API = 'PyFunge v2'
    ID = 0x46505254

    @Fingerprint.register('D')
    def format_double_fp(self, ip):
        num = pop_double(ip)
        format = ip.pop_string()
        try:
            ip.push_string(format % (num,))
        except (TypeError, KeyError):
            self.reflect(ip)

    @Fingerprint.register('F')
    def format_fp(self, ip):
        num = pop_float(ip)
        format = ip.pop_string()
        try:
            ip.push_string(format % (num,))
        except (TypeError, KeyError):
            self.reflect(ip)

    @Fingerprint.register('I')
    def format_int(self, ip):
        num = ip.pop()
        format = ip.pop_string()
        try:
            ip.push_string(format % (num,))
        except (TypeError, KeyError):
            self.reflect(ip)

    @Fingerprint.register('L')
    def format_long_int(self, ip):
        num = pop_long(ip)
        format = ip.pop_string()
        try:
            ip.push_string(format % (num,))
        except (TypeError, KeyError):
            self.reflect(ip)

    @Fingerprint.register('S')
    def format_str(self, ip):
        str = ip.pop_string()
        format = ip.pop_string()
        try:
            ip.push_string(format % (str,))
        except (TypeError, KeyError):
            self.reflect(ip)

