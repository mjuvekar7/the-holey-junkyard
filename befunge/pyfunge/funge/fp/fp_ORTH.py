from funge.fingerprint import Fingerprint

class ORTH(Fingerprint):
    'Orthogonal Easement Library'

    API = 'PyFunge v2'
    ID = 0x4f525448

    @Fingerprint.register('A')
    def bitwise_and(self, ip):
        b, a = ip.popmany(2)
        ip.push(a & b)

    @Fingerprint.register('O')
    def bitwise_or(self, ip):
        b, a = ip.popmany(2)
        ip.push(a | b)

    @Fingerprint.register('E')
    def bitwise_xor(self, ip):
        b, a = ip.popmany(2)
        ip.push(a ^ b)

    @Fingerprint.register('X')
    def change_x(self, ip):
        ip.position = ip.position.replace(_0=ip.pop()-ip.delta[0])

    @Fingerprint.register('Y')
    def change_y(self, ip):
        if ip.dimension > 1:
            ip.position = ip.position.replace(_1=ip.pop()-ip.delta[1])
        else:
            self.reflect()

    @Fingerprint.register('V')
    def change_dx(self, ip):
        ip.delta = ip.delta.replace(_0=ip.pop())

    @Fingerprint.register('W')
    def change_dy(self, ip):
        if ip.dimension > 1:
            ip.delta = ip.delta.replace(_1=ip.pop())
        else:
            self.reflect(ip)

    @Fingerprint.register('G')
    def orthogonal_get(self, ip):
        v = ip.pop_vector()[::-1]
        ip.push(ip.space.get(v))

    @Fingerprint.register('P')
    def orthogonal_put(self, ip):
        v = ip.pop_vector()[::-1]
        ip.space.put(v, ip.pop())

    @Fingerprint.register('Z')
    def ramp_if_zero(self, ip):
        if ip.pop():
            self.no_operation(ip)
        else:
            self.trampoline(ip)

    @Fingerprint.register('S')
    def output_string(self, ip):
        c = ip.pop()
        while c:
            self.platform.putchar(c)
            c = ip.pop()

