from funge.fingerprint import Fingerprint
from funge.fp.fp_FPSP import pop_float, push_float

import math
from struct import pack, unpack

def pop_vector3(ip):
    z = pop_float(ip)
    y = pop_float(ip)
    x = pop_float(ip)
    return (x, y, z)

def push_vector3(ip, (x, y, z)):
    push_float(ip, x)
    push_float(ip, y)
    push_float(ip, z)

def read_matrix4(ip, pos):
    matrix = []
    for y in xrange(4):
        row = []
        for x in xrange(4):
            value = ip.space.get(pos.replace(pos[0]+x, pos[1]+y))
            row.append(unpack('f', pack('I', value & 0xffffffff))[0])
        matrix.append(row)
    return matrix

def write_matrix4(ip, pos, matrix):
    for y in xrange(4):
        for x in xrange(4):
            value = unpack('i', pack('f', matrix[y][x]))[0]
            ip.space.put(pos.replace(pos[0]+x, pos[1]+y), value)

class ThreeDSP(Fingerprint):
    '3D space manipulation extension'

    API = 'PyFunge v2'
    ID = 0x33445350

    @Fingerprint.register('A')
    def vec_add(self, ip):
        b = pop_vector3(ip)
        a = pop_vector3(ip)
        push_vector3(ip, (a[0]+b[0], a[1]+b[1], a[2]+b[2]))

    @Fingerprint.register('B')
    def vec_subtract(self, ip):
        b = pop_vector3(ip)
        a = pop_vector3(ip)
        push_vector3(ip, (a[0]-b[0], a[1]-b[1], a[2]-b[2]))

    @Fingerprint.register('C')
    def vec_crossprod(self, ip):
        b = pop_vector3(ip)
        a = pop_vector3(ip)
        push_vector3(ip, (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]))

    @Fingerprint.register('D')
    def vec_dotprod(self, ip):
        b = pop_vector3(ip)
        a = pop_vector3(ip)
        push_float(ip, a[0]*b[0] + a[1]*b[1] + a[2]*b[2])

    @Fingerprint.register('L')
    def vec_length(self, ip):
        a = pop_vector3(ip)
        push_float(ip, (a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) ** 0.5)

    @Fingerprint.register('M')
    def vec_multiply(self, ip):
        b = pop_vector3(ip)
        a = pop_vector3(ip)
        push_vector3(ip, (a[0]*b[0], a[1]*b[1], a[2]*b[2]))

    @Fingerprint.register('N')
    def vec_normalize(self, ip):
        a = pop_vector3(ip)
        norm = (a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) ** 0.5
        if norm == 0:
            push_vector3(ip, a)
        else:
            push_vector3(ip, (a[0]/norm, a[1]/norm, a[2]/norm))

    @Fingerprint.register('P')
    def vec_copy(self, ip):
        source = ip.pop_vector()
        destination = ip.pop_vector()
        write_matrix4(ip, destination, read_matrix4(ip, source))

    @Fingerprint.register('R')
    def vec_gen_rotate(self, ip):
        angle = pop_float(ip) * math.pi / 180
        axis = ip.pop()
        target = ip.pop_vector()

        s = math.sin(angle)
        c = math.cos(angle)
        if axis == 1:
            write_matrix4(ip, target,
                    [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])
        elif axis == 2:
            write_matrix4(ip, target,
                    [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])
        elif axis == 3:
            write_matrix4(ip, target,
                    [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        else:
            self.reflect(ip)

    @Fingerprint.register('S')
    def vec_gen_scale(self, ip):
        scale = pop_vector3(ip)
        target = ip.pop_vector()
        write_matrix4(ip, target,
                [[scale[0], 0, 0, 0], [0, scale[1], 0, 0, 0],
                 [0, 0, scale[2], 0], [0, 0, 0, 1]])

    @Fingerprint.register('T')
    def vec_gen_translate(self, ip):
        translate = pop_vector3(ip)
        target = ip.pop_vector()
        write_matrix4(ip, target,
                [[1, 0, 0, translate[0]], [0, 1, 0, translate[1]],
                 [0, 0, 1, translate[2]], [0, 0, 0, 1]])

    @Fingerprint.register('U')
    def vec_duplicate(self, ip):
        a = pop_vector3(ip)
        push_vector3(ip, a)
        push_vector3(ip, a)

    @Fingerprint.register('V')
    def vec_project(self, ip):
        a = pop_vector3(ip)
        if a[2] == 0:
            push_float(ip, a[0])
            push_float(ip, a[1])
        else:
            push_float(ip, a[0] / a[2])
            push_float(ip, a[1] / a[2])

    @Fingerprint.register('X')
    def vec_transform(self, ip):
        matrix = read_matrix4(ip, ip.pop_vector())
        vec = pop_vector3(ip)

        result = []
        for i in xrange(3):
            result.append(vec[0]*matrix[i][0] + vec[1]*matrix[i][1] + vec[2]*matrix[i][2] + matrix[i][3])
        push_vector3(ip, result)

    @Fingerprint.register('Y')
    def vec_multiply_matrix(self, ip):
        matrixb = read_matrix4(ip, ip.pop_vector())
        matrixa = read_matrix4(ip, ip.pop_vector())
        target = ip.pop_vector()

        matrix = []
        for y in xrange(4):
            row = []
            for x in xrange(4):
                row.append(matrixb[y][0]*matrixa[0][x] + matrixb[y][1]*matrixa[1][x] +
                           matrixb[y][2]*matrixa[2][x] + matrixb[y][3]*matrixa[3][x])
            matrix.append(row)
        write_matrix4(ip, target, matrix)

    @Fingerprint.register('Z')
    def vec_scale(self, ip):
        a = pop_vector3(ip)
        n = pop_float(ip)
        push_vector3(ip, (a[0]*n, a[1]*n, a[2]*n))

