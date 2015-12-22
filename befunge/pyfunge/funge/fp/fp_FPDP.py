from funge.fingerprint import Fingerprint

import sys
import math
from struct import pack, unpack

def pop_double(ip):
    x, y = ip.popmany(2)
    return unpack('d', pack('II', y & 0xffffffff, x & 0xffffffff))[0]

def push_double(ip, value):
    y, x = unpack('ii', pack('d', value))
    ip.push(y)
    ip.push(x)

class FPDP(Fingerprint):
    'Double precision floating point'

    API = 'PyFunge v2'
    ID = 0x46504450

    if sys.hexversion < 0x20600f0:
        plusinf = 1e99999
        minusinf = -1e99999
        nan = plusinf + minusinf
    else:
        plusinf = float('inf')
        minusinf = float('-inf')
        nan = float('nan')

    def fpop(self, ip):
        x, y = ip.popmany(2)
        return struct.unpack('d', struct.pack('II', y & 0xffffffff, x & 0xffffffff))[0]

    def fpush(self, ip, value):
        y, x = struct.unpack('ii', struct.pack('d', value))
        ip.push(y)
        ip.push(x)

    @Fingerprint.register('A')
    def add(self, ip):
        b = pop_double(ip)
        a = pop_double(ip)
        push_double(ip, a + b)

    @Fingerprint.register('B')
    def sine(self, ip):
        v = pop_double(ip)
        push_double(ip, math.sin(v))

    @Fingerprint.register('C')
    def cosine(self, ip):
        v = pop_double(ip)
        push_double(ip, math.cos(v))

    @Fingerprint.register('D')
    def divide(self, ip):
        b = pop_double(ip)
        a = pop_double(ip)
        if b == 0:
            push_double(ip, self.nan) # XXX should be inf or -inf?
        else:
            push_double(ip, a / b)

    @Fingerprint.register('E')
    def arcsine(self, ip):
        v = pop_double(ip)
        if -1 <= v <= 1:
            push_double(ip, math.asin(v))
        else:
            push_double(ip, self.nan)

    @Fingerprint.register('F')
    def from_integer(self, ip):
        push_double(ip, ip.pop())

    @Fingerprint.register('G')
    def arctangent(self, ip):
        v = pop_double(ip)
        push_double(ip, math.atan(v))

    @Fingerprint.register('H')
    def arccosine(self, ip):
        v = pop_double(ip)
        if -1 <= v <= 1:
            push_double(ip, math.acos(v))
        else:
            push_double(ip, self.nan)

    @Fingerprint.register('I')
    def to_integer(self, ip):
        v = pop_double(ip)
        ip.push(int(v))

    @Fingerprint.register('K')
    def logarithm(self, ip):
        v = pop_double(ip)
        if v <= 0:
            push_double(ip, self.minusinf)
        else:
            push_double(ip, math.log(v))

    @Fingerprint.register('L')
    def logarithm_10(self, ip):
        v = pop_double(ip)
        if v <= 0:
            push_double(ip, self.minusinf)
        else:
            push_double(ip, math.log10(v))

    @Fingerprint.register('M')
    def multiply(self, ip):
        b = pop_double(ip); a = pop_double(ip)
        push_double(ip, a * b)

    @Fingerprint.register('N')
    def negate(self, ip):
        push_double(ip, -pop_double(ip))

    @Fingerprint.register('P')
    def output(self, ip):
        v = pop_double(ip)
        self.platform.putstr('%f' % v)

    @Fingerprint.register('Q')
    def sqrt(self, ip):
        v = pop_double(ip)
        if v < 0:
            push_double(ip, self.nan)
        else:
            push_double(ip, math.sqrt(v))

    @Fingerprint.register('R')
    def from_string(self, ip):
        try:
            push_double(ip, float(ip.pop_string()))
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('S')
    def subtract(self, ip):
        b = pop_double(ip)
        a = pop_double(ip)
        push_double(ip, a - b)

    @Fingerprint.register('T')
    def tangent(self, ip):
        v = pop_double(ip)
        push_double(ip, math.tan(v))

    @Fingerprint.register('V')
    def absolute_value(self, ip):
        push_double(ip, abs(pop_double(ip)))

    @Fingerprint.register('X')
    def exponential(self, ip):
        push_double(ip, math.exp(pop_double(ip)))

    @Fingerprint.register('Y')
    def power(self, ip):
        y = pop_double(ip)
        x = pop_double(ip)
        try:
            push_double(ip, x ** y)
        except ValueError:
            self.reflect(ip) # XXX

