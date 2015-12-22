.. _DATE:

``"DATE"`` Date Functions
----------------------------

:Fingerprint ID: 0x44415445

This fingerprint, from `RC/Funge-98`__, implements date-related functions. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#DATE

``A`` : *y* *m* *d* *n* --- *y* *m* *d*
    Adds (or subtracts if *n* is negative) *n* days to given date. Reflects for invalid date.

``C`` : *jd* --- *y* *m* *d*
    Converts Julian day (assuming 12:00 noon) to calendar date.

``D`` : *y1* *m1* *d1* *y2* *m2* *d2* --- *n*
    Pushes the number of days between given dates. For example, there are 72 days between January 1, 2009 and March 14, 2009. If first date is before second date pushes the negative value. Reflects for invalid dates.

``J`` : *y* *m* *d* --- *jd*
    Converts calendar date to Julian day (assuming 12:00 noon).

``T`` : *y* *doy* --- *y* *m* *d*
    Expands day-of-year to full date. Reflects for invalid date.

``W`` : *y* *m* *d* --- *dow*
    Pushes day of week, where Monday is 0 and Sunday is 6. Reflects for invalid date.

``Y`` : *y* *m* *d* --- *doy*
    Pushes day of year, where January 1 is 0. Reflects for invalid date.

All date is given as proleptic, extended Gregorian calendar. The year part of date can be negative, but it cannot be zero. So 1 BCE is year -1, 2 BCE is year -2, and so on. Julian day 0 was November 24, 4714 BCE, or January 1, 4713 BCE in Julian proleptic calendar.

