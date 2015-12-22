"""Instruction pointer (IP) implementation."""

import copy, os.path

from funge.stack import StackStack, TOSS
from funge.space import BoundedSpace
from funge.vector import Vector

class IP(object):
    def __init__(self, program, id, parent=None):
        self.program = program

        self.stringmode = False

        self.team = 1
        self.id = id
        if parent is None:
            self.parentid = None
        else:
            self.parentid = parent.id

        self.dimension = program.space.dimension
        self.space = program.space
        if parent is None:
            self.position = Vector.zero(self.dimension)
            self.delta = Vector.zero(self.dimension)
            self.offset = Vector.zero(self.dimension)
            self.stack = StackStack()
        else:
            self.position = parent.position
            self.delta = parent.delta
            self.offset = parent.offset
            self.stack = parent.stack.copy()

        self.commands = program.semantics.commands.copy()
        self.prevcommands = {}
        self.fploaded = []

        # rebinds the stack stack methods.
        self.invertmode = self.invertmode
        self.queuemode = self.queuemode

    def _get_invertmode(self):
        return self.stack.invertmode

    def _set_invertmode(self, flag):
        self.stack.invertmode = flag
        self.push = self.stack.push
        self.pushmany = self.stack.pushmany
        self.push_string = self.stack.push_string
        self.push_vector = self.stack.push_vector

    invertmode = property(_get_invertmode, _set_invertmode)

    def _get_queuemode(self):
        return self.stack.queuemode

    def _set_queuemode(self, flag):
        self.stack.queuemode = flag
        self.discard = self.stack.discard
        self.pop = self.stack.pop
        self.popmany = self.stack.popmany
        self.pop_string = self.stack.pop_string

    queuemode = property(_get_queuemode, _set_queuemode)

    def add_command(self, cmd, callback):
        self.prevcommands.setdefault(cmd, []).append(self.commands.get(cmd))
        if callback is None:
            del self.commands[cmd]
        else:
            self.commands[cmd] = callback

    def add_commands(self, overlay):
        for cmd, callback in overlay.commands.items():
            self.add_command(cmd, callback)

    def remove_command(self, cmd):
        prevcmds = self.prevcommands.get(cmd, [])
        if len(prevcmds) > 0:
            callback = prevcmds.pop()
            if callback is None:
                try:
                    del self.commands[cmd]
                except Exception:
                    pass
            else:
                self.commands[cmd] = callback

    def remove_commands(self, overlay):
        for cmd, callback in overlay.commands.items():
            # TODO check self.commands[cmd] and callback for diagnostics.
            self.remove_command(cmd)

    def load_fingerprint(self, fpid):
        try:
            fpcls = self.program.fplookup[fpid]
            fp = fpcls(self.program.semantics)
            fp.init(self)
            self.fploaded.append(fp)
            return True
        except Exception:
            return False

    def unload_fingerprint(self, fpid):
        try:
            fpcls = self.program.fplookup[fpid]
        except Exception:
            return False

        for i in reversed(xrange(len(self.fploaded))):
            if self.fploaded[i].__class__ is fpcls:
                try:
                    self.fploaded.pop(i).final(self)
                    return True
                except Exception:
                    return False
        return False

    def final(self):
        for fp in self.fploaded:
            fp.final(self)

    def push(self, item, stack=TOSS): self.stack.push(item, stack=stack)
    def pushmany(self, items, stack=TOSS): self.stack.pushmany(items, stack=stack)
    def push_string(self, s, stack=TOSS): self.stack.push_string(s, stack=stack)
    def push_vector(self, v, stack=TOSS): self.stack.push_vector(v, stack=stack)

    def discard(self, n=1, stack=TOSS): self.stack.discard(n, stack=stack)
    def pop(self, stack=TOSS): return self.stack.pop(stack=stack)
    def popmany(self, n, stack=TOSS): return self.stack.popmany(n, stack=stack)
    def pop_string(self, stack=TOSS): return self.stack.pop_string(stack=stack)
    def pop_vector(self, stack=TOSS):
        return Vector(self.stack.pop_vector(self.dimension, stack=stack))

