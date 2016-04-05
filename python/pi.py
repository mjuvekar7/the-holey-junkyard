class lft:
    def __init__(self, a, b, c, d):
        self.q = a
        self.r = b
        self.s = c
        self.t = d

    def extr(self, x):
        return (self.q*x + self.r)/(self.s*x + self.t)

def comp(a, b):
    return lft(a.q*b.q + a.r*b.s, a.q*b.r + a.r*b.t,
               a.s*b.q + a.t*b.s, a.s*b.r + a.t*b.t)

def stream(nexte, safe, prod, cons, z, nums):
    while True:
        y = nexte(z)
        if safe(z, y):
            z = prod(z, y)
            yield y
        z = cons(z, next(nums))

class lfts:
    k = 1

    def __iter__(self):
        return self

    def __next__(self):
        res = lft(self.k, 4*self.k+2, 0, 2*self.k+1)
        self.k += 1
        return res

class lfts_again():
    i = 1

    def __iter__(self):
        return self

    def __next__(self):
        j = 3 * (3*self.i+1) * (3*self.i+2)
        res = lft(self.i*(2*self.i-1), j*(5*self.i-2), 0, j)
        self.i += 1
        return res

def get_pi():
    num = 0
    for dig in stream(lambda z: int(z.extr(3)), lambda z, n: n == int(z.extr(4)),
                      lambda z, n: comp(lft(10, -10*n, 0, 1), z), comp, 
                      lft(1, 0, 0, 1), lfts()):
        print(dig)
        num += 1
        if num == 1000:
            break

# 5 times faster
def get_pi_again(out):
#    num = 0
    for dig in stream(lambda zi: (zi[0].q*(27*zi[1]+15) + 5*zi[0].r) // (zi[0].s*(27*zi[1]+15) + 5*zi[0].t),
#                      lambda zi, n: n == (zi[0].q*(675*zi[1]-216)+125*zi[0].r) // (zi[0].s*(675*zi[1]-216)+125*zi[0].t),
                      lambda zi, n: True,
                      lambda zi, n: (comp(lft(10, -10*n, 0, 1), zi[0]), zi[1]),
                      lambda zi, zz: (comp(zi[0], zz), zi[1]+1),
                      (lft(1, 0, 0, 1), 1), lfts_again()):
        out.write(str(dig))
#        num += 1
#        if num == 1000:
#            break
