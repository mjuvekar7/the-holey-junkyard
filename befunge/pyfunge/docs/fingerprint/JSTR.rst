.. _JSTR:

``"JSTR"`` Jesse van Herk's extensions to string functions
-------------------------------------------------------------

:Fingerprint ID: 0x4a535452

This fingerprint, from Jesse van Herk's version of RC/Funge-98, implements ``G`` and ``P`` commands from :ref:`STRN` with variable delta. It provides the following commands:

``G`` : *delta*\ :sup:`v` *pos*\ :sup:`v` *n* --- *str*\ :sup:`s`
    Same to original, but only gets *n* characters and uses custom delta. Reflects if *n* is negative.

``P`` : *str*\ :sup:`s` *delta*\ :sup:`v` *pos*\ :sup:`v` *n* ---
    Same to original, but only puts *n* characters and uses custom delta. Reflects if *n* is negative.

