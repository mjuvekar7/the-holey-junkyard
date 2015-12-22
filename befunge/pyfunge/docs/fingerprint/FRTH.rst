.. _FRTH:

``"FRTH"`` Some common forth commands
---------------------------------------

:Fingerprint ID: 0x46525448

This fingerprint, from `RC/Funge-98`__, implements common stack operations from Forth. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#FRTH

``D`` : ... --- ... *size*
    Pushes the size of stack before execution. Same to ``7y5*d+y``.

``L`` : ... *n* --- ...
    Pops *n*. Then moves (*n*\ +1)-th cell to the top if *n* is positive or moves the top to (-*n*\ +1)-th cell if negative. (For example, ``123453L`` is same to ``13452`` and ``1234503-L`` is same to ``15234``.) Assumes that the stack has infinite zeroes under the bottom if *n* is out of bound.

``O`` : *a* *b* --- *a* *b* *a*
    Pushes second-to-the-top cell in the stack. Same to ``1P``.

``P`` : ... *n* --- ... *value*
    Pushes (*n*\ +1)-th cell in the stack. Assumes that the stack has infinite zeroes under the bottom if *n* is out of bound. Reflects if *n* is negative.

``R`` : *a* *b* *c* --- *b* *c* *a*
    Moves third-to-the-top cell to the top. Same to ``2L``.

