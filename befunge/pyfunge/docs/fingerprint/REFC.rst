.. _REFC:

``"REFC"`` Referenced Cells Extension
---------------------------------------

:Fingerprint ID: 0x52454643

This fingerprint, from `Cat's Eye Technologies`__, implements the table of references shared among IPs, which maps scalar value to vector (of same dimension with the space). It provides the following commands:

__ http://catseye.tc/projects/funge98/library/REFC.html

``D`` : *ref* --- *vector*\ :sup:`v`
    Dereferences the scalar value to vector. Reflects if *ref* is not valid reference.

``R`` : *vector*\ :sup:`v` --- *ref*
    Create new reference to vector.

