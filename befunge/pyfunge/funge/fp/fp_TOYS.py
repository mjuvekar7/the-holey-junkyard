from funge.stack import TOSS
from funge.vector import Vector
from funge.fingerprint import Fingerprint

import random
import operator

class TOYS(Fingerprint):
    'Funge-98 Standard Toys'

    API = 'PyFunge v2'
    ID = 0x544f5953

    @Fingerprint.register('A')
    def gable(self, ip):
        n, c = ip.popmany(2)
        for i in xrange(n):
            ip.push(c)

    @Fingerprint.register('B')
    def pair_of_shoes(self, ip): # uncertain
        a, b = ip.popmany(2)
        ip.push(a + b)
        ip.push(a - b)

    @Fingerprint.register('C')
    def bracelet(self, ip):
        if self.dimension != 2:
            self.reflect(ip) # TODO

        destination = ip.pop_vector()
        size = ip.pop_vector()
        source = ip.pop_vector()

        get = ip.space.get
        put = ip.space.put
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                put((destination[0]+x, destination[1]+y), get((source[0]+x, source[1]+y)))

    @Fingerprint.register('D')
    def toilet_seat(self, ip):
        ip.push(ip.pop() - 1)

    @Fingerprint.register('E')
    def pitchfork_head(self, ip):
        sum = reduce(operator.add, ip.stack[TOSS], 0)
        ip.stack[TOSS].clear()
        ip.push(sum)

    @Fingerprint.register('F')
    def calipers(self, ip):
        if self.dimension != 2:
            self.reflect(ip)

        target = ip.pop_vector()
        nrows, ncolumns = ip.popmany(2) # XXX vague specification

        put = ip.space.put
        pop = ip.pop
        for y in xrange(nrows):
            for x in xrange(ncolumns):
                put((target[0]+x, target[1]+y), pop())

    @Fingerprint.register('G')
    def counterclockwise(self, ip):
        if self.dimension != 2:
            self.reflect(ip)

        target = ip.pop_vector()
        nrows, ncolumns = ip.popmany(2) # XXX vague specification

        get = ip.space.get
        push = ip.push
        for y in xrange(nrows-1, -1, -1):
            for x in xrange(ncolumns-1, -1, -1):
                push(get((target[0]+x, target[1]+y)))

    @Fingerprint.register('H')
    def pair_of_stilts(self, ip):
        b, a = ip.popmany(2)
        if b > 0:
            ip.push(a << b)
        elif b < 0:
            ip.push(a >> (-b))
        else:
            ip.push(a)

    @Fingerprint.register('I')
    def doric_column(self, ip):
        ip.push(ip.pop() + 1)

    @Fingerprint.register('J')
    def fishhook(self, ip):
        offset = ip.pop()
        replace = ip.position.replace
        get = ip.space.get
        put = ip.space.put
        if offset > 0:
            for y in xrange(ip.space.boundmax[1], ip.space.boundmin[1]-1, -1):
                put(replace(_1=y+offset), get(replace(_1=y)))
            for y in xrange(ip.space.boundmin[1]+offset, ip.space.boundmin[1]-1, -1):
                put(replace(_1=y), 32)
        elif offset < 0:
            for y in xrange(ip.space.boundmin[1], ip.space.boundmax[1]+1):
                put(replace(_1=y+offset), get(replace(_1=y)))
            for y in xrange(ip.space.boundmax[1]-offset+1, ip.space.boundmax[1]+1):
                put(replace(_1=y), 32)

    @Fingerprint.register('K')
    def scissors(self, ip):
        if self.dimension != 2:
            self.reflect(ip) # TODO

        destination = ip.pop_vector()
        size = ip.pop_vector()
        source = ip.pop_vector()

        get = ip.space.get
        put = ip.space.put
        for x in xrange(size[0]-1, -1, -1):
            for y in xrange(size[1]-1, -1, -1):
                put((destination[0]+x, destination[1]+y), get((source[0]+x, source[1]+y)))

    @Fingerprint.register('L')
    def corner(self, ip):
        lefthand = ip.position + ip.delta.replace(ip.delta[1], -ip.delta[0])
        ip.push(ip.space.get(lefthand))

    @Fingerprint.register('M')
    def kittycat(self, ip):
        if self.dimension != 2:
            self.reflect(ip) # TODO

        destination = ip.pop_vector()
        size = ip.pop_vector()
        source = ip.pop_vector()

        get = ip.space.get
        put = ip.space.put
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                put((destination[0]+x, destination[1]+y), get((source[0]+x, source[1]+y)))
                put((source[0]+x, source[1]+y), 32)

    @Fingerprint.register('N')
    def lightning_bolt(self, ip):
        ip.push(-ip.pop())

    @Fingerprint.register('O')
    def boulder(self, ip):
        offset = ip.pop()
        replace = ip.position.replace
        get = ip.space.get
        put = ip.space.put
        if offset > 0:
            for x in xrange(ip.space.boundmax[0], ip.space.boundmin[0]-1, -1):
                put(replace(_0=x+offset), get(replace(_0=x)))
            for y in xrange(ip.space.boundmin[0]+offset, ip.space.boundmin[0]-1, -1):
                put(replace(_0=y), 32)
        elif offset < 0:
            for x in xrange(ip.space.boundmin[0], ip.space.boundmax[0]+1):
                put(replace(_0=x+offset), get(replace(_0=x)))
            for y in xrange(ip.space.boundmax[0]-offset+1, ip.space.boundmax[0]+1):
                put(replace(_0=y), 32)

    @Fingerprint.register('P')
    def mailbox(self, ip):
        prod = reduce(operator.mul, ip.stack[TOSS], 1)
        ip.stack[TOSS].clear()
        ip.push(prod)

    @Fingerprint.register('Q')
    def necklace(self, ip):
        ip.space.put(ip.position - ip.delta, ip.pop())

    @Fingerprint.register('R')
    def can_opener(self, ip):
        righthand = ip.position + ip.delta.replace(-ip.delta[1], ip.delta[0])
        ip.push(ip.space.get(righthand))

    @Fingerprint.register('S')
    def chicane(self, ip):
        if self.dimension != 2:
            self.reflect(ip) # TODO

        destination = ip.pop_vector()
        size = ip.pop_vector()
        value = ip.pop()

        put = ip.space.put
        for x in xrange(size[0]):
            for y in xrange(size[1]):
                put((destination[0]+x, destination[1]+y), value)

    @Fingerprint.register('T')
    def barstool(self, ip):
        d, x = ip.popmany(2)
        if 0 <= d < ip.dimension:
            vec = [0] * ip.dimension
            vec[d] = x and -1 or 1
            ip.delta = Vector(vec)
        else:
            self.reflect(ip)

    @Fingerprint.register('U')
    def tumbler(self, ip):
        # XXX will be problem for other semantics
        index = random.randint(0, len(self.random_deltas)-1)
        ip.space.put(ip.position, [60, 62, 94, 118, 104, 108][index])
        ip.delta = self.random_deltas[index]

    @Fingerprint.register('V')
    def dixiecup(self, ip):
        if self.dimension != 2:
            self.reflect(ip) # TODO

        destination = ip.pop_vector()
        size = ip.pop_vector()
        source = ip.pop_vector()

        get = ip.space.get
        put = ip.space.put
        for x in xrange(size[0]-1, -1, -1):
            for y in xrange(size[1]-1, -1, -1):
                put((destination[0]+x, destination[1]+y), get((source[0]+x, source[1]+y)))
                put((source[0]+x, source[1]+y), 32)

    @Fingerprint.register('W')
    def television_antenna(self, ip):
        target = ip.pop_vector()
        value = ip.pop()
        actual = ip.space.get(target)
        if actual < value:
            ip.push(value)
            ip.push_vector(target)
            ip.position -= ip.delta
        elif actual > value:
            self.reflect(ip)

    @Fingerprint.register('X')
    def buried_treasure(self, ip):
        ip.position = ip.position.replace(_0=ip.position[0]+1)

    @Fingerprint.register('Y')
    def slingshot(self, ip):
        if ip.dimension > 1:
            ip.position = ip.position.replace(_1=ip.position[1]+1)
        else:
            self.reflect(ip)

    @Fingerprint.register('Z')
    def barn_door(self, ip):
        if ip.dimension > 2:
            ip.position = ip.position.replace(_2=ip.position[2]+1)
        else:
            self.reflect(ip)

