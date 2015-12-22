"""Implementation of Unefunge/Befunge/Trefunge-98 commands.
"""

from funge.vector import Vector
from funge.stack import TOSS, SOSS
from funge.space import Space
from funge.exception import IPQuitted
from funge.semantics import Semantics
from funge.languages.befunge93 import Unefunge93, Befunge93

import os, sys
import time

class Unefunge98(Unefunge93):
    dimension = 1

    @classmethod
    def create_space(self):
        return Space(self.dimension)

    def walk(self, ip):
        delta = ip.delta
        pos = ip.position
        get = ip.space.get
        scanwhile = ip.space.scanwhile
        scanuntil = ip.space.scanuntil

        if ip.stringmode:
            # advance to next cell, no matter if next cell is space
            # (since it has to be executed in this context anyway)
            cell = get(pos)
            pos += delta
            if cell == 32:
                # space is already executed, find next non-space cell
                pos = scanwhile(pos, delta, 32)
            else:
                # no normalization here, see sgml-spaces-wrap4 test.
                pass
        else:
            # skip to next non-space instruction.
            pos += delta
            cell = get(pos)
            if cell == 59:
                pos = scanuntil(pos + delta, delta, 59) + delta
            while 1:
                pos = scanwhile(pos, delta, 32)
                cell = get(pos)
                if cell == 59:
                    pos = scanuntil(pos + delta, delta, 59) + delta
                else:
                    break

        ip.position = pos

    def divide_by_zero(self, ip, dividend, remainder):
        ip.push(0) # different from Befunge-93 behavior

    @Semantics.register('&')
    def input_integer(self, ip):
        try:
            ip.push(self.platform.getint())
        except Exception:
            self.reflect(ip) # different from Befunge-93 behavior

    @Semantics.register("'")
    def fetch_character(self, ip):
        ip.position += ip.delta
        ip.push(ip.space.get(ip.position))

    @Semantics.register('(')
    def load_semantics(self, ip):
        count = ip.pop()
        fpid = 0
        for i in xrange(count):
            fpid = (fpid << 8) + ip.pop()
        if ip.load_fingerprint(fpid):
            ip.push(fpid)
            ip.push(1)
        else:
            self.reflect(ip)

    @Semantics.register(')')
    def unload_semantics(self, ip):
        count = ip.pop()
        fpid = 0
        for i in xrange(count):
            fpid = (fpid << 8) + ip.pop()
        if not ip.unload_fingerprint(fpid):
            self.reflect(ip)

    @Semantics.register(';')
    def jump_over(self, ip):
        # rarely reachable. (notable exception being concurrent/generated-marker)
        # since we should keep tick count, find next instruction and execute it
        # immediately, so ;...; can be ignored properly.
        self.walk(ip)
        self.command(ip)

    @Semantics.register('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    def fingerprint_commands(self, ip):
        self.reflect(ip)

    @Semantics.register('a')
    def push_10(self, ip): ip.push(10)
    @Semantics.register('b')
    def push_11(self, ip): ip.push(11)
    @Semantics.register('c')
    def push_12(self, ip): ip.push(12)
    @Semantics.register('d')
    def push_13(self, ip): ip.push(13)
    @Semantics.register('e')
    def push_14(self, ip): ip.push(14)
    @Semantics.register('f')
    def push_15(self, ip): ip.push(15)

    @Semantics.register('j')
    def jump_forward(self, ip):
        ip.position = ip.space.normalize(ip.position + ip.delta * ip.pop(), ip.delta)

    @Semantics.register('k')
    def iterate(self, ip):
        number = ip.pop()
        prevpos = ip.position
        prevdelta = ip.delta

        # look ahead next non-space instruction.
        self.walk(ip)

        if number != 0:
            instr = ip.space.get(ip.position)

            # move back to "k" command. should skip next instruction later.
            nextpos = ip.position
            ip.position = prevpos

            try:
                method = ip.commands[instr]
            except KeyError:
                return # TODO acts like reflect?

            for i in xrange(number):
                method(ip)

    @Semantics.register('n')
    def clear_stack(self, ip):
        ip.stack[TOSS].clear()

    @Semantics.register('q')
    def quit(self, ip):
        exitcode = ip.pop()
        raise IPQuitted(exitcode)

    @Semantics.register('r')
    def reflect(self, ip):
        ip.delta = -ip.delta

    @Semantics.register('s')
    def store_character(self, ip):
        current = ip.pop()
        ip.position += ip.delta
        ip.space.put(ip.position, current)

    @Semantics.register('u')
    def stack_under_stack(self, ip):
        if len(ip.stack) < 2:
            self.reflect(ip)
            return

        n = ip.pop()
        if n > 0:
            items = ip.popmany(n, stack=SOSS)[::-1]
            ip.pushmany(items, stack=TOSS)
        elif n < 0:
            items = ip.popmany(-n, stack=TOSS)[::-1]
            ip.pushmany(items, stack=SOSS)

    @Semantics.register('x')
    def absolute_delta(self, ip):
        ip.delta = ip.pop_vector()

    @Semantics.register('y')
    def get_sysinfo(self, ip):
        tm = time.localtime()
        dimension = self.dimension

        mode = ip.pop()
        toss = len(ip.stack[TOSS])
        if mode <= 0 or 10 + 3 * dimension <= mode < 10 + 5 * dimension:
            # it's very time consuming task. do this only if needed.
            rectmin, rectmax = ip.space.getrect()
        else:
            rectmin = rectmax = Vector.zero(dimension) # dummy!

        flags = 0x00
        if self.is_concurrent: flags |= 0x01 # adds "t" command
        if self.is_filesystem: flags |= 0x0e # adds "i", "o", "=" commands
        if self.platform.unbuffered_io: flags |= 0x10
        paradigm = 0
        if self.has_systemcmd: paradigm = 1 # equivalent to system() behavior

        bytespercell = -1 # bignum, undefined
        handprint = ip.program.FUNGE_HANDPRINT
        version = ip.program.FUNGE_VERSION

        ip.pushmany(
                [flags, bytespercell, handprint, version, paradigm, ord(os.sep),
                 dimension, ip.id, ip.team] +
                list(ip.position[::-1]) + list(ip.delta[::-1]) + list(ip.offset[::-1]) +
                list(rectmin[::-1]) + list((rectmax - rectmin)[::-1]) +
                [((tm[0]-1900) << 16) + (tm[1] << 8) + tm[2],
                 (tm[3] << 16) + (tm[4] << 8) + tm[5],
                 len(ip.stack)] +
                ([toss] + map(len, ip.stack[-2::-1])) +
                map(ord, '\0'.join(self.platform.args) + '\0\0\0') +
                map(ord, '\0'.join(k+'='+v for k,v in self.platform.environ.items()) + '\0\0')
            )

        if mode > 0:
            value = ip.stack[TOSS][-mode]
            infolen = len(ip.stack[TOSS]) - toss
            ip.discard(infolen, stack=TOSS)
            ip.push(value)

    @Semantics.register('z')
    def no_operation(self, ip):
        pass

    @Semantics.register('{')
    def begin_block(self, ip):
        n = ip.pop()
        ip.stack.push_stack()
        if n > 0:
            items = ip.popmany(n, stack=SOSS)
            ip.pushmany(items, stack=TOSS)
        elif n < 0:
            items = ip.popmany(-n, stack=TOSS)
            ip.pushmany(items, stack=SOSS)
        ip.push_vector(ip.offset, stack=SOSS)
        ip.offset = ip.position + ip.delta

    @Semantics.register('}')
    def end_block(self, ip):
        if len(ip.stack) < 2:
            self.reflect(ip)
            return

        ip.offset = ip.pop_vector(stack=SOSS)
        n = ip.pop()
        if n > 0:
            items = ip.popmany(n, stack=TOSS)
            ip.pushmany(items, stack=SOSS)
        elif n < 0:
            items = ip.popmany(-n, stack=SOSS)
            ip.pushmany(items, stack=TOSS)
        ip.stack.pop_stack()

    @Semantics.register('~')
    def input_character(self, ip):
        try:
            ip.push(self.platform.getchar())
        except Exception:
            self.reflect(ip) # different from Befunge-93 behavior

    undefined = reflect

class Befunge98(Unefunge98, Befunge93):
    dimension = 2

    @Semantics.register('[')
    def turn_left(self, ip):
        ip.delta = ip.delta.replace(ip.delta[1], -ip.delta[0])

    @Semantics.register(']')
    def turn_right(self, ip):
        ip.delta = ip.delta.replace(-ip.delta[1], ip.delta[0])

    @Semantics.register('w')
    def compare(self, ip):
        b, a = ip.popmany(2)
        if a < b:
            self.turn_left(ip)
        elif a > b:
            self.turn_right(ip)

class Trefunge98(Befunge98):
    dimension = 3

    def __init__(self, platform):
        Befunge98.__init__(self, platform)

        self.delta_high = Vector.zero(self.dimension).replace(_2=-1)
        self.delta_low = Vector.zero(self.dimension).replace(_2=1)

        self.random_deltas += [self.delta_high, self.delta_low]

    @Semantics.register('h')
    def go_high(self, ip):
        ip.delta = self.delta_high

    @Semantics.register('l')
    def go_low(self, ip):
        ip.delta = self.delta_low

    @Semantics.register('m')
    def high_low_if(self, ip):
        if ip.pop():
            ip.delta = self.delta_high
        else:
            ip.delta = self.delta_low

