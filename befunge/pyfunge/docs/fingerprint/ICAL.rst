.. _ICAL:

``"ICAL"`` Some Intercal-like functions
------------------------------------------

:Fingerprint ID: 0x4943414c

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements INTERCAL-esque operations. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#ICAL

``A`` : *a* --- &\ *a*
    Performs unary AND operation, defined as ``a AND ror(a, 1)`` where ``ror`` stands for bitwise rotate-right operation.

``F`` : *n* ---
    Works like INTERCAL's FORGET command. It discards *n* vectors from the address stack. Reflects if *n* is negative; it is no-op when *n* is zero. This command doesn't change delta.

``I`` : *a* *b* --- *a*\ $\ *b*
    Performs mingle operation.

    Mingle interleaves bits from *a* and *b*, so if *a* = *a*\ :sub:`3`\ *a*\ :sub:`2`\ *a*\ :sub:`1`\ *a*\ :sub:`0` and *b* = *b*\ :sub:`3`\ *b*\ :sub:`2`\ *b*\ :sub:`1`\ *b*\ :sub:`0` then *a*\ $\ *b* = *a*\ :sub:`3`\ *b*\ :sub:`3`\ *a*\ :sub:`2`\ *b*\ :sub:`2`\ *a*\ :sub:`1`\ *b*\ :sub:`1`\ *a*\ :sub:`0`\ *b*\ :sub:`0`.

``N`` : *target*\ :sup:`v` ---
    Works like INTERCAL's NEXT command. It pushes the position of IP to the address stack, and jumps to *target* so for next time that cell is executed. Reflects if the address stack contains 79 entries already. (This is original INTERCAL-72 behavior, indeed.)

``O`` : *a* --- V\ *a*
    Performs unary OR operation, defined as ``a OR ror(a, 1)`` where ``ror`` stands for bitwise rotate-right operation.

``R`` : *n* ---
    Works like INTERCAL's RESUME command. It pops *n* vectors from the address stack, and jumps to last popped vector so for next time that cell is executed. Reflects if *n* is negative. If *n* is larger than the size of address stack, the address stack will be emptied and the position won't change. This command doesn't change delta.

``S`` : *a* *b* --- *a*\ ~\ *b*
    Performs select operation.

    Select collects bits from *a*, such that corresponding bit from *b* is set. Collected bits are left-padded and stored in the order: for example ``1100 ~ 101`` is ``10``, since *b* has bit 2 and 0 set.

``X`` : *a* --- ∀\ *a*
    Performs unary XOR operation, defined as ``a XOR ror(a, 1)`` where ``ror`` stands for bitwise rotate-right operation.

INTERCAL uses the fixed integer size but PyFunge doesn't, so it uses certain heuristics. If an operand of unary commands (``A``, ``O``, ``X``) is larger than 16 bits, it assumes the integer size of 32 bits; if it is larger than 32 bits, it assumes the integer size of 64 bits; and so on. This is consistent with RC/Funge-98's behavior too.

