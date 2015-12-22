.. _SUBR:

``"SUBR"`` Subroutine extension
----------------------------------

:Fingerprint ID: 0x53554252

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements a function call to arbitrary Funge code and a return from it. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#SUBR

``A`` : ---
    Sets the absolute mode, so the jump location is independent to IP's storage offset. This is a default behavior.

``C`` : *a*\ :sub:`1` ... *a*\ :sub:`n` *pos*\ :sup:`v` *n* --- *origpos*\ :sup:`v` *origdelta*\ :sup:`v` *a*\ :sub:`1` ... *a*\ :sub:`n`
    Calls a subroutine at *pos* and saves the original position and delta as *origpos* and *origdelta*. After the call IP travels towards right. It pops *n* items from the stack as well, and moves them to the top of the stack. Reflects if *n* is negative.

``J`` : *pos*\ :sup:`v` ---
    Jumps to given *pos*, and make IP travels towards right. It doesn't store any return information.

``O`` : ---
    Sets the relative mode, so the jump location is relative to IP's storage offset.

``R`` : *origpos*\ :sup:`v` *origdelta*\ :sup:`v` *a*\ :sub:`1` ... *a*\ :sub:`n` *n* --- *a*\ :sub:`1` ... *a*\ :sub:`n`
    Returns from a subroutine and restores the position and delta to *origpos* and *origdelta*, respectively. It also pops *n* items from the stack and moes them to the top of the stack. Reflects if *n* is negative.

