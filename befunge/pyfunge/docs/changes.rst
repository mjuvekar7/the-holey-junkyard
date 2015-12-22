.. _changes:

#####################
Changes in PyFunge
#####################


.. _version-0.5-rc2:

0.5-rc2 (2009-04-24)
====================

* Bug fixes.

  - Befunge-93 space now treats the cell as 8-bit unsigned integer.
  - New IPs cloned by ``t`` command are now guaranteed to be executed before parent IP.
  - ``u`` command does obey queuemode and invertmode from :ref:`MODE <MODE>`.
  - ``F`` command of :ref:`TIME <TIME>` was off by one. (0 should mean the first day of year.)

* Internal API changes. These changes don't affect ``PyFunge v2`` fingerprint API, but does require some trivial changes.

  - The return value of command callback (previously used to be walk flag) is now unused. Fingerprint modules for 0.5-rc1 will work correctly, but I strongly recommends to return :const:`None` (or don't use ``return`` at all) always.
  - :meth:`funge.semantics.Semantics.execute` is gone, due to the prior change.
  - :meth:`funge.semantics.Semantics.walk` is now a part of public API.
  - Individual access to :meth:`funge.stack.Stack` is strongly discouraged. You should use :meth:`funge.ip.IP`'s stack stack wrapper instead. (If your fingerprint works on the stack stack, your code can be affected.)
  - :attr:`funge.ip.IP.th_id` and :attr:`th_team <funge.ip.IP.th_team>` became :attr:`funge.ip.IP.id` and :attr:`team <funge.ip.IP.team>`. :attr:`funge.ip.IP.parentid` is also available now.
  - :meth:`funge.space.Space.put` has an optional third argument to optimize bulk changes to Funge space. You can use :meth:`funge.space.Space.notifyrect` with it.
  - :attr:`funge.space.Space.rectmin` and :attr:`rectmax <funge.space.Space.rectmax>` became :attr:`funge.space.Space.boundmin` and :attr:`boundmax <funge.space.Space.boundmax>`. If you want the exact bounds use :meth:`funge.space.Space.getrect` instead.

* Extensive optimizations resulted in 10--30% overall speed-up.

  - :meth:`funge.space.Space.putspace` is 3x faster for huge code (say, more than 10000 commands).
  - :meth:`funge.space.Space.scanwhile` and :meth:`scanuntil <funge.space.Space.scanuntil>` is 2x faster for general case. These methods were bottlenecks of entire Funge code execution.
  - The stack API is revised to perform well even with or without invertmode and queuemode.
  - :meth:`funge.program.Program.execute` now special-cases single IP, and 2x faster for that case.

* New Funge-98 fingerprints: :ref:`3DSP <3DSP>`, :ref:`ICAL <ICAL>`, :ref:`IIPC <IIPC>`, :ref:`IMAP <IMAP>`, :ref:`IMTH <IMTH>`, :ref:`LONG <LONG>`, :ref:`NCRS <NCRS>`, :ref:`PERL <PERL>`, :ref:`SCKE <SCKE>`, :ref:`SETS <SETS>`, :ref:`SOCK <SOCK>`, :ref:`SUBR <SUBR>` and :ref:`TERM <TERM>`.

* Provides the complete documentation. Earlier version has some missing sections yet to be written.

* More regression tests in ``tests/`` directory.


.. _version-0.5-rc1:

0.5-rc1 (2009-04-15)
====================

* Full Befunge-98 compliance.

  - Rewrote problematic IP walking algorithm to get correct behavior of ``#``, ``'``, ``s`` and concurrency.
  - Fixed ``[`` and ``]`` command which got swapped.
  - Fixed ``/`` and ``%`` command so division by zero results in zero, not reflects.
  - Corrected ``k`` command. (Meaning of it was quite dubious, but now clear)
  - Fixed ``{``, ``}`` and ``u`` command which had a number of bugs, including treating the argument with incorrect sign.
  - ``:`` always pushes two items, even if the stack has one or zero items.
  - Fixed faulty treatment of Unefunge and Befunge source code.
  - Almost complete change in internal API.

* A lot of code restructuring and refactoring.

  - All packages are merged into :mod:`funge` package.
  - Renamed internal classes.
  - ``funge.execute`` module splits into :mod:`funge.languages` package.
  - Introduced :class:`funge.vector.Vector` class for convenience.

* Big improvement in performance (10x-40x speed gain), including:

  - More efficient space-related algorithms; they are also used only when needed. (8x speed gain)
  - Added dimension-dependent, caching Vector class. (2x speed gain)
  - General code simplification. (1.5x-2x speed gain)

* New command-line front-end, allowing the direct execution of all available languages.
* New fingerprint implementation, which API dubbed "PyFunge v2". (See :ref:`writing-fingerprint` for more information)
* Implemented more fingerprints. (See :ref:`funge98-fingerprints` for more information)
* Added the regression test suite. (See :ref:`tests` for more information)
* Moved to `Mercurial <http://www.selenic.com/mercurial/>`_ repository.


.. _version-0.2-beta1:

0.2-beta1 (2004-06-11)
========================

* Initial release.

