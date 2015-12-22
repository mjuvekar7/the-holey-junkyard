.. _LONG:

``"LONG"`` Long Integers
----------------------------

:Fingerprint ID: 0x4c4f4e47

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements arithmetic operations of the long integers. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#LONG

``A`` : *a*\ :sup:`L` *b*\ :sup:`L` --- *(a+b)*\ :sup:`L`
    Adds two long integers.

``B`` : *x*\ :sup:`L` --- *abs(x)*\ :sup:`L`
    Calculates the absolute value of *x*.

``D`` : *a*\ :sup:`L` *b*\ :sup:`L` --- *(a÷b)*\ :sup:`L`
    Divides two long integers. If the divisor is zero it pushes zero. PyFunge tries to emulate RC/Funge-98's behavior as much as possible, so it uses C-like division (remainder's sign is same to dividend's one) instead of Python division.

``E`` : *x* --- *x*\ :sup:`L`
    Pushes a long integer from given integer.

``L`` : *a*\ :sup:`L` *n* --- *(a << n)*\ :sup:`L`
    Shift *a* left by *n* bits. Reflects if *n* is negative.

``M`` : *a*\ :sup:`L` *b*\ :sup:`L` --- *(a×b)*\ :sup:`L`
    Multiplies two long integers.

``N`` : *x*\ :sup:`L` --- *-x*\ :sup:`L`
    Negates the long integer.

``O`` : *a*\ :sup:`L` *b*\ :sup:`L` --- *(a mod b)*\ :sup:`L`
    Calculates the remainder of two long integers. If the divisor is zero it pushes zero. PyFunge tries to emulate RC/Funge-98's behavior as much as possible, so it uses C-like division (remainder's sign is same to dividend's one) instead of Python division.

``P`` : *x*\ :sup:`L` ---
    Prints the long integer.

``R`` : *a*\ :sup:`L` *n* --- *(a >> n)*\ :sup:`L`
    Shift *a* right by *n* bits. Reflects if *n* is negative.

``S`` : *a*\ :sup:`L` *b*\ :sup:`L` --- *(a-b)*\ :sup:`L`
    Subtracts two long integers.

``Z`` : *str*\ :sup:`s` --- *x*\ :sup:`L`
    Tries to parse the string into the long integer. Reflects on failure.

Long integer is not that long in PyFunge, since it is restricted to 64 bits. It can be useful for implicitly wrapping integers (as in C and other languages) though. Long integer occupies two stack cells: the bottom one is the upper 32 bits, and the top one is the lower 32 bits. All bits over 32 bit boundary are ignored.

