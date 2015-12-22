.. _TOYS:

``"TOYS"`` Funge-98 Standard Toys
------------------------------------

:Fingerprint ID: 0x544f5953

This fingerprint, from `Cat's Eye Technologies`__, implements a lot of "toy" commands, sometimes useful for Funge programming. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/TOYS.html

``A`` : *value* *n* --- *value* ... *value*
    Pushes *n* copies of *value*. If *n* is not positive it does nothing.

``B`` : *b* *a* --- *(a+b)* *(a-b)*
    Performs "butterfly" operation, originated from fast Fourier transform algorithms.

``D`` : *a* --- *(a-1)*
    Decrements the top of stack.

``E`` : ... --- *sum*
    Pops all cells from the stack and pushes their sum.

``H`` : *a* *b* --- *(a shift b)*
    Pushes *a* shifted by *b* bits. If *b* is positive it shifts left, or it shifts right. In PyFunge left shift doesn't overflow since the integer is arbitrary precision.

``I`` : *a* --- *(a+1)*
    Increments the top of stack.

``J`` : *offset* ---
    Moves the current column (cells with same X coordinate) up (negative offset) or down (positive offset).

``L`` : --- *a*
    Pushes the value of cell at the left of IP. Here "left" means the next command to be executed if current command is ``[``.

``N`` : *a* --- *-a*
    Negates the top of stack.

``O`` : *offset* ---
    Moves the current row (cells with same Y coordinate) left (negative offset) or right (positive offset).

``P`` : ... --- *product*
    Pops all cells from the stack and pushes their product. Note that this ignores the implicit zeroes under the bottom of stack.

``Q`` : *a* ---
    Sets the cell behind current IP to *a*.

``R`` : --- *a*
    Pushes the value of cell at the right of IP. Here "right" means the next command to be executed if current command is ``]``.

``T`` : *a* *dimension* ---
    Changes delta to unit vector of given dimension if *a* is non-zero, or negate of unit vector if *a* is zero. In the other words ``0T`` acts like ``_``, ``1T`` acts like ``|`` and ``2T`` acts like ``m``. Reflects if the invalid dimension is given.

``U`` : ---
    Acts like ``?`` and transmutes itself to the command which sets delta to changed value.

``W`` : *value* *target*\ :sup:`v` ---
    Pops the target vector and value. Then executes itself indefinitely (i.e. consuming ticks), until the target cell at *target* is not less than given value. Reflects if the cell is greater than given value. This command is useful for synchronization in Concurrent Funges.

``X`` : ---
    Increments X coordinate of IP. Does not change the direction.

``Y`` : ---
    Increments Y coordinate of IP. Does not change the direction.

``Z`` : ---
    Increments Z coordinate of IP. Does not change the direction.

The following commands reflect in Unefunge and Trefunge mode. (These commands cannot be trivially extended to other dimensions.)

``C`` : *src*\ :sup:`v` *size*\ :sup:`v` *dest*\ :sup:`v` ---
    Pops three vectors and copies Funge space starting at *src* and which size is *size* into *dest*, in the coordinate-ascending order.

``F`` : *a*\ :sub:`nm` ... *a*\ :sub:`11` *n* *m* *dest*\ :sup:`v` ---
    Pops one vector and two scalars. Then pops *n* by *m* cells and populates Funge space starting at *dest* with *n* rows and *m* columns, in the coordinate-ascending order.

``G`` : *n* *m* *src*\ :sup:`v` --- *a*\ :sub:`nm` ... *a*\ :sub:`11`
    Pops one vector and two scalars. Then pushes *n* by *m* cells from Funge space starting at *dest* with *n* rows and *m* columns, in the coordinate-ascending order.

``K`` : *src*\ :sup:`v` *size*\ :sup:`v` *dest*\ :sup:`v` ---
    Pops three vectors and copies Funge space starting at *src* and which size is *size* into *dest*, in the coordinate-descending order.

``M`` : *src*\ :sup:`v` *size*\ :sup:`v` *dest*\ :sup:`v` ---
    Pops three vectors and moves (i.e. copies and sets the original to whitespace) Funge space starting at *src* and which size is *size* into *dest*, in the coordinate-ascending order.

``S`` : *value* *size*\ :sup:`v` *dest*\ :sup:`v` ---
    Pops two vectors and value, fills Funge space starting at *dest* and which size is *size* to *value*.

``V`` : *src*\ :sup:`v` *size*\ :sup:`v` *dest*\ :sup:`v` ---
    Pops three vectors and moves (i.e. copies and sets the original to whitespace) Funge space starting at *src* and which size is *size* into *dest*, in the coordinate-descending order.

