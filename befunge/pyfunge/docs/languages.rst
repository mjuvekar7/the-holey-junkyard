.. _languages:

#####################
Supported Languages
#####################

PyFunge supports four distinct languages in the Funge family: Befunge-93, Unefunge-98, Befunge-98, Trefunge-98. All these languages operate in the Funge space (which is bounded to 25 rows and 80 columns in Befunge-93, or infinite in Funge-98) and the stack (which is extended to stack stacks in Funge-98).


Befunge-93 Semantics
========================

PyFunge supports the full Befunge-93 language. It does not support Funge-98 commands in Befunge-93 mode at all, since it will make some legitimate Befunge-93 programs don't work.


Undefined behaviors
---------------------

* PyFunge uses an arbitrary precision Python integer for stack cells.
* Division by zero asks the user for alternative value. This was a behavior of original Befunge-93 reference interpreter. You can also select an alternative behavior by :option:`--division-by-zero` option.


Funge-98 Semantics
=====================

PyFunge 0.5.0 and later is fully (if not almost) compliant to Funge-98 specification. This section describes its undefined behaviors with respect to the specification, and precise behaviors of supported fingerprints.


Undefined behaviors
---------------------

In regarding Funge virtual machine:

* PyFunge uses an arbitrary precision Python integer. This also means Funge space is truly infinite, because the coordinate uses the same type.
* PyFunge supports ``.b98`` extension for Befunge-98, as mentioned in the specification informally. It also supports ``.u98`` and ``.t98`` extensions for Unefunge-98 and Trefunge-98 respectively. (See :ref:`invocation` for overriding.)
* PyFunge assumes that Funge space is full of spaces, not the wrapped rectangle. For example, wrapping string pushes one (not zero) space on the edge.

In regarding Funge-98 commands:

* ``/`` and ``%`` with negative divisor or dividend does same with Python: for positive divisor non-negative remainder is used, and for negative divisor ``(-x)/(-y)`` is same to ``x/y``.
* ``k`` with a negative argument does nothing.
* ``=`` invokes :manpage:`system(3)` call.
* ``t`` does not copy the fingerprint list from parent IP.
* ``(`` and ``)`` with negative count does same thing with zero count.

In regarding system information command (``y``):

* PyFunge's handprint is 0x50794698, i.e. ``'PyF\x98'``.
* PyFunge pushes -1 for the number of bytes per cell. This matches the behavior of `efunge <http://kuonet.org/~anmaster/efunge/>`_, only known other Funge-98 interpreter supports an arbitrary precision integer.
* Sizes of each stack stacks are pushed from BOSS (at bottom) to TOSS (at top).
* Current date and time uses local time. Use ``TIME`` fingerprint for explicit behavior.
* The order of environment variables is undefined: you cannot depend on this order, unless the environment variables didn't change.


.. _funge98-fingerprints:

Supported fingerprints
------------------------

PyFunge supports many fingerprints enabled by default. The following is an exhaustive list of them.

Note that this is a description of PyFunge implementation, not the official specification. Unless the fingerprint is from PyFunge, do not consider this document is authoritative.

.. toctree::

   fingerprint/3DSP.rst
   fingerprint/BASE.rst
   fingerprint/BOOL.rst
   fingerprint/CPLI.rst
   fingerprint/DATE.rst
   fingerprint/DIRF.rst
   fingerprint/EVAR.rst
   fingerprint/FILE.rst
   fingerprint/FIXP.rst
   fingerprint/FPRT.rst
   fingerprint/FPxP.rst
   fingerprint/FRTH.rst
   fingerprint/HRTI.rst
   fingerprint/ICAL.rst
   fingerprint/IIPC.rst
   fingerprint/IMAP.rst
   fingerprint/IMTH.rst
   fingerprint/INDV.rst
   fingerprint/JSTR.rst
   fingerprint/LONG.rst
   fingerprint/MODE.rst
   fingerprint/MODU.rst
   fingerprint/NCRS.rst
   fingerprint/NULL.rst
   fingerprint/ORTH.rst
   fingerprint/PERL.rst
   fingerprint/REFC.rst
   fingerprint/ROMA.rst
   fingerprint/SCKE.rst
   fingerprint/SETS.rst
   fingerprint/SOCK.rst
   fingerprint/STRN.rst
   fingerprint/SUBR.rst
   fingerprint/TERM.rst
   fingerprint/TIME.rst
   fingerprint/TOYS.rst

.. topic:: Notations for stack operation

   This section uses a notation to describe how the command changes the stack. It looks like this:

        ``X`` : *x*\ :sub:`1`\ :sup:`fp` ... *x*\ :sub:`n`\ :sup:`fp` *path*\ :sup:`s` *delta*\ :sup:`v` *start*\ :sup:`v` n --- *x*\ :sub:`n` ... *x*\ :sub:`1`
            Dumps the *n* values from Funge space starting at *start* with given *delta*. *k*-th popped value is multiplied by scale factor *x*\ :sub:`k`, and written to *path* as IEEE 754 double precision floating point format with unspecified endian. Reflects on failure. If succeed, it reverses the order of scale factors in the stack.

   This fictional (and somewhat contrived) example shows the stack notation. The stack notation consists of "before" part and "after" part, each consists of the stack contents listed from the bottom to the top.

   A superscript after the variable denotes the type. If there is no superscript, it is a single (scalar) cell. The type notation is as follows:

   * "v" denotes a vector, whose size is equal to the number of dimensions in Funge space.
   * "v3" denotes a three-dimensional vector, whose elements are single precision floating point numbers used by ``FPSP``.
   * "s" denotes a null-terminated string ("0gnirts").
   * "fp" denotes a floating point number, which occupies one or two cells. Whether this is a single precision or double precision is up to the context. (See ``FPSP`` and ``FPDP`` for actual format.)
   * "L" denotes a long integer, which occupies two cells. (See ``LONG`` for actual format.)
   * "A" denotes an array with its size on the top of the stack. For example, ``abc3`` pushes an array with three elements, ``0`` pushes an empty array, and ``k$`` discards the array. The order of elements is up to semantics.

   If the stack has a fewer cells than the command requires, it assumes the stack has infinite zeroes under the bottom unless specified. In the other words, the command pops the required cells (possibly implicit zeroes) and pushes the generated cells. Even if the "before" and "after" part contains the same number of cells, it can result in changes in the size of stack if the stack underflows.

