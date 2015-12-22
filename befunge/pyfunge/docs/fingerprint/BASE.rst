.. _BASE:

``"BASE"`` I/O for numbers in other bases
--------------------------------------------

:Fingerprint ID: 0x42415345

This fingerprint, from `RC/Funge-98`__, implements input and output for numbers in the other bases. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#BASE

``B`` : *n* ---
    Prints *n* in binary.

``H`` : *n* ---
    Prints *n* in hexadecimal.

``I`` : *base* --- *n*
    Reads a number in the given base. For *base* larger than 10, additional digits are from ``A`` to ``Z``. Reflects if *base* is not between 2 and 36, or at EOF.

``N`` : *n* *base* ---
    Prints *n* in the given base. For *base* larger than 10, additional digits are from ``A`` to ``Z``. Reflects if *base* is not between 2 and 36.

``O`` : *n* ---
    Prints *n* in octal.

