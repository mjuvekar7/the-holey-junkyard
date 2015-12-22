.. _TERM:

``"TERM"`` Terminal extension
-------------------------------

:Fingerprint ID: 0x5445524d

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements basic terminal operations moving the cursor and clearing the screen. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#TERM

``C`` : ---
    Clears the screen.

``D`` : *n* ---
    Moves the cursor down *n* lines. If *n* is negative, it moves up.

``G`` : *c* *r* ---
    Puts the cursor at row *r* and column *c*. The first line is row 0, and the first column is column 0.

``H`` : ---
    Moves the cursor to home (the first line and first column).

``L`` : ---
    Clears from cursor to the end of the current line.

``S`` : ---
    Clears from cursor to the end of the current screen. (``HS`` will act like ``C`` for example.)

``U`` : *n* ---
    Moves the cursor up *n* lines. If *n* is negative, it moves down.

