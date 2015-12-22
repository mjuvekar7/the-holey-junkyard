.. _IIPC:

``"IIPC"`` Inter IP communication extension
-----------------------------------------------

:Fingerprint ID: 0x49495043

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements commands that manipulates the other IP's stack and sleeps until the signal. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#IIPC

``A`` : --- *parentid*
    Pushes the identifier of parent IP, from which current IP is splitted.

``D`` : ---
    Makes the current IP asleep (dormant) until the stack is manipulated by another IP, using ``G`` or ``P`` commands.

``G`` : *id* --- *n*
    Pops one item from the stack of the IP which identifier is *id*, and pushes it to the current IP's stack. It could wake up the target IP. Reflects if *id* is an invalid identifier.

``I`` : --- *id*
    Pushes the identifier of IP. In PyFunge it is equivalent to ``8y``.

``L`` : *id* --- *n*
    Same to ``G``, but it doesn't pop from the stack of target IP. Since it doesn't manipulate the stack it won't wake up the target IP either.

``P`` : *n* *id* ---
    Pushes a value *n* to the stack of the IP which identifier is *id*. It could wake up the target IP. Reflects if *id* is an invalid identifier.

