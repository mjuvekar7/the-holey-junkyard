"""Implementation of stack and stack stack."""

TOSS = -1
SOSS = -2

class Stack(list):
    push = list.append

    def pushmany(self, items):
        self.extend(reversed(items))

    def push_string(self, s):
        items = map(ord, s) + [0]
        self.append(0)
        self.extend(map(ord, s[::-1]))

    push_vector = list.extend

    def rpush(self, item):
        self.insert(0, item)

    def rpushmany(self, items):
        self[0:0] = items

    def rpush_string(self, s):
        self[0:0] = map(ord, s) + [0]

    def rpush_vector(self, v):
        self[0:0] = reversed(v)

    def discard(self, n=1):
        assert n >= 0
        if n > 0: del self[-n:]

    def pop(self):
        try:
            return list.pop(self)
        except IndexError:
            return 0

    def popmany(self, n):
        assert n > 0
        result = self[-1:-n-1:-1]
        del self[-n:]
        if len(result) < n:
            result.extend([0] * (n - len(result)))
        return result

    def pop_string(self):
        for firstzero in xrange(len(self)-1, -1, -1):
            if self[firstzero] == 0: break
        else:
            firstzero = None
        if firstzero is None:
            items = self[::-1]
            del self[:]
        else:
            items = self[-1:firstzero:-1]
            del self[firstzero:]
        return ''.join(map(chr, items))

    def pop_vector(self, n):
        assert n > 0
        result = self[-n:]
        del self[-n:]
        if len(result) < n:
            result = [0] * (n - len(result)) + result
        return result

    def rdiscard(self, n=1):
        assert n >= 0
        del self[:n]

    def rpop(self):
        try:
            return list.pop(self, 0)
        except IndexError:
            return 0

    def rpopmany(self, n):
        assert n > 0
        result = self[:n]
        del self[:n]
        if len(result) < n:
            result.extend([0] * (n - len(result)))
        return result

    def rpop_string(self):
        try:
            firstzero = self.index(0)
        except ValueError:
            firstzero = len(self)
        items = self[:firstzero]
        del self[:firstzero+1]
        return ''.join(map(chr, items))

    def rpop_vector(self, n):
        assert n > 0
        result = self[n-1::-1]
        del self[:n]
        if len(result) < n:
            result = [0] * (n - len(result)) + result
        return result

    def clear(self):
        del self[:]

class StackStack(object):
    def __init__(self):
        self.sstack = [Stack()]
        self.invertmode = self.queuemode = False

    def __len__(self):
        return len(self.sstack)

    def _get_invertmode(self):
        return self._invertmode

    def _set_invertmode(self, flag):
        if flag:
            self._invertmode = True
            self.push = self._rpush
            self.pushmany = self._rpushmany
            self.push_string = self._rpush_string
            self.push_vector = self._rpush_vector
        else:
            self._invertmode = False
            self.push = self._push
            self.pushmany = self._pushmany
            self.push_string = self._push_string
            self.push_vector = self._push_vector

    invertmode = property(_get_invertmode, _set_invertmode)

    def _get_queuemode(self):
        return self._queuemode

    def _set_queuemode(self, flag):
        if flag:
            self._queuemode = True
            self.discard = self._rdiscard
            self.pop = self._rpop
            self.popmany = self._rpopmany
            self.pop_string = self._rpop_string
            self.pop_vector = self._rpop_vector
        else:
            self._queuemode = False
            self.discard = self._discard
            self.pop = self._pop
            self.popmany = self._popmany
            self.pop_string = self._pop_string
            self.pop_vector = self._pop_vector

    queuemode = property(_get_queuemode, _set_queuemode)

    def __getitem__(self, key):
        return self.sstack[key]

    def __getattr__(self, name):
        return getattr(self.sstack, name)

    def push_stack(self):
        self.sstack.append(Stack())

    def pop_stack(self):
        self.sstack.pop()

    def push(self, item, stack=TOSS): raise NotImplemented()
    def pushmany(self, items, stack=TOSS): raise NotImplemented()
    def push_string(self, s, stack=TOSS): raise NotImplemented()
    def push_vector(self, v, stack=TOSS): raise NotImplemented()

    def _push(self, item, stack=TOSS): self.sstack[stack].push(item)
    def _pushmany(self, items, stack=TOSS): return self.sstack[stack].pushmany(items)
    def _push_string(self, s, stack=TOSS): self.sstack[stack].push_string(s)
    def _push_vector(self, v, stack=TOSS): self.sstack[stack].push_vector(v)

    def _rpush(self, item, stack=TOSS): self.sstack[stack].rpush(item)
    def _rpushmany(self, items, stack=TOSS): return self.sstack[stack].rpushmany(items)
    def _rpush_string(self, s, stack=TOSS): self.sstack[stack].rpush_string(s)
    def _rpush_vector(self, v, stack=TOSS): self.sstack[stack].rpush_vector(v)

    def discard(self, n=1, stack=TOSS): raise NotImplemented()
    def pop(self, stack=TOSS): raise NotImplemented()
    def popmany(self, n, stack=TOSS): raise NotImplemented()
    def pop_string(self, stack=TOSS): raise NotImplemented()
    def pop_vector(self, n, stack=TOSS): raise NotImplemented()

    def _discard(self, n=1, stack=TOSS): self.sstack[stack].discard(n)
    def _pop(self, stack=TOSS): return self.sstack[stack].pop()
    def _popmany(self, n, stack=TOSS): return self.sstack[stack].popmany(n)
    def _pop_string(self, stack=TOSS): return self.sstack[stack].pop_string()
    def _pop_vector(self, n, stack=TOSS): return self.sstack[stack].pop_vector(n)

    def _rdiscard(self, n=1, stack=TOSS): self.sstack[stack].rdiscard(n)
    def _rpop(self, stack=TOSS): return self.sstack[stack].rpop()
    def _rpopmany(self, n, stack=TOSS): return self.sstack[stack].rpopmany(n)
    def _rpop_string(self, stack=TOSS): return self.sstack[stack].rpop_string()
    def _rpop_vector(self, n, stack=TOSS): return self.sstack[stack].rpop_vector(n)

    def copy(self):
        obj = StackStack()
        obj.sstack = [Stack(st[:]) for st in self.sstack]
        obj.invertmode = self.invertmode
        obj.queuemode = self.queuemode
        return obj

