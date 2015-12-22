from funge.vector import Vector
from funge.fingerprint import Fingerprint

class INDV(Fingerprint):
    'Pointer functions'

    API = 'PyFunge v2'
    ID = 0x494E4456

    @Fingerprint.register('G')
    def get_num(self, ip):
        pos = ip.pop_vector()

        pos2 = []
        for i in xrange(ip.dimension):
            pos2.append(ip.space.get(pos))
            pos += self.delta_right
        pos2 = Vector(pos2[::-1])

        ip.push(ip.space.get(pos2))

    @Fingerprint.register('P')
    def put_num(self, ip):
        pos = ip.pop_vector()

        pos2 = []
        for i in xrange(ip.dimension):
            pos2.append(ip.space.get(pos))
            pos += self.delta_right
        pos2 = Vector(pos2[::-1])

        ip.space.put(pos2, ip.pop())

    @Fingerprint.register('V')
    def get_vector(self, ip):
        pos = ip.pop_vector()

        pos2 = []
        for i in xrange(ip.dimension):
            pos2.append(ip.space.get(pos))
            pos += self.delta_right
        pos2 = Vector(pos2[::-1])

        vec = []
        for i in xrange(ip.dimension):
            vec.append(ip.space.get(pos2))
            pos2 += self.delta_right
        ip.push_vector(vec[::-1])

    @Fingerprint.register('W')
    def put_vector(self, ip):
        pos = ip.pop_vector()

        pos2 = []
        for i in xrange(ip.dimension):
            pos2.append(ip.space.get(pos))
            pos += self.delta_right
        pos2 = Vector(pos2[::-1])

        vec = ip.pop_vector()
        for v in vec[::-1]:
            ip.space.put(pos2, v)
            pos2 += self.delta_right

