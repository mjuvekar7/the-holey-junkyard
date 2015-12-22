.. _SETS:

``"SETS"`` Set operations
----------------------------

:Fingerprint ID: 0x53455453

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements set operations. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#SETS

``A`` : *set*\ :sup:`A` *value* --- *(set∪{value})*\ :sup:`A`
    Adds *value* to the *set*. If there is *value* in the *set*, it will do nothing.

``C`` : *set*\ :sup:`A` --- *set*\ :sup:`A` *len*
    Pushes the size of the *set*.

``D`` : *set*\ :sup:`A` --- *set*\ :sup:`A` *set*\ :sup:`A`
    Duplicates the set.

``G`` : *delta*\ :sup:`v` *source*\ :sup:`v` --- *set*\ :sup:`A`
    Reads the set from the Funge space, starting from *source* with given *delta*. The set is retrieved in the stack order: the cell at *source* should contain the number of items. Reflects if the stored set is invalid.

``I`` : *a*\ :sup:`A` *b*\ :sup:`A` --- *(a∩b)*\ :sup:`A`
    Pushes the intersection of two sets *a* and *b*.

``M`` : *set*\ :sup:`A` *value* --- *result*
    Pushes 1 if *value* is in the *set*, or 0 otherwise.

``P`` : *set*\ :sup:`A` --- *set*\ :sup:`A`
    Prints the *set* to the standard output.

``R`` : *set*\ :sup:`A` *value* --- *(set-{value})*\ :sup:`A`
    Removes *value* from the *set*. If there is no *value* in the *set*, it will do nothing.

``S`` : *a*\ :sup:`A` *b*\ :sup:`A` --- *(a-b)*\ :sup:`A`
    Pushes the difference of two sets *a* and *b*.

``U`` : *a*\ :sup:`A` *b*\ :sup:`A` --- *(a∪b)*\ :sup:`A`
    Pushes the union of two sets *a* and *b*.

``W`` : *set*\ :sup:`A` *delta*\ :sup:`v` *dest*\ :sup:`v` --- *set*\ :sup:`A`
    Writes the set to the Funge space, starting from *dest* with given *delta*. The set is stored in the stack order: the cell at *dest* will contain the number of items.

``X`` : *a*\ :sup:`A` *b*\ :sup:`A` --- *b*\ :sup:`A` *a*\ :sup:`A`
    Exchanges two sets *a* and *b* in the top of the stack.

``Z`` : *set*\ :sup:`A` ---
    Pops and discards the *set* in the top of the stack.

All commands reflect if given set is invalid: stack underflow has been occurred, the size of set is negative, or there is duplicates in the set.

