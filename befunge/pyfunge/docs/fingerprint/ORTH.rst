.. _ORTH:

``"ORTH"`` Orthogonal Easement Library
-----------------------------------------

:Fingerprint ID: 0x4f525448

This fingerprint, from `Cat's Eye Technologies`__, implements some commands present in `Orthogonal programming language <http://www.muppetlabs.com/~breadbox/orth/>`_ but not in Funge-98. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/ORTH.html

``A`` : *a* *b* --- *(a AND b)*
    Performs bitwise AND.

``E`` : *a* *b* --- *(a XOR b)*
    Performs bitwise exclusive OR.

``G`` : *pos*\ :sup:`v` ---
    Same to ``g``, but the coordinates are pushed in the reverse order. PyFunge supports this command in Unefunge and Trefunge mode as well.

``O`` : *a* *b* --- *(a OR b)*
    Performs bitwise OR.

``P`` : *value* *pos*\ :sup:`v` ---
    Same to ``p``, but the coordinates are pushed in the reverse order. PyFunge supports this command in Unefunge and Trefunge mode as well.

``S`` : *str*\ :sup:`s` ---
    Pops the null-terminated string and prints it.

``V`` : *dx* ---
    Changes current X coordinate of delta.

``X`` : *x* ---
    Changes current X coordinate.

``Z`` : *a* ---
    Pops *a* and skips next command (as like ``#``) if it is zero.

The following commands reflect in Unefunge mode.

``W`` : *dy* ---
    Changes current Y coordinate of delta.

``Y`` : *y* ---
    Changes current Y coordinate.

