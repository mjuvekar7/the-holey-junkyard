.. _TIME:

``"TIME"`` Time and Date functions
------------------------------------

:Fingerprint ID: 0x54494d45

This fingerprint, from `RC/Funge-98`__, implements time-related functions. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#TIME

``D`` : --- *d*
    Pushes current day of month.

``F`` : --- *doy*
    Pushes current day of year, where January 1 is day 0.

``G`` : ---
    Sets to GMT (i.e. UTC) mode. This mode is local to current IP.

``H`` : --- *hour*
    Pushes current hour.

``L`` : ---
    Sets to local time mode. This mode is local to current IP, and it is default.

``M`` : --- *min*
    Pushes current minute.

``O`` : --- *m*
    Pushes current month, where January is 1.

``S`` : --- *sec*
    Pushes current second.

``W`` : --- *dow*
    Pushes current day of week, where Sunday is 1 and Saturday is 7.

``Y`` : --- *y*
    Pushes current year.

