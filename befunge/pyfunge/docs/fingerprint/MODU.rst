.. _MODU:

``"MODU"`` Modulo Arithmetic Extension
-----------------------------------------

:Fingerprint ID: 0x4d4f4455

This fingerprint, from `Cat's Eye Technologies`__, implements various modulo behaviors with negative divisor or dividend. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/MODU.html

``M`` : *a* *b* --- *(a mod b)*
    A remainder is defined as ``a - floor(a/b)``. Same to ``%`` behavior of PyFunge.

``R`` : *a* *b* --- *(a mod b)*
    A remainder has same sign with dividend. A sign of divisor is ignored.

``U`` : *a* *b* --- *(a mod b)*
    A remainder ignores a sign of divisor and dividend.

Every commands pushes 0 if divisor is zero.

