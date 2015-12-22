.. _FPDP:
.. _FPSP:

``"FPDP"`` Double precision floating point and ``"FPSP"`` Single precision floating point
-------------------------------------------------------------------------------------------

:Fingerprint ID: 0x46504450 (FPDP) and 0x46505350 (FPSP)

These fingerprints, from `RC/Funge-98`__, implement operations on single and double precision floating point number. Single precision floating point number occupies one stack cell, while double precision occupies two stack cells. They provide the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#FPSP

``A`` : *x*\ :sup:`fp` *y*\ :sup:`fp` --- *(x+y)*\ :sup:`fp`
    Adds two floating point numbers.

``B`` : *x*\ :sup:`fp` --- *sin(x)*\ :sup:`fp`
    Calculates sine of floating point number.

``C`` : *x*\ :sup:`fp` --- *cos(x)*\ :sup:`fp`
    Calculates cosine of floating point number.

``D`` : *x*\ :sup:`fp` *y*\ :sup:`fp` --- *(x÷y)*\ :sup:`fp`
    Divides two floating point numbers.

``E`` : *x*\ :sup:`fp` --- *arcsin(x)*\ :sup:`fp`
    Calculates arcsine of floating point number.

``F`` : *n* --- *x*\ :sup:`fp`
    Converts integer to floating point number.

``G`` : *x*\ :sup:`fp` --- *arctan(x)*\ :sup:`fp`
    Calculates arctangent of floating point number.

``H`` : *x*\ :sup:`fp` --- *arccos(x)*\ :sup:`fp`
    Calculates arccosine of floating point number.

``I`` : *x*\ :sup:`fp` --- *n*
    Converts floating point number to integer, discarding the fraction part.

``K`` : *x*\ :sup:`fp` --- *log(x)*\ :sup:`fp`
    Calculates natural logarithm of floating point number.

``L`` : *x*\ :sup:`fp` --- *log10(x)*\ :sup:`fp`
    Calculates common (base 10) logarithm of floating point number.

``M`` : *x*\ :sup:`fp` *y*\ :sup:`fp` --- *(x×y)*\ :sup:`fp`
    Multiplies two floating point numbers.

``N`` : *x*\ :sup:`fp` --- *-x*\ :sup:`fp`
    Negates floating point number.

``P`` : *x*\ :sup:`fp` ---
    Prints floating point number.

``Q`` : *x*\ :sup:`fp` --- *sqrt(x)*\ :sup:`fp`
    Calculates the square root of floating point number.

``S`` : *x*\ :sup:`fp` *y*\ :sup:`fp` --- *(x-y)*\ :sup:`fp`
    Subtracts two floating point numbers.

``T`` : *x*\ :sup:`fp` --- *tan(x)*\ :sup:`fp`
    Calculates tangent of floating point number.

``V`` : *x*\ :sup:`fp` --- *abs(x)*\ :sup:`fp`
    Calculates the absolute value of floating point number.

``X`` : *x*\ :sup:`fp` --- *exp(x)*\ :sup:`fp`
    Calculates the exponential of floating point number.

``Y`` : *x*\ :sup:`fp` *y*\ :sup:`fp` --- *(x^y)*\ :sup:`fp`
    Raises *y* to the power of *x*.

In PyFunge these single and double precision floating point number are implemented as IEEE 754 single precision (32-bit) and double precision (64-bit) format. A single precision number occupies one cell, and a double precision number occupies two cells for lower and upper 32 bits, in the unspecified (endian-specific) order. PyFunge ignores all bits except the lowermost 32 bits for such cells.

The precise operations on floating point numbers are done as specified in IEEE 754. So it correctly handles infinities and NaNs (Not a Number).

