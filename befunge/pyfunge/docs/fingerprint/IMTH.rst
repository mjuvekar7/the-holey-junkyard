.. _IMTH:

``"IMTH"`` Some integer math functions
----------------------------------------

:Fingerprint ID: 0x494d5448

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements yet another mathematical functions over integers. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#IMTH

``A`` : *a*\ :sub:`1` ... *a*\ :sub:`n` *n* --- (Σ\ *a*\ :sub:`i`\ ÷\ *n*)
    Calculates an average of *n* items (possibly including implicit zeroes under the bottom) from the stack. Reflects if *n* is negative, and pushes zero if *n* is zero.

``B`` : *x* --- *abs(x)*
    Calculates the absolute value of *x*.

``C`` : *x* --- *(1000×x)*
    Multiplies *x* by 1000.

``D`` : *x* --- *(x-sign(x))*
    Decreases the absolute value of *x* if *x* is nonzero, or do nothing if *x* is zero. In principle it is equal to *x* minus the sign function (see ``G`` command) of *x*.

``E`` : *x* --- *(10000×x)*
    Multiplies *x* by 10000.

``F`` : *n* --- *n!*
    Calculates the factorial of *n*. Reflects if *n* is negative. Strangely enough, it pushes zero (not 1) if *n* is zero. PyFunge retains this behavior for compatibility with RC/Funge-98.

``G`` : *x* --- *sign(x)*
    Pushes the sign function of *x*: -1 if *x* is negative, +1 if *x* is positive, and 0 if *x* is zero.

``H`` : *x* --- *(100×x)*
    Multiplies *x* by 100.

``I`` : *x* --- *(x+sign(x))*
    Increases the absolute value of *x* if *x* is nonzero, or do nothing if *x* is zero. In principle it is equal to *x* plus the sign function (see ``G`` command) of *x*.

``L`` : *x* *c* --- (*x*\ ×2\ :sup:`c`)
    Shift *x* left by *c* bits, or right by -*c* bits if *c* is negative. No-op if *c* is zero.

``N`` : *a*\ :sub:`1` ... *a*\ :sub:`n` *n* --- min{*a*\ :sub:`i`}
    Calculates a minimum of *n* items (possibly including implicit zeroes under the bottom) from the stack. Reflects if *n* is negative or zero.

``R`` : *x* *c* --- (*x*\ ÷2\ :sup:`c`)
    Shift *x* right by *c* bits, or left by -*c* bits if *c* is negative. No-op if *c* is zero.

``S`` : *a*\ :sub:`1` ... *a*\ :sub:`n` *n* --- (Σ\ *a*\ :sub:`i`)
    Calculates a sum of *n* items (possibly including implicit zeroes under the bottom) from the stack. Reflects if *n* is negative, and pushes zero if *n* is zero.

``T`` : *x* --- *(10×x)*
    Multiplies *x* by 10.

``U`` : *x* ---
    Prints *x* as an unsigned integer. Note that PyFunge prints only lower 32 bits of *x* since this command requires the size of integer to be finite.

``X`` : *a*\ :sub:`1` ... *a*\ :sub:`n` *n* --- max{*a*\ :sub:`i`}
    Calculates a maximum of *n* items (possibly including implicit zeroes under the bottom) from the stack. Reflects if *n* is negative or zero.

``Z`` : *x* --- *-x*
    Negates the sign of *x*.

