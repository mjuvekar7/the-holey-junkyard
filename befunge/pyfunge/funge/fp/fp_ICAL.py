from funge.fingerprint import Fingerprint

def getsize(value):
    # do operation with 2^(2^k) bits, where k >= 4 is minimum size for a
    size = 15
    while value >> size != 0 and value >> size != -1:
        size = size * 2 + 1
    return size

class ICAL(Fingerprint):
    'Some Intercal-like functions'

    API = 'PyFunge v2'
    ID = 0x4943414c

    def init(self, ip):
        Fingerprint.init(self, ip)
        self.addrstack = []

    @Fingerprint.register('A')
    def unary_and(self, ip):
        a = ip.pop()
        ip.push(a & ((a >> 1) | ((a & 1) << getsize(a))))

    @Fingerprint.register('F')
    def forget(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        else:
            del self.addrstack[-n:]

    @Fingerprint.register('I')
    def interleave(self, ip):
        b, a = ip.popmany(2)
        result = 0
        shift = 0
        while a or b:
            result |= (((a & 1) << 1) | (b & 1)) << shift
            shift += 2
            a >>= 1
            b >>= 1
        ip.push(result)

    @Fingerprint.register('N')
    def next(self, ip):
        if len(self.addrstack) < 80:
            self.addrstack.append(ip.position)
            ip.position = ip.pop_vector() - ip.delta
        else:
            self.reflect(ip) # this is actual behavior of INTERCAL-72. wtf.

    @Fingerprint.register('O')
    def unary_or(self, ip):
        a = ip.pop()
        ip.push(a | ((a >> 1) | ((a & 1) << getsize(a))))

    @Fingerprint.register('R')
    def resume(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        elif n > 0:
            if n > 1: del self.addrstack[-(n-1):]
            if self.addrstack:
                ip.position = self.addrstack.pop()

    @Fingerprint.register('S')
    def select(self, ip):
        b, a = ip.popmany(2)
        result = 0
        shift = 0
        while a or b:
            if b & 1:
                result |= (a & 1) << shift
                shift += 1
            a >>= 1
            b >>= 1
        ip.push(result)

    @Fingerprint.register('X')
    def unary_xor(self, ip):
        a = ip.pop()
        ip.push(a ^ ((a >> 1) | ((a & 1) << getsize(a))))

