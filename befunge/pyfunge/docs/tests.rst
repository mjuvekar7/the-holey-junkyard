.. _tests:

########
Tests
########

PyFunge source distribution contains some test suites in :file:`tests/`. You check out them against current PyFunge version with :file:`pyfunge-test` shell script::

    $ ./pyfunge-test
    Done, XX out of XX test(s) passed.

This section discusses how the tests are organized and written.


Test format
===============

Each test requires at least two files:

- Test program: :file:`{testname}.bf`, :file:`{testname}.u98`, :file:`{testname}.b98` or :file:`{testname}.t98`, according to the language.
- Expected result: :file:`{testname}.expected`. It contains an ignored newline at the end, for convenience. (Many text editors always append one newline at the end of file.)

There are several optional files:

- Input data: :file:`{testname}.input`. It is fed into the :command:`pyfunge` script.
- Additional options: :file:`{testname}.options`. For example, you can include :option:`--disable-fprint` option in it to disable all fingerprints.

..
  - Checker script: :file:`{testname}.check`. If present, the test script uses that script to compare the result with the expected one. (It is not required to check against the original :file:`{testname}.expected` file.)
  - Initialization and finalization script: :file:`{testname}.init` and :file:`{testname}.final`, respectively.


Test categories
-------------------

:file:`tests/` directory contains some directories to organize tests:

- :file:`befunge93/`: Tests for Befunge-93 language.
- :file:`befunge98/`: Tests for Befunge-98 language.
- :file:`unefunge98/`: Tests for Unefunge-98 language.
- :file:`trefunge98/`: Tests for Trefunge-98 language.
- :file:`concurrent/`: Tests for concurrent Funge-98.
- :file:`fingerprints/{fprintname}/`: Tests for each fingerprints.

These directories are not important to the test script: they are just for convenience.


Test against Mycology suite
==============================

PyFunge contains a convenience script called :file:`mycology-filter` in :file:`tools/` directory of the source distribution. This script, written in :manpage:`awk(1)`, highlights the result from Mycology_ test suite -- it also analyzes some ``UNDEF`` lines and marks it as ``GOOD`` or ``BAD`` line if possible. It also distinguishes ``UNDEF`` lines due to the specification and ``UNDEF`` lines due to the limitation of test suite (i.e. ``UNSURE``), so you have to check out only ``UNSURE`` lines.

.. _Mycology: http://users.tkk.fi/~mniemenm/befunge/mycology.html

Typical usage is as like this::

    $ pyfunge mycology.b98 | mycology-filter
    0 1 2 3 4 5 6 7 
    GOOD: , works
    GOOD: : duplicates
    GOOD: empty stack pops zero
    [...]

    The Mycology Befunge-98 test suite is practically done.
    Trying to quit with q. If the return status is 15, consider it GOOD...

    *** GOOD 365, BAD 0, UNDEF 49, UNSURE 64

Note that this script does not preserve the exit code, and you should check it by hand. This script is also not capable for ``mycoterm`` or ``mycouser`` tests.

