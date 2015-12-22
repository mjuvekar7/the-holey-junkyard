.. _NCRS:

``"NCRS"`` Ncurses extension
-------------------------------

:Fingerprint ID: 0x4e435253

.. versionadded:: 0.5-rc2

This fingerprint, from Jesse van Herk's version of RC/Funge-98, implements an interface to curses library. Contradictory to the name, this fingerprint doesn't necessilarly require the GNU ncurses library. It provides the following commands:

``B`` : ---
    Emits a short attention sound, if supported.

``C`` : *mode* ---
    Clears the part of window according to *mode*:

    - Clears the entire window if *mode* is 0.
    - Clears from cursor to the end of the line if *mode* is 1.
    - Clears from cursor to the end of the window if *mode* is 2.
    - Reflects otherwise.

    It requires the current window, initialized by ``1I``.

``E`` : *echo* ---
    Turns on or off echo mode according to *echo*. In echo mode, each character input is printed to the screen back.

``G`` : --- *ch*
    Gets a character, including function keys and keypad. It requires the current window, initialized by ``1I``.

``I`` : *init* ---
    Initializes the current window if *init* is non-zero, or finalizes it otherwise.

``K`` : *keypad* ---
    Turn on or off the automatic parsing of special key sequences according to *keypad*. If this mode is turned off, you can get the funky escape sequence via ``G``. It requires the current window, initialized by ``1I``.

``M`` : *c* *r* ---
    Moves the cursor to (*c*, *r*). It requires the current window, initialized by ``1I``.

``N`` : *nocbreak* ---
    Turns off or on cbreak mode according to *echo*. (Unlike ``E`` and ``K``, it turns *off* if *echo* is non-zero.) In cbreak mode, the line buffering is disabled and characters are read one by one.

``P`` : *ch* ---
    Puts a character to current cursor position. It requires the current window, initialized by ``1I``.

``R`` : ---
    Updates the display immediately. It requires the current window, initialized by ``1I``.

``S`` : *str*\ :sup:`s` ---
    Puts a string to current cursor position. It requires the current window, initialized by ``1I``.

``U`` : *ch* ---
    Puts a character to the input buffer back, so next ``G`` command gets it. Only one ``U`` can be executed before next ``G`` command. It requires the current window, initialized by ``1I``.

All commands reflect on failure, or when the current window is not initialized if needed.

