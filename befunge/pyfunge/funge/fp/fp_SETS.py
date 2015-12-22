from funge.stack import TOSS
from funge.fingerprint import Fingerprint

def pop_set(ip):
    # strangely enough, a set doesn't obey normal rules of stack operation.
    if not ip.stack[TOSS]:
        raise ValueError # stack underflown
    n = ip.pop()
    if n == 0:
        return set()
    elif not 0 <= n <= len(ip.stack[TOSS]):
        raise ValueError # stack underflown
    items = ip.popmany(n)
    itemsset = set(items)
    if len(items) != len(itemsset):
        raise ValueError # invalid set
    return itemsset

def push_set(ip, items):
    ip.pushmany(list(items))
    ip.push(len(items))

class SETS(Fingerprint):
    'Set operations'

    API = 'PyFunge v2'
    ID = 0x53455453

    @Fingerprint.register('A')
    def add(self, ip):
        v = ip.pop()
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            set.add(v)
            push_set(ip, set)

    @Fingerprint.register('C')
    def count(self, ip):
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, set)
            ip.push(len(set))

    @Fingerprint.register('D')
    def duplicate(self, ip):
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, set)
            push_set(ip, set)

    @Fingerprint.register('G')
    def get(self, ip):
        source = ip.pop_vector()
        delta = ip.pop_vector()
        n = ip.space.get(source)
        if n < 0:
            self.reflect(ip)
        else:
            items = []
            for i in xrange(n):
                source += delta
                items.append(ip.space.get(source))
            if len(set(items)) != len(items):
                self.reflect(ip)
            else:
                push_set(ip, items)

    @Fingerprint.register('I')
    def intersection(self, ip):
        try:
            setb = pop_set(ip)
            seta = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, seta)
            push_set(ip, setb)
            push_set(ip, seta & setb)

    @Fingerprint.register('M')
    def membership(self, ip):
        v = ip.pop()
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, set)
            if v in set:
                ip.push(1)
            else:
                ip.push(0)

    @Fingerprint.register('P')
    def output(self, ip):
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, set)
            self.platform.putstr('{%s}' % ','.join(map(str, sorted(set))))

    @Fingerprint.register('R')
    def remove(self, ip):
        v = ip.pop()
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            set.discard(v)
            push_set(ip, set)

    @Fingerprint.register('S')
    def subtract(self, ip):
        try:
            setb = pop_set(ip)
            seta = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, seta)
            push_set(ip, setb)
            push_set(ip, seta - setb)

    @Fingerprint.register('U')
    def union(self, ip):
        try:
            setb = pop_set(ip)
            seta = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, seta)
            push_set(ip, setb)
            push_set(ip, seta | setb)

    @Fingerprint.register('W')
    def write(self, ip):
        destination = ip.pop_vector()
        delta = ip.pop_vector()
        try:
            set = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, set)
            ip.space.put(destination, len(set))
            for item in set:
                destination += delta
                ip.space.put(destination, item)

    @Fingerprint.register('X')
    def exchange(self, ip):
        try:
            setb = pop_set(ip)
            seta = pop_set(ip)
        except ValueError:
            self.reflect(ip)
        else:
            push_set(ip, setb)
            push_set(ip, seta)

    @Fingerprint.register('Z')
    def discard(self, ip):
        try:
            pop_set(ip)
        except ValueError:
            self.reflect(ip)

