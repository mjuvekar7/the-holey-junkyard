from funge.vector import Vector
from funge.fingerprint import Fingerprint

class STRN(Fingerprint):
    'String functions'

    API = 'PyFunge v2'
    ID = 0x5354524e

    @Fingerprint.register('A')
    def append(self, ip):
        a = ip.pop_string()
        b = ip.pop_string()
        ip.push_string(a + b)

    @Fingerprint.register('C')
    def compare(self, ip):
        a = ip.pop_string()
        b = ip.pop_string()
        if a > b:
            ip.push(+1)
        elif a < b:
            ip.push(-1)
        else:
            ip.push(0)

    @Fingerprint.register('D')
    def display(self, ip):
        self.platform.putstr(ip.pop_string())

    @Fingerprint.register('F')
    def search(self, ip):
        a = ip.pop_string()
        b = ip.pop_string()
        try:
            ip.push_string(a[a.index(b):])
        except Exception:
            ip.push(0) # null string

    @Fingerprint.register('G')
    def get(self, ip):
        pos = ip.pop_vector() + ip.offset

        boundmin = ip.space.boundmin
        boundmax = ip.space.boundmax
        get = ip.space.get
        delta = self.delta_right
        items = []
        while pos.between(boundmin, boundmax):
            cell = get(pos)
            if cell == 0: break
            items.append(cell)
            pos += delta
        else:
            self.reflect(ip)
            return

        ip.push_string(''.join(map(chr, items)))

    @Fingerprint.register('I')
    def input(self, ip):
        string = []
        try:
            while 1:
                ch = self.platform.getchar()
                if ch == 10: break
                string.append(ch)
        except Exception:
            self.reflect(ip)
        else:
            ip.push_string(''.join(map(chr, string)).rstrip('\r\n'))

    @Fingerprint.register('L')
    def left(self, ip):
        n = ip.pop()
        a = ip.pop_string()
        if n < 0:
            self.reflect(ip)
        else:
            ip.push_string(a[:n])

    @Fingerprint.register('M')
    def slice(self, ip):
        n, s = ip.popmany(2)
        a = ip.pop_string()
        if n < 0 or not 0 <= s < len(a):
            self.reflect(ip)
        else:
            ip.push_string(a[s:s+n])

    @Fingerprint.register('N')
    def length(self, ip):
        a = ip.pop_string()
        ip.push_string(a)
        ip.push(len(a))

    @Fingerprint.register('P')
    def put(self, ip):
        pos = ip.pop_vector() + ip.offset
        string = ip.pop_string()

        put = ip.space.put
        delta = self.delta_right
        for ch in string:
            put(pos, ord(ch))
            pos += delta
        put(pos, 0)

    @Fingerprint.register('R')
    def right(self, ip):
        n = ip.pop()
        a = ip.pop_string()
        if n < 0:
            self.reflect(ip)
        else:
            ip.push_string(a[-n:])

    @Fingerprint.register('S')
    def from_integer(self, ip):
        num = ip.pop()
        ip.push_string(str(num))

    @Fingerprint.register('V')
    def to_integer(self, ip):
        s = ip.pop_string()
        try:
            ip.push(int(s))
        except Exception:
            self.reflect(ip)

