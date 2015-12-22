"""Implementation of Befunge-93 commands.

There is internal (non-existent) Unefunge-93 base class, for extending with
Funge-98 base class later.
"""

from funge.vector import Vector
from funge.space import Befunge93Space
from funge.exception import IPQuitted
from funge.semantics import Semantics

import random

class Unefunge93(Semantics):
    dimension = 1
    is_concurrent = False
    is_filesystem = False
    has_systemcmd = False

    def __init__(self, platform):
        Semantics.__init__(self, platform)

        self.delta_left = Vector.zero(self.dimension).replace(_0=-1)
        self.delta_right = Vector.zero(self.dimension).replace(_0=1)

        self.random_deltas = [self.delta_left, self.delta_right]

    @classmethod
    def init_ip(self, ip):
        ip.delta = Vector.zero(ip.dimension).replace(1)

    def stringmode(self, ip):
        cell = ip.space.get(ip.position)
        if cell == 34:
            self.toggle_stringmode(ip)
        else:
            ip.push(cell)

    def undefined(self, ip):
        pass

    def divide_by_zero(self, ip, dividend, remainder):
        if remainder:
            tmpl = 'What do you want %d %% 0 to be? '
        else:
            tmpl = 'What do you want %d / 0 to be? '
        ip.push(self.platform.prompt(tmpl % dividend, int))

    @Semantics.register(' ')
    def space(self, ip):
        pass

    @Semantics.register('!')
    def logical_not(self, ip):
        if ip.pop():
            ip.push(0)
        else:
            ip.push(1)

    @Semantics.register('"')
    def toggle_stringmode(self, ip):
        ip.stringmode = not ip.stringmode

    @Semantics.register('#')
    def trampoline(self, ip):
        ip.position += ip.delta

    @Semantics.register('$')
    def pop(self, ip):
        ip.popmany(1)

    @Semantics.register('%')
    def remainder(self, ip):
        b, a = ip.popmany(2)
        if b == 0:
            self.divide_by_zero(ip, a, True)
        else:
            ip.push(a % b)

    @Semantics.register('&')
    def input_integer(self, ip):
        try:
            ip.push(self.platform.getint())
        except Exception:
            ip.push(0)

    @Semantics.register('*')
    def multiply(self, ip):
        b, a = ip.popmany(2)
        ip.push(a * b)

    @Semantics.register('+')
    def add(self, ip):
        b, a = ip.popmany(2)
        ip.push(a + b)

    @Semantics.register(',')
    def output_character(self, ip):
        self.platform.putchar(ip.pop() & 255)

    @Semantics.register('-')
    def subtract(self, ip):
        b, a = ip.popmany(2)
        ip.push(a - b)

    @Semantics.register('.')
    def output_integer(self, ip):
        self.platform.putint(ip.pop())

    @Semantics.register('/')
    def divide(self, ip):
        b, a = ip.popmany(2)
        if b == 0:
            self.divide_by_zero(ip, a, False)
        else:
            ip.push(a // b) # integer division

    @Semantics.register('0')
    def push_0(self, ip): ip.push(0)
    @Semantics.register('1')
    def push_1(self, ip): ip.push(1)
    @Semantics.register('2')
    def push_2(self, ip): ip.push(2)
    @Semantics.register('3')
    def push_3(self, ip): ip.push(3)
    @Semantics.register('4')
    def push_4(self, ip): ip.push(4)
    @Semantics.register('5')
    def push_5(self, ip): ip.push(5)
    @Semantics.register('6')
    def push_6(self, ip): ip.push(6)
    @Semantics.register('7')
    def push_7(self, ip): ip.push(7)
    @Semantics.register('8')
    def push_8(self, ip): ip.push(8)
    @Semantics.register('9')
    def push_9(self, ip): ip.push(9)

    @Semantics.register(':')
    def duplicate(self, ip):
        top = ip.pop()
        ip.push(top)
        ip.push(top)

    @Semantics.register('<')
    def go_west(self, ip):
        ip.delta = self.delta_left

    @Semantics.register('>')
    def go_east(self, ip):
        ip.delta = self.delta_right

    @Semantics.register('?')
    def go_away(self, ip):
        ip.delta = random.choice(self.random_deltas)

    @Semantics.register('@')
    def stop(self, ip):
        raise IPQuitted()

    @Semantics.register('\\')
    def swap(self, ip):
        b, a = ip.popmany(2)
        ip.push(b)
        ip.push(a)

    @Semantics.register('_')
    def east_west_if(self, ip):
        if ip.pop():
            ip.delta = self.delta_left
        else:
            ip.delta = self.delta_right

    @Semantics.register('`')
    def greater_than(self, ip):
        b, a = ip.popmany(2)
        if a > b:
            ip.push(1)
        else:
            ip.push(0)

    @Semantics.register('g')
    def get(self, ip):
        v = ip.pop_vector() + ip.offset
        ip.push(ip.space.get(v))

    @Semantics.register('p')
    def put(self, ip):
        v = ip.pop_vector() + ip.offset
        ip.space.put(v, ip.pop())

    @Semantics.register('~')
    def input_character(self, ip):
        try:
            ip.push(self.platform.getchar())
        except Exception:
            ip.push(0)

class Befunge93(Unefunge93):
    dimension = 2

    def __init__(self, platform):
        Unefunge93.__init__(self, platform)

        self.delta_up = Vector.zero(self.dimension).replace(_1=-1)
        self.delta_down = Vector.zero(self.dimension).replace(_1=1)

        self.random_deltas += [self.delta_up, self.delta_down]

    @classmethod
    def create_space(self):
        return Befunge93Space()

    @Semantics.register('^')
    def go_north(self, ip):
        ip.delta = self.delta_up

    @Semantics.register('v')
    def go_south(self, ip):
        ip.delta = self.delta_down

    @Semantics.register('|')
    def north_south_if(self, ip):
        if ip.pop():
            ip.delta = self.delta_up
        else:
            ip.delta = self.delta_down

class Befunge93_divbyzero_stop(Befunge93):
    def divide_by_zero(self, ip, dividend, remainder):
        self.platform.warn('Division by zero encountered at %r.' % (ip.position,))
        raise IPQuitted(1)

class Befunge93_divbyzero_value(Befunge93):
    def __init__(self, platform, divbyzero):
        Befunge93.__init__(self, platform)
        self.divbyzero = divbyzero

    def divide_by_zero(self, ip, dividend, remainder):
        self.platform.warn('Division by zero encountered at %r.' % (ip.position,))
        ip.push(self.divbyzero)

