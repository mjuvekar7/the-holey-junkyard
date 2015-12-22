.. _installation:

##############
Installation
##############


Requirements
===============

PyFunge requires, obviously, `Python <http://python.org>`_ installation to run. You'll require Python 2.4 or later.

For IA-32 platform, PyFunge makes use of `Psyco <http://psyco.sourceforge.net/>`_ for better performance. You can expect 2 or 3 times speed-up with Psyco, since PyFunge uses very tight and hard-to-optimize loop to execute Funge program.


Installing
==============

If you have `easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_, you can type the following command to install PyFunge::

    $ easy_install PyFunge

Or you can download the source archive from `the official website <http://mearie.org/projects/pyfunge/>`_ and extract it. :file:`funge/` directory contains the entire :mod:`funge` package, and :file:`pyfunge` is an executable :ref:`driver script <pyfunge-driver>`. The former should go into your library directory (normally ``site-packages``), and the latter should go into your binary (normally ``/usr/local/bin``).

The source distribution also contains a documentation in :file:`docs/` directory, which is what you're now reading. For building the documentation you need `Sphinx <http://sphinx.pocoo.org/>`_, version 0.4 or later. Alternatively you can read the most recent documentation at `here <http://packages.python.org/PyFunge/>`__.


Self-check
=============

The source distribution contains some Funge test suites in :file:`tests/`. You check out them against current PyFunge version with :file:`pyfunge-test` shell script::

    $ ./pyfunge-test
    Done, XX out of XX test(s) passed.

If there are any outstanding messages it didn't pass the tests. For more information about these tests, see :ref:`tests`.

