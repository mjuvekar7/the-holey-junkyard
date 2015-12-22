from funge.fingerprint import Fingerprint

import math
import operator

class IMTH(Fingerprint):
    'Some integer math functions'

    API = 'PyFunge v2'
    ID = 0x494d5448

    @Fingerprint.register('A')
    def average(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        elif n > 0:
            ip.push(sum(ip.popmany(n)) / n)
        else:
            ip.push(0)

    @Fingerprint.register('B')
    def absolute_value(self, ip):
        ip.push(abs(ip.pop()))

    @Fingerprint.register('C')
    def multiply_100(self, ip):
        ip.push(ip.pop() * 100)

    @Fingerprint.register('D')
    def decrease_absolute_value(self, ip):
        n = ip.pop()
        if n < 0:
            ip.push(n + 1)
        elif n > 0:
            ip.push(n - 1)
        else:
            ip.push(0)

    @Fingerprint.register('E')
    def multiply_10000(self, ip):
        ip.push(ip.pop() * 10000)

    @Fingerprint.register('F')
    def factorial(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        elif n > 0:
            ip.push(reduce(operator.mul, range(1, n+1), 1))
        else:
            # RC/Funge-98 pushes 0 for 0F, instead of correct 1. what the heck.
            ip.push(0)

    @Fingerprint.register('G')
    def sign(self, ip):
        n = ip.pop()
        if n < 0:
            ip.push(-1)
        elif n > 0:
            ip.push(+1)
        else:
            ip.push(0)

    @Fingerprint.register('H')
    def multiply_1000(self, ip):
        ip.push(ip.pop() * 1000)

    @Fingerprint.register('I')
    def increase_absolute_value(self, ip):
        n = ip.pop()
        if n < 0:
            ip.push(n - 1)
        elif n > 0:
            ip.push(n + 1)
        else:
            ip.push(0)

    @Fingerprint.register('L')
    def shift_left(self, ip):
        c, n = ip.popmany(2)
        if c < 0:
            ip.push(n >> -c)
        else:
            ip.push(n << c)

    @Fingerprint.register('N')
    def minimum(self, ip):
        n = ip.pop()
        if n <= 0:
            self.reflect(ip)
        else:
            ip.push(min(ip.popmany(n)))

    @Fingerprint.register('R')
    def shift_right(self, ip):
        c, n = ip.popmany(2)
        if c < 0:
            ip.push(n << -c)
        else:
            ip.push(n >> c)

    @Fingerprint.register('S')
    def sum(self, ip):
        n = ip.pop()
        if n < 0:
            self.reflect(ip)
        elif n > 0:
            ip.push(sum(ip.popmany(n)))
        else:
            ip.push(0)

    @Fingerprint.register('T')
    def multiply_10(self, ip):
        ip.push(ip.pop() * 10)

    @Fingerprint.register('U')
    def unsigned_print(self, ip):
        self.platform.putint(ip.pop() & 0xffffffff)

    @Fingerprint.register('X')
    def maximum(self, ip):
        n = ip.pop()
        if n <= 0:
            self.reflect(ip)
        else:
            ip.push(max(ip.popmany(n)))

    @Fingerprint.register('Z')
    def negate(self, ip):
        ip.push(-ip.pop())

