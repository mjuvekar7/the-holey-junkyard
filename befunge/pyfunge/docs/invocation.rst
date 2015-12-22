.. _invocation:

############
Invocation
############

PyFunge supports a command-line front end for executing Funge program.


.. _pyfunge-driver:

:manpage:`pyfunge(1)`
=======================

``pyfunge`` is a driver script, used for interpreting a Funge program. In short, you can simply execute Funge program by providing a file name::

    $ pyfunge hello.bf

It can read the source code from the standard input (``-``), but you have to specify the version and number of dimensions (only if it is not Befunge) manually. (See also :option:`-v` and :option:`-d`.)

::

    $ pyfunge -v98 -d3 -


General options
------------------

.. cmdoption:: -h
               --help

   Shows the help message.

.. cmdoption:: -V
               --version

   Shows the version of PyFunge.

.. cmdoption:: -w
               --warnings

   Enables warnings. PyFunge generates warnings under the following circumstances:

   * Division by zero in Befunge-93 mode.

.. cmdoption:: -x
               --skip-first-line

   Skips the first line of Funge code. This is useful for standalone script or CGI::

        #!/usr/bin/env pyfunge -x -v98
        a"!dlrow ,olleH">:#,_0q


Funge options
---------------

.. cmdoption:: -v standard
               --std standard

   Selects the language standard to be used. PyFunge currently supports the following standards:

   ``93``, ``befunge93``
       The program will run in Befunge-93 mode: Funge space is bounded and every non-Befunge-93 commands do nothing.

   ``98``, ``funge98``
       The program will run in standard Funge-98 mode. This is default.

   PyFunge tries to infer this option from source code extension, so you don't have to use this generally. If the extension is ``.bf`` it is Befunge-93 code, and if it is one of ``.u98``, ``.b98`` and ``.t98`` it is Funge-98 code. But if you have to run the standalone script or C-Funge polyglot this option will be useful.

.. cmdoption:: -d dimension
               --dimension dimension

   Sets how many dimensions are in the Funge space. *dimension* can be 1 (Unefunge), 2 (Befunge) or 3 (Trefunge). Note that there is no Unefunge-93 nor Trefunge-93, so a combination like ``-v93 -d1`` will raise an error.

   PyFunge tries to infer this option from source code extension (like :option:`-v`), and if it cannot the number of dimensions defaults to 2, i.e. Befunge.

.. cmdoption:: -1
               --unefunge

   Short for ``--dimension 1``.
   
.. cmdoption:: -2
               --befunge

   Short for ``--dimension 2``.

.. cmdoption:: -3
               --trefunge

   Short for ``--dimension 3``.

.. cmdoption:: --statistics

   Shows statistics after the program is terminated. It displays the elapsed time, the real time (excluding the user input), how many commands are executed and how many ticks are elapsed.


Befunge-93 options
--------------------

These options will work only in Befunge-93 mode (``-v 93``).

.. cmdoption:: --division-by-zero value

   Selects the behavior when division by zero occurs. *value* can be one of the following:

   number
       Division by zero results in given value, no matter what the dividend is. If warnings are enabled it will issue the warning for it.

   ``prompt``
       PyFunge will ask for a result of division by zero. This is default behavior.

   ``stop``
       The program will be terminated when division by zero occurs. If warnings are enabled it will issue the warning for it.

   Funge-98 explicitly states that division by zero results in zero, so this option cannot be applied.


Funge-98 options
------------------

These options will work only in Funge-98 mode (``-v 98``).

.. cmdoption:: -f fingerprints
               --fprint fingerprints

   Uses the given fingerprints. Fingerprint names are given as comma-delimited list, and it defaults to every fingerprints in default search path (i.e. :mod:`funge.fp` package).

.. cmdoption:: --disable-fprint

   Disables all fingerprints.

.. cmdoption:: -I fingerprintpath
               --fprint-include fingerprintpath

   Adds fingerprint search path. See :envvar:`PYFUNGE_FPRINT_PATH` for the format and detail.

.. cmdoption:: --concurrent

   Enables the concurrent Funge. This is default in Funge-98 mode.

.. cmdoption:: --filesystem

   Enables the filesystem Funge. This is default in Funge-98 mode.

.. cmdoption:: -C
               --no-concurrent

   Disables the concurrent Funge.

.. cmdoption:: -F
               --no-filesystem

   Disables the filesystem Funge.

.. cmdoption:: --list-fprints

   Lists all available fingerprints and exits. If :envvar:`PYFUNGE_FPRINT_PATH` or :option:`-I` is set it is used to search additional fingerprints.


.. :manpage:`pyfungec(1)`
   ========================

.. :manpage:`pyfunged(1)`
   ========================


Environment variables
=======================

PyFunge internally recognizes the following environment variables, if any:

.. envvar:: PYFUNGE_NO_PSYCO

   If this is set to a non-empty string it disables JIT compilation provided by Psyco. It can slow down the execution quite much, but it is useful for debugging and profiling.

.. envvar:: PYFUNGE_FPRINT_PATH

   If this is set to a non-empty string it finds fingerprints from given paths separated by path separator, in addition to default search path (which points :mod:`funge.fp` package). A path separator is semicolon in Windows and colon in Unix.

   Default search path has a priority over search paths set by this one, and this search paths have a priority over search paths set by :option:`-I` option.

