from funge.stack import TOSS
from funge.fingerprint import Fingerprint

class FRTH(Fingerprint):
    'Some common forth commands'

    API = 'PyFunge v2'
    ID = 0x46525448

    @Fingerprint.register('D')
    def depth(self, ip):
        ip.push(len(ip.stack[TOSS]))

    @Fingerprint.register('L')
    def roll(self, ip):
        n = ip.pop()
        if n < 0:
            target = ip.pop()
            values = [ip.pop() for i in xrange(-n)]
            ip.push(target)
            for value in values[::-1]: ip.push(value)
        elif n > 0:
            values = [ip.pop() for i in xrange(n)]
            target = ip.pop()
            for value in values[::-1]: ip.push(value)
            ip.push(target)

    @Fingerprint.register('O')
    def over(self, ip):
        b = ip.pop()
        a = ip.pop()
        ip.push(a)
        ip.push(b)
        ip.push(a)

    @Fingerprint.register('P')
    def pick(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        elif n >= len(ip.stack[TOSS]):
            ip.push(0)
        else:
            ip.push(ip.stack[TOSS][-n-1])

    @Fingerprint.register('R')
    def rot(self, ip):
        c = ip.pop()
        b = ip.pop()
        a = ip.pop()
        ip.push(b)
        ip.push(c)
        ip.push(a)

