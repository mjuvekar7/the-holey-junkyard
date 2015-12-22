.. _3DSP:

``"3DSP"`` 3D space manipulation extension
---------------------------------------------

:Fingerprint ID: 0x33445350

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements operations on three-dimensional vectors and 4 by 4 matrices. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#3DSP

``A`` : *a*\ :sup:`v3` *b*\ :sup:`v3` --- *(a+b)*\ :sup:`v3`
    Adds two three-dimensional vectors.

``B`` : *a*\ :sup:`v3` *b*\ :sup:`v3` --- *(a-b)*\ :sup:`v3`
    Subtracts three-dimensional vector *b* from *a*.

``C`` : *a*\ :sup:`v3` *b*\ :sup:`v3` --- *(a×b)*\ :sup:`v3`
    Calculates cross product of two three-dimensional vectors. *a* and *b* should be in the correct order, as cross product is not commutative.

``D`` : *a*\ :sup:`v3` *b*\ :sup:`v3` --- *(a·b)*
    Calculates dot product of two three-dimensional vectors.

``L`` : *a*\ :sup:`v3` --- *sqrt(a·a)*
    Calculates length of given three-dimensional vector, defined as a square root of dot product of *a* and *a*.

``M`` : *a*\ :sup:`v3` *b*\ :sup:`v3` --- *(ab)*\ :sup:`v3`
    Multiplies two three-dimensional vectors.

``N`` : *a*\ :sup:`v3` --- *a÷sqrt(a·a)*\ :sup:`v3`
    Normalizes the given three-dimensional vector, so its length is 1. If *a* is zero vector, pushes itself.

``U`` : *a*\ :sup:`v3` --- *a*\ :sup:`v3` *a*\ :sup:`v3`
    Duplicates the given three-dimensional vector.

``V`` : *a*\ :sup:`v3` --- *x* *y*
    Projects the given three-dimensional vector to 2D view. In the other words, a vector *a*\ **i**\ +\ *b*\ **j**\ +\ *c*\ **k** projects to (*a*\ ÷\ *c*)\ **i**\ +\ (*b*\ ÷\ *c*)\ **j**. If *c* is zero it is assumed to be 1.

``Z`` : *a*\ :sup:`v3` *n*\ :sup:`fp` --- *(na)*\ :sup:`v3`
    Multiplies the given three-dimensional vector by scalar.

The following commands reflect in Unefunge mode.

``P`` : *dest*\ :sup:`v` *src*\ :sup:`v` ---
    Copies the matrix starting at *src* to *dest*, in the Funge space.

``R`` : *dest*\ :sup:`v` *axis* *angle*\ :sup:`fp` ---
    Puts the transformation matrix rotating *angle* degrees by *axis* to *dest* in the Funge space. *axis* is 1 for X axis, 2 for Y axis and 3 for Z axis. Reflects if *axis* is invalid.

``S`` : *dest*\ :sup:`v` *scale*\ :sup:`v3` ---
    Puts the transformation matrix scaling by factor of *scale* for each axes.

``T`` : *dest*\ :sup:`v` *offset*\ :sup:`v3` ---
    Puts the transformation matrix translating by *offset* for each axes.

``X`` : *a*\ :sup:`v3` *source*\ :sup:`v` --- *(aM)*\ :sup:`v3`
    Multiplies the three-dimensional vector by the transformation matrix *M* given by *source*. Actually it multiplies in the reverse order: the result should be *a*\ *M*.

``Y`` : *target*\ :sup:`v` *sourcea*\ :sup:`v` *sourceb*\ :sup:`v` ---
    Multiplies two matrices *A* and *B* given by *sourcea* and *sourceb*, and puts it to *target* in the Funge space. Actually it multiplies in the reverse order: the result should be *B*\ *A*.

Three-dimensional vector consists of three single precision floating point number, as used by :ref:`FPSP fingerprint <FPSP>`. 4 by 4 matrix in the Funge space occupies 4 by 4 cells, for example from (x,y,z) to (x+3,y+3,z) in Trefunge, and of course uses same floating point number.

