from funge.fingerprint import Fingerprint

class SUBR(Fingerprint):
    'Subroutine extension'

    API = 'PyFunge v2'
    ID = 0x53554252

    def init(self, ip):
        Fingerprint.init(self, ip)
        if not hasattr(ip, 'SUBR_relmode'):
            ip.SUBR_relmode = False

    @Fingerprint.register('A')
    def absolute_mode(self, ip):
        ip.SUBR_relmode = False

    @Fingerprint.register('C')
    def call(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
            return
        target = ip.pop_vector()
        if ip.SUBR_relmode: target += ip.offset

        args = ip.popmany(n)
        ip.push_vector(ip.position)
        ip.push_vector(ip.delta)
        ip.pushmany(args)

        ip.position = target - self.delta_right
        ip.delta = self.delta_right

    @Fingerprint.register('J')
    def jump_to(self, ip):
        target = ip.pop_vector()
        if ip.SUBR_relmode: target += ip.offset

        ip.position = target - self.delta_right
        ip.delta = self.delta_right

    @Fingerprint.register('R')
    def return_from(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
            return
        args = ip.popmany(n)
        delta = ip.pop_vector()
        position = ip.pop_vector()

        ip.pushmany(args)

        ip.position = position
        ip.delta = delta

    @Fingerprint.register('O')
    def relative_mode(self, ip):
        ip.SUBR_relmode = True

