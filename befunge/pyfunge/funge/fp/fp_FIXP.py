from funge.fingerprint import Fingerprint

import math, random

class FIXP(Fingerprint):
    'Some useful fixed point math functions'

    API = 'PyFunge v2'
    ID = 0x46495850

    @Fingerprint.register('A')
    def bitwise_and(self, ip):
        a, b = ip.popmany(2)
        ip.push(a & b)

    @Fingerprint.register('B')
    def arccosine(self, ip):
        v = ip.pop()
        if -10000 <= v <= 10000:
            ip.push(int(round(math.acos(v / 10000.) * 1800000 / math.pi)))
        else:
            self.reflect(ip)

    @Fingerprint.register('C')
    def cosine(self, ip):
        ip.push(int(round(math.cos(ip.pop() * math.pi / 1800000.) * 10000)))

    @Fingerprint.register('D')
    def random(self, ip):
        ip.push(int(random.random() * ip.pop()))

    @Fingerprint.register('I')
    def sine(self, ip):
        ip.push(int(round(math.sin(ip.pop() * math.pi / 1800000.) * 10000)))

    @Fingerprint.register('J')
    def arcsine(self, ip):
        v = ip.pop()
        if -10000 <= v <= 10000:
            ip.push(int(round(math.asin(v / 10000.) * 1800000 / math.pi)))
        else:
            self.reflect(ip)

    @Fingerprint.register('N')
    def negate(self, ip):
        ip.push(-ip.pop())

    @Fingerprint.register('O')
    def bitwise_or(self, ip):
        a, b = ip.popmany(2)
        ip.push(a | b)

    @Fingerprint.register('P')
    def multiply_pi(self, ip):
        ip.push(int(ip.pop() * math.pi))

    @Fingerprint.register('Q')
    def sqrt(self, ip):
        v = ip.pop()
        if v < 0:
            self.reflect(ip)
        else:
            ip.push(int(math.sqrt(v)))

    @Fingerprint.register('R')
    def power(self, ip):
        b, a = ip.popmany(2)
        if a == b == 0:
            self.reflect(ip)
        elif b < 0:
            ip.push(0)
        else:
            ip.push(a ** b)

    @Fingerprint.register('S')
    def sign(self, ip):
        v = ip.pop()
        if v > 0:
            ip.push(1)
        elif v < 0:
            ip.push(-1)
        else:
            ip.push(0)

    @Fingerprint.register('T')
    def tangent(self, ip):
        ip.push(int(round(math.tan(ip.pop() * math.pi / 1800000.) * 10000)))

    @Fingerprint.register('U')
    def arctangent(self, ip):
        ip.push(int(round(math.atan(ip.pop() / 10000.) * 1800000 / math.pi)))

    @Fingerprint.register('V')
    def absolute_value(self, ip):
        ip.push(abs(ip.pop()))

    @Fingerprint.register('X')
    def bitwise_xor(self, ip):
        a, b = ip.popmany(2)
        ip.push(a ^ b)


