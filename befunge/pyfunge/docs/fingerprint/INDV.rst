.. _INDV:

``"INDV"`` Pointer functions
-------------------------------

:Fingerprint ID: 0x494e4456

This fingerprint, from `RC/Funge-98`__, implements the indirect get and put. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#INDV

``G`` : *pos*\ :sup:`v` --- *value*
    Reads one vector from *pos*, and pushes the cell at that vector. The vector in Funge space is read rightwards in the reverse order (Y and X in Befunge mode, Z, Y and X in Trefunge mode).

``P`` : *value* *pos*\ :sup:`v` ---
    Reads one vector from *pos*, and puts the *value* to the cell at that vector. The vector in Funge space is read rightwards in the reverse order.

``V`` : *pos*\ :sup:`v` --- *vec*\ :sup:`v`
    Same to ``G`` but it reads a vector instead of a scalar. The vector is read in the same way.

``W`` : *vec*\ :sup:`v` *pos*\ :sup:`v` ---
    Same to ``P`` but it puts a vector instead of a scalar. The vector is written in the same way.

