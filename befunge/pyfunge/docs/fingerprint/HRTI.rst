.. _HRTI:

``"HRTI"`` High-Resolution Timer Interface
--------------------------------------------

:Fingerprint ID: 0x48525449

This fingerprint, from `Cat's Eye Technologies`__, implements sub-second precision timer. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/HRTI.html

``E`` : ---
    Erases any existing mark set by ``M``.

``G`` : --- *ticks*
    Pushes the smallest clock tick the system can handle, measured in microseconds.

``M`` : ---
    Marks current clock tick for later use.

``S`` : --- *ticks*
    Pushes the number of microseconds elapsed since the last whole second.

``T`` : --- *ticks*
    Pushes the number of microseconds elapsed since last mark. Reflects if there is no mark set.

