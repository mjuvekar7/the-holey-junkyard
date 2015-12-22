.. _CPLI:

``"CPLI"`` Complex Integer extension
---------------------------------------

:Fingerprint ID: 0x43504c49

This fingerprint, from `RC/Funge-98`__, implements arithmetics of Gaussian integers, that is complex integer whose real and imaginary part are both integers. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#CPLI

``A`` : *a* *b* *c* *d* --- *r* *i*
    Pushes (*a*\ +\ *b*\ i) + (*c*\ +\ *d*\ i).

``D`` : *a* *b* *c* *d* --- *r* *i*
    Pushes (*a*\ +\ *b*\ i) ÷ (*c*\ +\ *d*\ i). The fraction part of real and imaginary part is discarded. Reflects if *c* and *d* are both zero.

``M`` : *a* *b* *c* *d* --- *r* *i*
    Pushes (*a*\ +\ *b*\ i) × (*c*\ +\ *d*\ i).

``O`` : *a* *b* ---
    Prints a complex number *a*\ +\ *b*\ i.

``S`` : *a* *b* *c* *d* --- *r* *i*
    Pushes (*a*\ +\ *b*\ i) - (*c*\ +\ *d*\ i).

``V`` : *a* *b* --- *mag*
    Pushes a magnitude of a complex number, given by ``sqrt(a*a+b*b)``.

