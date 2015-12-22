from funge.fingerprint import Fingerprint

from struct import pack, unpack

def pop_long(ip):
    y, x = ip.popmany(2)
    value = ((x & 0xffffffff) << 32) + (y & 0xffffffff)
    return ((value + 0x8000000000000000) & 0xffffffffffffffff) - 0x8000000000000000

def push_long(ip, value):
    ip.push((((value >> 32) + 0x80000000) & 0xffffffff) - 0x80000000)
    ip.push(((value + 0x80000000) & 0xffffffff) - 0x80000000)

class LONG(Fingerprint):
    'Long Integers'

    API = 'PyFunge v2'
    ID = 0x4c4f4e47

    @Fingerprint.register('A')
    def long_add(self, ip):
        b = pop_long(ip)
        a = pop_long(ip)
        push_long(ip, a + b)

    @Fingerprint.register('B')
    def long_absolute_value(self, ip):
        a = pop_long(ip)
        push_long(ip, abs(a))

    @Fingerprint.register('D')
    def long_divide(self, ip):
        b = pop_long(ip)
        a = pop_long(ip)
        if b == 0:
            push_long(ip, 0)
        elif a < 0:
            push_long(ip, (a + abs(a) % abs(b)) / b)
        else:
            push_long(ip, (a - abs(a) % abs(b)) / b)

    @Fingerprint.register('E')
    def long_from_int(self, ip):
        push_long(ip, ip.pop())

    @Fingerprint.register('L')
    def long_shift_left(self, ip):
        n = ip.pop()
        a = pop_long(ip)
        if n < 0:
            self.reflect(ip)
        else:
            push_long(ip, a << n)

    @Fingerprint.register('M')
    def long_multiply(self, ip):
        b = pop_long(ip)
        a = pop_long(ip)
        push_long(ip, a * b)

    @Fingerprint.register('N')
    def long_negate(self, ip):
        push_long(ip, -pop_long(ip))

    @Fingerprint.register('O')
    def long_modulo(self, ip):
        b = pop_long(ip)
        a = pop_long(ip)
        if b == 0:
            push_long(ip, 0)
        elif a < 0:
            push_long(ip, -(abs(a) % abs(b)))
        else:
            push_long(ip, abs(a) % abs(b))

    @Fingerprint.register('P')
    def long_print(self, ip):
        a = pop_long(ip)
        self.platform.putint(a)

    @Fingerprint.register('R')
    def long_shift_right(self, ip):
        n = ip.pop()
        a = pop_long(ip)
        if n < 0:
            self.reflect(ip)
        else:
            push_long(ip, a >> n)

    @Fingerprint.register('S')
    def long_subtract(self, ip):
        b = pop_long(ip)
        a = pop_long(ip)
        push_long(ip, a - b)

    @Fingerprint.register('Z')
    def long_from_string(self, ip):
        s = ip.pop_string()
        try:
            push_long(ip, int(s))
        except Exception:
            self.reflect(ip)

