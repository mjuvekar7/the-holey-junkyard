from funge.semantics import SemanticsOverlay
from funge.fingerprint import Fingerprint

class Hovermode1D(SemanticsOverlay):
    @SemanticsOverlay.register('<')
    def go_west(self, ip):
        ip.delta = ip.delta.replace(_0=ip.delta[0]-1)

    @SemanticsOverlay.register('>')
    def go_east(self, ip):
        ip.delta = ip.delta.replace(_0=ip.delta[0]+1)

    @SemanticsOverlay.register('_')
    def east_west_if(self, ip):
        if ip.pop():
            ip.delta = ip.delta.replace(_0=ip.delta[0]-1)
        else:
            ip.delta = ip.delta.replace(_0=ip.delta[0]+1)

class Hovermode2D(Hovermode1D):
    @SemanticsOverlay.register('^')
    def go_north(self, ip):
        ip.delta = ip.delta.replace(_1=ip.delta[1]-1)

    @SemanticsOverlay.register('v')
    def go_south(self, ip):
        ip.delta = ip.delta.replace(_1=ip.delta[1]+1)

    @SemanticsOverlay.register('|')
    def north_south_if(self, ip):
        if ip.pop():
            ip.delta = ip.delta.replace(_1=ip.delta[1]-1)
        else:
            ip.delta = ip.delta.replace(_1=ip.delta[1]+1)

class Switchmode1D(SemanticsOverlay):
    @SemanticsOverlay.register('{')
    def begin_block(self, ip):
        ip.space.put(ip.position, ord('}'))
        return self.semantics.begin_block(ip)

    @SemanticsOverlay.register('}')
    def end_block(self, ip):
        ip.space.put(ip.position, ord('{'))
        return self.semantics.end_block(ip)

    @SemanticsOverlay.register('(')
    def load_semantics(self, ip):
        ip.space.put(ip.position, ord(')'))
        return self.semantics.load_semantics(ip)

    @SemanticsOverlay.register(')')
    def unload_semantics(self, ip):
        ip.space.put(ip.position, ord('('))
        return self.semantics.unload_semantics(ip)

class Switchmode2D(Switchmode1D):
    @SemanticsOverlay.register('[')
    def turn_left(self, ip):
        ip.space.put(ip.position, ord(']'))
        return self.semantics.turn_left(ip)

    @SemanticsOverlay.register(']')
    def turn_right(self, ip):
        ip.space.put(ip.position, ord('['))
        return self.semantics.turn_right(ip)

class MODE(Fingerprint):
    'Funge-98 Standard Modes'

    API = 'PyFunge v2'
    ID = 0x4d4f4445

    def init(self, ip):
        Fingerprint.init(self, ip)
        if not hasattr(ip, 'hovermode'):
            ip.hovermode = None
        if not hasattr(ip, 'switchmode'):
            ip.switchmode = None

    @Fingerprint.register('H')
    def toggle_hovermode(self, ip):
        if ip.hovermode is None:
            if ip.dimension > 1:
                ip.hovermode = Hovermode2D(self.semantics)
            else:
                ip.hovermode = Hovermode1D(self.semantics)
            ip.add_commands(ip.hovermode)
        else:
            ip.remove_commands(ip.hovermode)
            ip.hovermode = None

    @Fingerprint.register('I')
    def toggle_invertmode(self, ip):
        ip.invertmode = not ip.invertmode

    @Fingerprint.register('Q')
    def toggle_queuemode(self, ip):
        ip.queuemode = not ip.queuemode

    @Fingerprint.register('S')
    def toggle_switchmode(self, ip):
        if ip.switchmode is None:
            if ip.dimension > 1:
                ip.switchmode = Switchmode2D(self.semantics)
            else:
                ip.switchmode = Switchmode1D(self.semantics)
            ip.add_commands(ip.switchmode)
        else:
            ip.remove_commands(ip.switchmode)
            ip.switchmode = None

