.. _FIXP:

``"FIXP"`` Some useful fixed point math functions
---------------------------------------------------

:Fingerprint ID: 0x46495850

This fingerprint, from `RC/Funge-98`__, implements fixed-point arithmetics. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#FIXP

``A`` : *a* *b* --- *(a AND b)*
    Performs bitwise AND.

``B`` : *(10000×n)* --- *(10000×arccos(n))*
    Calculates arccosine of *n*, in degrees. Reflects for invalid argument.

``C`` : *(10000×n)* --- *(10000×cos(n))*
    Calculates cosine of *n*, in degrees.

``D`` : *n* --- *x*
    Pushes a random number between 0 and *n*-1, or between *n* and -1 if *n* is negative.

``I`` : *(10000×n)* --- *(10000×sin(n))*
    Calculates sine of *n*, in degrees.

``J`` : *(10000×n)* --- *(10000×arcsin(n))*
    Calculates arcsine of *n*, in degrees. Reflects for invalid argument.

``N`` : *n* --- *-n*
    Pushes the negate of *n*.

``O`` : *a* *b* --- *(a OR b)*
    Performs bitwise OR.

``P`` : *n* --- *(π×n)*
    Pushes *n* multiplied by pi.

``Q`` : *n* --- *sqrt(n)*
    Pushes the square root of *n*. Reflects if *n* is negative.

``R`` : *a* *b* --- *a^b*
    Pushes the *b*-th power of *a*. Reflects if *a* and *b* are zero.

``S`` : *n* --- *sign(n)*
    Pushes +1 if *n* is positive, -1 if negative, or 0 if zero.

``T`` : *(10000×n)* --- *(10000×tan(n))*
    Calculates tangent of *n*, in degrees.

``U`` : *(10000×n)* --- *(10000×arctan(n))*
    Calculates arctangent of *n*, in degrees. Reflects for invalid argument.

``V`` : *n* --- *abs(n)*
    Pushes the absolute value of *n*.

``X`` : *a* *b* --- *(a XOR b)*
    Performs bitwise XOR.

All commands discards the fraction of result value, except that result value scaled by 10000 is rounded to nearest integer.

