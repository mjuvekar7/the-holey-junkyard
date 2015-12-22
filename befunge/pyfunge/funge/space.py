"""Implementation of Funge space.

Funge-98 space is conceptually N-dimensional grid with walkaround semantics,
called Lahey-space. Befunge-93 space is a subset of Funge-98 space, which have
explicit boundary from (0,0) to (79,23).
"""

from itertools import izip, count

from funge.exception import *
from funge.vector import Vector

class Space(object):
    """Lahey-space implementation."""

    def __init__(self, dimension, default=32):
        assert dimension >= 1

        self.dimension = dimension
        self.space = {}
        self.default = default

        self.boundmin = None
        self.boundmax = None

        self.rectcount = [{} for i in xrange(dimension)]
        self.rectchanged = False

    def get(self, pos):
        try:
            return self.space[pos]
        except KeyError:
            return self.default

    def put(self, pos, char, update_bounds=True):
        prevpresent = pos in self.space

        if char == self.default:
            try:
                del self.space[pos]
            except Exception:
                pass

            if prevpresent:
                for i in xrange(self.dimension):
                    self.rectcount[i][pos[i]] -= 1
                self.rectchanged = True
        else:
            self.space[pos] = char

            if not prevpresent:
                for i in xrange(self.dimension):
                    try:
                        self.rectcount[i][pos[i]] += 1
                    except KeyError:
                        self.rectcount[i][pos[i]] = 1

                if update_bounds:
                    boundmax = self.boundmax
                    if boundmax is None:
                        self.boundmax = Vector(pos)
                    else:
                        self.boundmax = boundmax.pairwise_max(pos)

                    boundmin = self.boundmin
                    if boundmin is None:
                        self.boundmin = Vector(pos)
                    else:
                        self.boundmin = boundmin.pairwise_min(pos)

                    if boundmax != self.boundmax or boundmin != self.boundmin:
                        self.rectchanged = True

    def getspace(self, pos, size, rtrim=True):
        dimension = self.dimension
        get = self.space.get
        if dimension == 1:
            rangex = xrange(pos[0], pos[0]+size[0])
            if rtrim:
                return ''.join(chr(get((x,), 32)) for x in rangex).rstrip(' ')
            else:
                return ''.join(chr(get((x,), 32)) for x in rangex)
        elif dimension == 2:
            rangex = xrange(pos[0], pos[0]+size[0])
            rangey = xrange(pos[1], pos[1]+size[1])
            if rtrim:
                return '\n'.join(
                    ''.join(chr(get((x,y), 32)) for x in rangex).rstrip(' ')
                    for y in rangey).rstrip('\n')
            else:
                return '\n'.join(
                    ''.join(chr(get((x,y), 32)) for x in rangex)
                    for y in rangey)
        elif dimension == 3:
            rangex = xrange(pos[0], pos[0]+size[0])
            rangey = xrange(pos[1], pos[1]+size[1])
            rangez = xrange(pos[2], pos[2]+size[2])
            if rtrim:
                return '\f'.join(
                    '\n'.join(
                        ''.join(chr(get((x,y,z), 32)) for x in rangex).rstrip(' ')
                        for y in rangey).rstrip('\n')
                    for z in rangez).rstrip('\f')
            else:
                return '\f'.join(
                    '\n'.join(
                        ''.join(chr(get((x,y,z), 32)) for x in rangex)
                        for y in rangey)
                    for z in rangez)
        else:
            raise NotImplemented

    def putspace(self, pos, str):
        dimension = self.dimension
        put = self.put

        if dimension >= 3:
            x = mx = pos[0]
            y = my = pos[1]
            z = pos[2]
            more = pos[3:]
            for plane in str.split('\f'):
                for line in plane.splitlines():
                    for ch in line:
                        if ch != ' ': put((x, y, z) + more, ord(ch), False)
                        x += 1
                    if mx < x: mx = x
                    y += 1
                    x = pos[0]
                if my < y: my = y
                z += 1
                y = pos[1]

            self.notifyrect(pos, (mx - 1, my - 1, z - 1) + more)
            return Vector([mx - pos[0], my - pos[1], z - pos[2]] + [1] * (dimension - 3))

        str = str.replace('\f', '')
        if dimension >= 2:
            x = mx = pos[0]
            y = pos[1]
            for line in str.splitlines():
                for ch in line:
                    if ch != ' ': put((x, y), ord(ch), False)
                    x += 1
                if mx < x: mx = x
                y += 1
                x = pos[0]

            self.notifyrect(pos, (mx - 1, y - 1))
            return Vector([mx - pos[0], y - pos[1]])

        str = str.replace('\r\n', '').replace('\r', '').replace('\n', '')
        if dimension >= 1:
            x = pos[0]
            for ch in str:
                if ch != ' ': put((x,), ord(ch), False)
                x += 1

            self.notifyrect(pos, (x - 1,))
            return Vector([x - pos[0]])

        assert False, 'invalid dimension'

    def getrect(self):
        if self.rectchanged:
            rectmin = []
            rectmax = []
            for count in self.rectcount:
                nonemptylines = [k for k,v in count.items() if v > 0]
                rectmin.append(min(nonemptylines))
                rectmax.append(max(nonemptylines))
            self.boundmin = Vector(rectmin)
            self.boundmax = Vector(rectmax)
            self.rectchanged = False

        return self.boundmin, self.boundmax

    def notifyrect(self, minpos, maxpos):
        boundmax = self.boundmax
        if boundmax is None:
            self.boundmax = Vector(maxpos)
        else:
            self.boundmax = boundmax.pairwise_max(maxpos)

        boundmin = self.boundmin
        if boundmin is None:
            self.boundmin = Vector(minpos)
        else:
            self.boundmin = boundmin.pairwise_min(minpos)

        if boundmax != self.boundmax or boundmin != self.boundmin:
            self.rectchanged = True

    def normalize(self, position, delta):
        boundmin = self.boundmin
        boundmax = self.boundmax

        for i in xrange(self.dimension):
            if not boundmin[i] <= position[i] <= boundmax[i]: break
        else:
            return position # nothing to do

        # find out maximum backstep which locates IP to other edges.
        # i.e. find maximum k such that boundmin <= IP - k * delta <= boundmax
        backsteps = []
        for i in xrange(self.dimension):
            if delta[i] > 0:
                backsteps.append((position[i] - boundmin[i]) // delta[i])
            elif delta[i] < 0:
                backsteps.append((position[i] - boundmax[i]) // delta[i])

        assert backsteps
        return position - min(backsteps) * delta

    def scanuntil(self, position, delta, value):
        try:
            cell = self.space[position]
        except KeyError:
            cell = self.default

        if cell != value:
            space = self.space
            default = self.default
            boundmin = self.boundmin
            boundmax = self.boundmax
            dimrange = range(self.dimension)
            normalize = self.normalize

            while cell != value:
                position += delta
                for i in dimrange:
                    if not boundmin[i] <= position[i] <= boundmax[i]:
                        position = normalize(position, delta)
                        break

                try:
                    cell = space[position]
                except KeyError:
                    cell = default

        return position

    def scanwhile(self, position, delta, value):
        try:
            cell = self.space[position]
        except KeyError:
            cell = self.default

        if cell == value:
            space = self.space
            default = self.default
            boundmin = self.boundmin
            boundmax = self.boundmax
            dimrange = range(self.dimension)
            normalize = self.normalize

            while cell == value:
                position += delta
                for i in dimrange:
                    if not boundmin[i] <= position[i] <= boundmax[i]:
                        position = normalize(position, delta)
                        break

                try:
                    cell = space[position]
                except KeyError:
                    cell = default

        return position

class BoundedSpace(Space):
    def __init__(self, dimension, rectmin, rectmax, default=32):
        Space.__init__(self, dimension, default)
        self.rectmin = Vector(rectmin)
        self.rectmax = Vector(rectmax)

    def check_position(self, pos):
        for x in xrange(0, self.dimension):
            if not self.rectmin[x] <= pos[x] <= self.rectmax[x]: return False
        return True

    def get(self, pos):
        if self.check_position(pos):
            return Space.get(self, pos)
        else:
            return self.default

    def put(self, pos, char, update_bounds=True):
        if self.check_position(pos):
            Space.put(self, pos, char, update_bounds)

    def normalize(self, position, delta):
        return Vector([rmin + (pos - rmin) % (rmax - rmin + 1) for pos, rmin, rmax
                in zip(position, self.rectmin, self.rectmax)])

class Befunge93Space(BoundedSpace):
    def __init__(self, width=80, height=25):
        BoundedSpace.__init__(self, 2, (0, 0), (width-1, height-1))

    def put(self, pos, char, update_bounds=True):
        BoundedSpace.put(self, pos, char & 0xff, update_bounds)

