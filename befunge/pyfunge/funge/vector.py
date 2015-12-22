"""Vector class, used for cordinates and so on.

Vector class is further optimized to use dimension-dependent cached class.
It speeds up the program 2x-3x faster.
"""

import operator

def create_vector_class(dimension):
    typename = 'Vector%d' % dimension
    template = '''
    class %(cls)s(tuple):
        __slots__ = ()
        @staticmethod
        def zero(dimension):
            assert dimension == %(dimension)d
            return %(cls)s((%(zeroexpr)s))
        def __add__(lhs, rhs):
            assert len(rhs) == %(dimension)d, 'different size of vector'
            return %(cls)s((%(addexpr)s))
        def __sub__(lhs, rhs):
            assert len(rhs) == %(dimension)d, 'different size of vector'
            return %(cls)s((%(subexpr)s))
        def __mul__(lhs, rhs):
            return %(cls)s((%(mulexpr)s))
        def __rmul__(rhs, lhs):
            return %(cls)s((%(rmulexpr)s))
        def __div__(lhs, rhs):
            return %(cls)s((%(divexpr)s))
        def __floordiv__(lhs, rhs):
            return %(cls)s((%(floordivexpr)s))
        def __mod__(lhs, rhs):
            return %(cls)s((%(modexpr)s))
        def __pos__(self):
            return self
        def __neg__(self):
            return %(cls)s((%(negexpr)s))
        def between(self, min, max):
            return %(betweenexpr)s
        def pairwise_min(lhs, rhs):
            assert len(rhs) == %(dimension)d, 'different size of vector'
            return %(cls)s((%(pairwiseminexpr)s))
        def pairwise_max(lhs, rhs):
            assert len(rhs) == %(dimension)d, 'different size of vector'
            return %(cls)s((%(pairwisemaxexpr)s))
        def replace(self, %(replargs)s):
            %(replpropagate)s
            return %(cls)s((%(replargsexpr)s))
        def __repr__(self):
            return '<%%s>' %% ', '.join(map(repr, self))
    '''.strip() % {
        'dimension': dimension,
        'cls': typename,
        'zeroexpr': '0,' * dimension,
        'addexpr': ''.join('lhs[%d]+rhs[%d],' % (i,i) for i in xrange(dimension)),
        'subexpr': ''.join('lhs[%d]-rhs[%d],' % (i,i) for i in xrange(dimension)),
        'mulexpr': ''.join('lhs[%d]*rhs,' % i for i in xrange(dimension)),
        'rmulexpr': ''.join('lhs*rhs[%d],' % i for i in xrange(dimension)),
        'divexpr': ''.join('lhs[%d]/rhs,' % i for i in xrange(dimension)),
        'floordivexpr': ''.join('lhs[%d]//rhs,' % i for i in xrange(dimension)),
        'modexpr': ''.join('lhs[%d]%%rhs,' % i for i in xrange(dimension)),
        'negexpr': ''.join('-self[%d],' % i for i in xrange(dimension)),
        'betweenexpr': ' and '.join('min[%d]<=self[%d]<=max[%d]' % (i,i,i)
                for i in xrange(dimension)),
        'pairwiseminexpr': ''.join('min(lhs[%d],rhs[%d]),' % (i,i)
                for i in xrange(dimension)),
        'pairwisemaxexpr': ''.join('max(lhs[%d],rhs[%d]),' % (i,i)
                for i in xrange(dimension)),
        'replargs': ','.join('_%d=None' % i for i in xrange(dimension)),
        'replpropagate': '\n            '.join('if _%d is None: _%d = self[%d]' % (i,i,i)
                for i in xrange(dimension)),
        'replargsexpr': ''.join('_%d,' % i for i in xrange(dimension)),
    }

    namespace = {'__name__': __name__}
    try:
        exec template in namespace
    except SyntaxError, err:
        raise SyntaxError(err.msg + ':\n' + template)
    return namespace[typename]

# XXX should really be customizable?
_vector_classes = [None, create_vector_class(1), create_vector_class(2), create_vector_class(3)]


class Vector(tuple):
    def __new__(cls, iterable):
        return _vector_classes[len(iterable)](iterable)

    @staticmethod
    def zero(dimension):
        return Vector((0,) * dimension)

