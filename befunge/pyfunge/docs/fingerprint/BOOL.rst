.. _BOOL:

``"BOOL"`` Logic functions
-----------------------------

:Fingerprint ID: 0x424f4f4c

This fingerprint, from `RC/Funge-98`__, implements bitwise operations over integer. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#BOOL

``A`` : *a* *b* --- *(a AND b)*
    Performs bitwise AND.

``N`` : *a* --- *(NOT a)*
    Performs bitwise negation.

``O`` : *a* *b* --- *(a OR b)*
    Performs bitwise OR.

``X`` : *a* *b* --- *(a XOR b)*
    Performs bitwise exclusive OR.

PyFunge assumes the arguments to be two's complement representation. Thus ``N`` is actually same to ``0\-1-``.

