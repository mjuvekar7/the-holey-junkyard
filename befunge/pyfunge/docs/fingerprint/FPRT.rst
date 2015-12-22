.. _FPRT:

``"FPRT"`` Formatted print
-----------------------------

:Fingerprint ID: 0x46505254

This fingerprint, from `RC/Funge-98`__, implements :manpage:`sprintf(3)`-like formatting commands. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#FPRT

``D`` : *format*\ :sup:`s` *x*\ :sup:`fp` --- *str*\ :sup:`s`
    Formats a double precision floating point number, also used in :ref:`FPDP <FPDP>`, with given *format*.

``F`` : *format*\ :sup:`s` *x*\ :sup:`fp` --- *str*\ :sup:`s`
    Formats a single precision floating point number, also used in :ref:`FPSP <FPSP>`, with given *format*.

``I`` : *format*\ :sup:`s` *n* --- *str*\ :sup:`s`
    Formats the number with given *format*.

``L`` : *format*\ :sup:`s` *x*\ :sup:`L` --- *str*\ :sup:`s`
    Formats the long number, also used in :ref:`LONG <LONG>`, with given *format*.

``S`` : *format*\ :sup:`s` *str*\ :sup:`s` --- *str*\ :sup:`s`
    Formats the null-terminated string with given *format*.

All command reflects if *format* has zero or two format specifiers, or is invalid.

