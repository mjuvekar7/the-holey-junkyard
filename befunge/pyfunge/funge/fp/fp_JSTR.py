from funge.vector import Vector
from funge.fingerprint import Fingerprint

class JSTR(Fingerprint):
    'Jesse van Herk\'s extensions to string functions'

    API = 'PyFunge v2'
    ID = 0x4a535452

    @Fingerprint.register('G')
    def get_ex(self, ip):
        n = ip.pop()
        pos = ip.pop_vector() + ip.offset
        delta = ip.pop_vector()

        ip.push(0)
        for i in xrange(n):
            ip.push(ip.space.get(pos))
            pos += delta

    @Fingerprint.register('P')
    def put_ex(self, ip):
        n = ip.pop()
        pos = ip.pop_vector() + ip.offset
        delta = ip.pop_vector()

        for i in xrange(n):
            ip.space.put(pos, ip.pop())
            pos += delta

