from funge.fingerprint import Fingerprint

import sys
import math
from struct import pack, unpack

def pop_float(ip):
    return unpack('f', pack('I', ip.pop() & 0xffffffff))[0]

def push_float(ip, value):
    ip.push(unpack('i', pack('f', value))[0])

class FPSP(Fingerprint):
    'Single precision floating point'

    API = 'PyFunge v2'
    ID = 0x46505350

    if sys.hexversion < 0x20600f0:
        plusinf = 1e99999
        minusinf = -1e99999
        nan = plusinf + minusinf
    else:
        plusinf = float('inf')
        minusinf = float('-inf')
        nan = float('nan')

    @Fingerprint.register('A')
    def add(self, ip):
        b = pop_float(ip)
        a = pop_float(ip)
        push_float(ip, a + b)

    @Fingerprint.register('B')
    def sine(self, ip):
        v = pop_float(ip)
        push_float(ip, math.sin(v))

    @Fingerprint.register('C')
    def cosine(self, ip):
        v = pop_float(ip)
        push_float(ip, math.cos(v))

    @Fingerprint.register('D')
    def divide(self, ip):
        b = pop_float(ip)
        a = pop_float(ip)
        if b == 0:
            push_float(ip, self.nan) # XXX should be inf or -inf?
        else:
            push_float(ip, a / b)

    @Fingerprint.register('E')
    def arcsine(self, ip):
        v = pop_float(ip)
        if -1 <= v <= 1:
            push_float(ip, math.asin(v))
        else:
            push_float(ip, self.nan)

    @Fingerprint.register('F')
    def from_integer(self, ip):
        push_float(ip, ip.pop())

    @Fingerprint.register('G')
    def arctangent(self, ip):
        v = pop_float(ip)
        push_float(ip, math.atan(v))

    @Fingerprint.register('H')
    def arccosine(self, ip):
        v = pop_float(ip)
        if -1 <= v <= 1:
            push_float(ip, math.acos(v))
        else:
            push_float(ip, self.nan)

    @Fingerprint.register('I')
    def to_integer(self, ip):
        v = pop_float(ip)
        ip.push(int(v))

    @Fingerprint.register('K')
    def logarithm(self, ip):
        v = pop_float(ip)
        if v <= 0:
            push_float(ip, self.minusinf)
        else:
            push_float(ip, math.log(v))

    @Fingerprint.register('L')
    def logarithm_10(self, ip):
        v = pop_float(ip)
        if v <= 0:
            push_float(ip, self.minusinf)
        else:
            push_float(ip, math.log10(v))

    @Fingerprint.register('M')
    def multiply(self, ip):
        b = pop_float(ip); a = pop_float(ip)
        push_float(ip, a * b)

    @Fingerprint.register('N')
    def negate(self, ip):
        push_float(ip, -pop_float(ip))

    @Fingerprint.register('P')
    def output(self, ip):
        v = pop_float(ip)
        self.platform.putstr('%f' % v)

    @Fingerprint.register('Q')
    def sqrt(self, ip):
        v = pop_float(ip)
        if v < 0:
            push_float(ip, self.nan)
        else:
            push_float(ip, math.sqrt(v))

    @Fingerprint.register('R')
    def from_string(self, ip):
        try:
            push_float(ip, float(ip.pop_string()))
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('S')
    def subtract(self, ip):
        b = pop_float(ip)
        a = pop_float(ip)
        push_float(ip, a - b)

    @Fingerprint.register('T')
    def tangent(self, ip):
        v = pop_float(ip)
        push_float(ip, math.tan(v))

    @Fingerprint.register('V')
    def absolute_value(self, ip):
        push_float(ip, abs(pop_float(ip)))

    @Fingerprint.register('X')
    def exponential(self, ip):
        push_float(ip, math.exp(pop_float(ip)))

    @Fingerprint.register('Y')
    def power(self, ip):
        y = pop_float(ip)
        x = pop_float(ip)
        try:
            push_float(ip, x ** y)
        except ValueError:
            self.reflect(ip) # XXX

