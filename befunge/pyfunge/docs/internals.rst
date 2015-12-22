.. _internals:

############
Internals
############

.. module:: funge
   :synopsis: PyFunge package.

All PyFunge modules are contained in :mod:`funge` package. With an exception of front-end modules, all modules are orthogonal to other methods and can be used independently.


:mod:`funge.main` -- PyFunge front-end
========================================

.. module:: funge.main
   :synopsis: Implements front-end of PyFunge. (Meant to be used by driver script)

This front-end is used by the driver script, :ref:`pyfunge-driver`.

.. function:: main(argv)

   Parses given arguments (normally from ``sys.argv``) and does an appropriate action.


:mod:`funge.program` -- Entry point
======================================

.. module:: funge.program
   :synopsis: Executes Funge program.

This module combines all other modules into the execution environment. If you have to run Funge code you may want to use :class:`Program` class.

.. class:: Program(semantics, platform=None, args=None, environ=None, warnings=False)

   The Funge environment class.

   .. attribute:: ips

      The list of :class:`~funge.ip.IP` objects. Every tick IPs are executed in the order listed in the list.

   .. method:: add_ip(ip)

      Adds given IP to the current IP list. If this method is called while :meth:`execute_step` is called, given IP gets executed at first of next call.

   .. method:: remove_ip(ip)

      Removes given IP from the current IP list if any, without any finalization process. This method is useful for *hibernating* IP, for example. Returns given IP, or :const:`None` if none.

   .. method:: create_ip()

      Creates new IP and adds it to current IP list. Returns the new IP.

   .. method:: clone_ip(ip)

      Clones given IP with opposite delta and adds it to current IP list. Returns the new IP.

   .. method:: load_code(code)

      Puts given Funge code string to Funge space.

   .. method:: execute_step()

      Executes instructions at all IPs in the :attr:`ips`. It takes one tick. One can override this method to provide debugger functionality, like :class:`DebuggingProgram`.

   .. method:: execute()

      Calls :meth:`execute_step` forever, until :exc:`~funge.exception.IPQuitted` exception is raised. Returns the exit code from that exception.

      This call is far more efficient than individual :meth:`execute_step` calls, since it optimizes the IP list with length 1 --- very common case. But it will call :meth:`execute_step` anyway if it is overridden.

.. class:: DebuggingProgram(semantics, args, stoppos=None, warnings=None)

   Same to :class:`Program`, but shows the status of IPs each tick. This is intended to provide the minimum debugger functionality.

   The trace will start when any IP hits the cell at *stoppos* in Funge space. If any fatal exception (mainly because of bugs in PyFunge) is raised it will dump current status as well.

   .. method:: dump_ips()

      Dumps the status of IPs.


:mod:`funge.vector` -- Vector classes
========================================

.. module:: funge.vector
   :synopsis: Implements vector classes.

This module implements an efficient vector class(es).

.. class:: Vector(iterable)

   The vector class, which is a subclass of tuple and supports the following operations:

   =========================  ====================================
   Operation                  Meaning
   =========================  ====================================
   ``x + y``                  Pairwise addition
   ``x - y``                  Pairwise subtraction
   ``x * y``                  Pairwise multiplication by scalar
   ``x / y``                  Pairwise integer division by scalar
   ``x // y``                 Pairwise integer division by scalar
   ``x % y``                  Pairwise remainder by scalar
   ``+x``                     *x* unchanged
   ``-x``                     *x* negated
   ``x.between(min, max)``    :const:`True` if every element is between
                              corresponding element of min and max
   ``x.pairwise_min(y)``      Pairwise minimum element
   ``x.pairwise_max(y)``      Pairwise maximum element
   ``x.replace(_0=a, ...)``   Changes particular element
   =========================  ====================================

   The vector class uses different class for different number of dimensions internally, so these operations are more efficient than generic class.

   .. staticmethod:: zero(dimension)

      Returns *dimension*-tuple with all zeroes.

   .. method:: between(min, max)

      Returns :const:`True` only if every element is between corresponding element of *min* and *max*. In the other words, it returns :const:`True` if a point which coordinate is *self* is within a hypercube defined by *min* and *max*, or lies on it.

   .. method:: pairwise_min(vec)

      Returns a vector whose elements greater than corresponding element of *vec* are replaced to it.

   .. method:: pairwise_max(vec)

      Returns a vector whose elements less than corresponding element of *vec* are replaced to it.

   .. method:: replace(_0=None, _1=None, _2=None, ...)

      Returns a vector whose elements are replaced by *_0* (for X coordinate), *_1* (for Y coordinate) and so on. Only non-:const:`None` elements will be replaced.


:mod:`funge.stack` -- Stack stack
====================================

.. module:: funge.stack
   :synopsis: Implements Funge stack stack.

This module implements Funge stack and Funge-98 stack stack.

.. class:: Stack

   One stack. This class is inherited from Python list so all methods and operations of list can be applied.
   
   The following stack operations are unique to this class. Every ``push*`` and ``pop*`` methods has its counterpart, ``rpush*`` and ``rpop*`` methods, only differ that ``r``-prefixed methods treat the stack reversed. For example, :meth:`push` pushes to the top but :meth:`rpush` pushes to the bottom. These counterparts are needed mainly for :meth:`MODE <MODE>` fingerprint.

   .. method:: push(item)
               rpush(item)

      Pushes a value to the top or the bottom of the stack.

   .. method:: pushmany(items)
               rpushmany(items)

      Pushes values to the top or the bottom of the stack. Values will be pushed in the reverse order, so they will be in the given order when popped.

   .. method:: push_string(s)
               rpush_string(s)

      Pushes given string to the top or the bottom of the stack. The string will be pushed as null-terminated one ("0gnirts").

   .. method:: push_vector(v)
               rpush_vector(v)

      Pushes a vector or any iterable to the top or the bottom of the stack. It is mainly used for pushing position or delta (hence the name).

   .. method:: discard(n=1)
               rdiscard(n=1)

      Pops *n* items from the top or the bottom of the stack and discards them. *n* can be larger than the size of the stack.

   .. method:: pop()
               rpop()

      Pops a value from the top or the bottom of the stack and returns it.

      If the stack is empty, it will pop zero.

   .. method:: popmany(n)
               rpopmany(n)

      Pops *n* values from the top or the bottom of the stack and returns them. Values will be returned in the popped order.

      If the stack is empty, it will pop zeroes.

   .. method:: pop_string()
               rpop_string()

      Pops a null-terminated string ("0gnirts") from the top or the bottom of the stack and returns it.

      If the stack is empty, the string ends at the bottom of the stack and it won't raise any exception.

   .. method:: pop_vector(n)
               rpop_vector(n)

      Pops a list of size *n* from the top or the bottom of the stack and return it. A vector will be popped in the pushed order (i.e. the reverse popped order), so it is mainly used for pushing position or delta (hence the name).

      If the stack is empty, one or more first elements will be zero.

   .. method:: clear()

      Empties the stack in place.

.. data:: TOSS
          SOSS

   Refers to the top of stack stack and the second-to-top of stack stack. They can be used for stack stack indices or ``stack`` argument to every stack stack operations.

   They are equal to ``-1`` and ``-2``, respectively. It is recommended that use these symbolic constants than numerical indices.

.. class:: StackStack

   Funge-98 stack stack. It mainly provides convenience methods for accessing the top of stack stack.

   A stack stack itself is organized by Python list, and can be indexed to access individual stack object. For example ``sstack[TOSS]`` returns the top of stack stack, and ``sstack[3]`` returns the 4th stack from the bottom of stack stack. Also ``len(sstack)`` gives the size of stack stack.

   .. attribute:: invertmode

      Gets or sets *invertmode*. If invertmode is enabled push operations push to the bottom, not the top. It is disabled by default, and can be copied by :meth:`copy`.

   .. attribute:: queuemode

      Gets or sets *queuemode*. If queuemode is enabled pop operations pop from the bottom, not the top. It is disabled by default, and can be copied by :meth:`copy`.

   .. method:: push_stack()

      Pushes new empty stack to the top of stack stack.

   .. method:: pop_stack()

      Pops the top of stack stack and discards it.

   .. method:: push(item, stack=TOSS)
               pushmany(items, stack=TOSS)
               push_string(s, stack=TOSS)
               push_vector(v, stack=TOSS)
               discard(n=1, stack=TOSS)
               pop(stack=TOSS)
               popmany(n, stack=TOSS)
               pop_string(stack=TOSS)
               pop_vector(n, stack=TOSS)

      Does given operation on the given *stack*, with current :attr:`invertmode` and :attr:`queuemode`.
      
      For example ``sstack.push(42, TOSS)`` is equal to the following code::

          if sstack.invertmode:
              sstack[TOSS].rpush(42)
          else:
              sstack[TOSS].push(42)

   .. method:: copy()

      Creates a deep copy of the stack stack.


:mod:`funge.space` -- Funge space
====================================

.. module:: funge.space
   :synopsis: Implements bounded and unbounded Funge spaces.

This module implements Funge spaces.

.. class:: Space(dimension, default=32)

   Infinite Funge-98 space. Dimension can be larger than 3 (though :meth:`getspace` and :meth:`putspace` won't work then).

   .. attribute:: boundmin
                  boundmax

      Returns the least and greatest point of rectangle covers every non-space cells in the space. Note that this rectangle can be larger than needed, since calculating the exact bounds is quite expensive. See :meth:`getrect` for the exact bounds.

   .. method:: get(pos)

      Returns the cell at given position, or default value if none. The position can be :class:`~funge.vector.Vector` or tuple.

   .. method:: put(pos, value, update_bounds=True)

      Writes the value to given position. If value is equal to default value, the cell will be removed from the space.

      If *update_bounds* is :const:`False`, it doesn't update :attr:`boundmin` and :attr:`boundmax`. It is useful for putting many cells once, but then you have to notify the change of Funge space using :meth:`notifyrect`.

   .. method:: getspace(pos, size, rtrim=True)

      Captures Funge space given by lowest point and size, and returns the string. If rtrim is :const:`True`, it strips every spaces before newline and every newline before form-feed. This is mainly used for ``o`` command.

   .. method:: putspace(pos, str)

      Writes the string to the space starting at given position. Newline or form-feed is recognized or stripped according to the number of dimension. After writing it, returns the size of written area as a :class:`~funge.vector.Vector`.

   .. method:: getrect()

      Returns the smallest rectangle covers every non-space cells in the Funge space. This is an expensive operation, and mainly exists for ``y`` command.

   .. method:: notifyrect(minpos, maxpos)

      Notifies the given area in the Funge space is updated, and bounds should be recalculated accordingly. *minpos* and *maxpos* is all inclusive, and do not need to be exact rectangle. This method is only useful if you put cells without updating bounds (*update_bounds* argument).

   .. method:: normalize(position, delta)

      Normalizes given position so it is in the bounds and the difference between original and normalized position is a multiple of delta.

   .. method:: scanuntil(position, delta, value)
               scanwhile(position, delta, value)

      Finds the next cell in the path starting at *position* towards *delta*, which is equal (for :meth:`scanuntil`) or not equal (for :meth:`scanwhile`) to given *value*. Returns the coordinate of that cell.

.. class:: BoundedSpace(dimension, rectmin, rectmax, default=32)

   The space with explicit bounds. This is a base class of :class:`Befunge93Space`.

.. class:: Befunge93Space(width=80, height=25)

   The Befunge-93 space, which is two-dimensional, 80 columns wide and 25 rows high by default. It differs from :class:`BoundedSpace` that it treats every cell as 8-bit unsigned integer, as the reference implementation does.


:mod:`funge.ip` -- Instruction pointer
=========================================

.. module:: funge.ip
   :synopsis: Implements Funge instruction pointer.

This module implements Funge instruction pointer, which has independent position, direction and stack stack.

.. class:: IP(program, id, parent=None)

   An instruction pointer (IP). If *parent* is given it is used for initializing default environment (namely :attr:`parentid`, :attr:`position`, :attr:`delta`, :attr:`offset` and :attr:`stack`) of IP.

   .. attribute:: team

      Returns the team identifier of IP. PyFunge does not make use of this, and always sets it to ``1``.

   .. attribute:: id

      Returns the identifier of IP.

   .. attribute:: parentid

      Returns the identifier of parent IP, or :const:`None` if none.

   .. attribute:: dimension

      Returns the number of dimensions in Funge space.

   .. attribute:: space

      Returns the attached Funge space.

   .. attribute:: position

      Returns or sets the position of IP.

   .. attribute:: delta

      Returns or set the direction (delta) of IP.

   .. attribute:: offset

      Returns or set the storage offset of IP. It defaults to the origin.

   .. attribute:: stack

      Returns the attached stack stack.

   .. attribute:: stringmode

      Returns :const:`True` if *stringmode* is set to the IP, or :const:`False` otherwise.

   .. attribute:: invertmode
                  queuemode

      Returns :const:`True` if *invertmode* or *queuemode* is set to the :class:`stack stack <funge.stack.StackStack>`, or :const:`False` otherwise.

      Setting them affects stack stack methods of current IP. Indeed, these attributes are connected to the stack stack attributes.

   .. attribute:: commands

      The commands available to the IP. This is a dictionary that maps the cell value to callbacks: one can execute an arbitrary command by ``ip.commands[instr](ip)``. It should be altered by :meth:`add_commands` and :meth:`remove_commands`.

   .. method:: add_command(command, callback)

      Adds one command with given callback. If callback is :const:`None`, it removes the current command. (But it can be restored with :meth:`remove_command`.)

   .. method:: add_commands(overlay)

      Adds commands from the given semantics overlay, e.g. fingerprint object. See :meth:`add_command` for precise behavior.

      It pushes new command to the internal stack for each cell value. This is required by Funge-98 specification: as a consequence, if :meth:`add_commands` and :meth:`remove_commands` are not called in the correct order it can execute a command from unloaded fingerprint.

   .. method:: remove_command(command)

      Removes one command and restores to the original callback.

   .. method:: remove_commands(overlay)

      Removes commands of the given semantics overlay, e.g. fingerprint object. See :meth:`add_commands` for precise behavior.

   .. method:: load_fingerprint(fpid)

      Loads a fingerprint of given identifier and initializes it. Returns :const:`True` unless the fingerprint is non-existent, or the fingerprint initialization is failed.

   .. method:: unload_fingerprint(fpid)

      Unloads a fingerprint of given identifier and finalizes it. Returns :const:`True` unless the fingerprint is not yet loaded, or the fingerprint finalization is failed.

   .. method:: push(item)
               pushmany(items)
               push_string(s)
               push_vector(v)

      Pushes to the top of the stack stack. They are same to :class:`~funge.stack.StackStack`'s corresponding methods, but affected by :attr:`invertmode` flag.

   .. method:: discard(n=1)
               pop()
               popmany(n)
               pop_string()
               pop_vector()

      Pops from the top of the stack stack. They are same to :class:`~funge.stack.StackStack`'s corresponding methods, but affected by :attr:`queuemode` flag.

      :meth:`pop_vector` is a special case, since it always pops and returns a :class:`~funge.vector.Vector` whose size is same to the number of dimensions in Funge space.


:mod:`funge.exception` -- Exceptions
========================================

.. module:: funge.exception
   :synopsis: Defines package-wide exceptions.

This module defines some package-wide exceptions.

.. exception:: IPStopped

   Raised when the IP hits ``@`` instruction in Funge-98 mode. The caller should remove the IP from the queue.

.. exception:: IPQuitted(exitcode)

   Raised when the IP hits ``@`` instruction in Befunge-93 mode, or ``q`` instruction in Funge-98 mode. The caller should terminate all IPs.


:mod:`funge.semantics` -- Command semantics
=============================================

.. module:: funge.semantics
   :synopsis: Defines a base class for semantics.

This module provides a base class for core semantics (:class:`Semantics`) and overlay (:class:`SemanticsOverlay`).

.. class:: SemanticsBase()

   The base of semantics implementation.

   .. attribute:: commands

      Returns the dictionary maps the cell value to corresponding callback. The callback should have one argument, :class:`~funge.ip.IP` object. This class attribute is automatically generated via :meth:`register` decorator.

   .. staticmethod:: register(commands, \*\*kwargs)

      This is a decorator for commands. Typical example of semantics classes is like this::

          class SomeSemantics(SemanticsBase):
              @SemanticsBase.register('@')
              def squiggle(self, ip):
                  self.platform.warn('IP hit a squiggle! Awwwww!!!')
                  raise IPStopped()

              @SemanticsBase.register('0123456789')
              def numbers(self, ip):
                  self.platform.warn('You should not use numbers. Pushes the answer instead.')
                  ip.push(42)

      *commands* can be a string or a list of character values. *kwargs* are stored in the method directory: they can be used as a hint of the instruction. (Note that PyFunge 0.5.0 doesn't use this hint yet.)

      Commands can be inherited and overridden from other classes. If two different methods implement same command the result is undefined.

.. class:: Semantics(platform)

   Implements a core semantics, usable for an argument to :class:`~funge.program.Program`. It has to implement several methods besides from commands.

   .. staticmethod:: create_space()

      Creates and returns the space appropriate for current semantics.

   .. staticmethod:: init_ip(ip)

      Initializes the given IP at the start of the program. For example, most semantics will initialize IP to travel towards right.

   .. method:: walk(ip)

      Finds the next executable instruction and changes IP's position. By default it moves towards delta and normalizes the position. It should skip spaces or markers in Funge-98 mode.

   .. method:: command(ip)

      Executes one command at current position of IP. Every tick this method and :meth:`walk`  have to be called, since this method alone doesn't seek to next instruction.

   .. method:: undefined(ip)

      Called when IP hits an undefined command.

   .. method:: stringmode(ip)

      Called when string mode is enabled.

.. class:: SemanticsOverlay(semantics)

   Implements *semantics overlay*, which can attach to IP and detach from IP in the runtime. :class:`~funge.fingerprint.Fingerprint` object is a kind of semantics overlay. Its argument is a core semantics and can be called as overlays' method.


:mod:`funge.languages` -- Language implementations
====================================================

.. module:: funge.languages
   :synopsis: Provides language semantics.

This package provides language semantics for Befunge-93 and Funge-98 languages.


:mod:`funge.languages.befunge93` -- Befunge-93 implementation
----------------------------------------------------------------

.. module:: funge.languages.befunge93
   :synopsis: Implements Befunge-93 commands.

This module implements Befunge-93 commands.

.. class:: Unefunge93(platform)

   Implements an one-dimensional subset of Befunge-93 commands. Such language doesn't exist but it is used for the base class of :class:`~funge.languages.funge98.Unefunge98`.

   .. attribute:: delta_right
                  delta_left

      Equal to ``Vector(self.dimension).replace(_0=-1)`` and ``Vector(self.dimension).replace(_0=1)``, respectively.

.. class:: Befunge93(platform)

   Implements full Befunge-93 commands.

   .. attribute:: delta_up
                  delta_down

      Equal to ``Vector(self.dimension).replace(_1=-1)`` and ``Vector(self.dimension).replace(_1=1)``, respectively.

.. class:: Befunge93_divbyzero_stop(platform)

   Same to :class:`Befunge93` class, but IP terminates with exit code if division by zero occurs.

.. class:: Befunge93_divbyzero_value(platform, divbyzero)

   Same to :class:`Befunge93` class, but pushes given value if division by zero occurs.


:mod:`funge.languages.funge98` -- Core Funge-98 implementation
------------------------------------------------------------------

.. module:: funge.languages.funge98
   :synopsis: Implements core Funge-98 commands.

This module implements core Funge-98 commands. "Core" means no filesystem Funge and no concurrent Funge: see :mod:`funge.languages.funge98opt` module for those.

.. class:: Unefunge98(platform)

   Implements core Unefunge-98 commands.

.. class:: Befunge98(platform)

   Implements core Befunge-98 commands.

.. class:: Trefunge98(platform)

   Implements core Trefunge-98 commands.

   .. attribute:: delta_high
                  delta_low

      Equal to ``Vector(self.dimension).replace(_2=-1)`` and ``Vector(self.dimension).replace(_2=1)``, respectively.


:mod:`funge.languages.funge98opt` -- Concurrent and filesystem Funges
-----------------------------------------------------------------------

.. module:: funge.languages.funge98opt
   :synopsis: Implements concurrent and filesystem Funge commands.

This module implements additional concurrent and filesystem Funge commands.

.. class:: FilesystemFunge(platform)

   Implements filesystem Funge commands (``=``, ``i``, ``o``). This is a base class for real languages.

.. class:: ConcurrentFunge(platform)

   Implements concurrent Funge commands (``t``, ``@``). This is a base class for real languages.

.. class:: FilesystemUnefunge98(platform)
           FilesystemBefunge98(platform)
           FilesystemTrefunge98(platform)
           ConcurrentUnefunge98(platform)
           ConcurrentBefunge98(platform)
           ConcurrentTrefunge98(platform)
           ConcurrentFilesystemUnefunge98(platform)
           ConcurrentFilesystemBefunge98(platform)
           ConcurrentFilesystemTrefunge98(platform)

   Implements filesystem or concurrent Funge commands along with core Funge-98 commands. There are nine such combinations provided.


:mod:`funge.platform` -- Platform abstraction
===============================================

.. module:: funge.platform
   :synopsis: Abstracts the external system.

This module defines a class for interfacing with external system.

.. class:: Platform(args, environ, warnings=False)

   Base class for platform abstraction. The classes should override I/O functions, and optionally file-related functions or :meth:`system`.

   .. attribute:: args

      Returns the list of command-line arguments.

   .. attribute:: environ

      Returns the dictionary of environment variables.

   .. method:: warn(message)

      Optionally displays the warning.

   .. method:: prompt(message, process=...)

      Displays given message and prompts for input. When the user inputs, it is processed with process callback and returned. If the callback raises the exception it prompts again. By default process returns given line unchanged.

   .. method:: flush()

      Flushes the output. It is only explicitly called before the user inputs.

   .. method:: getchar()

      Reads one character from the input and returns its code.

   .. method:: ungetchar(ch)

      Pushes given character code back to input buffer. Next :meth:`getchar` should return that character.

   .. method:: putchar(ch)

      Writes one character whose code is ch to the output.

   .. method:: getint()

      Reads one integer from the input. It follows Funge-98 specification so discards every non-digits. If you have to input an interpreter-specific thing use :meth:`prompt` instead.

   .. method:: putint(num)

      Writes the integer and one space character to the output.

   .. method:: putstr(s)

      Prints the given string to the output.

   .. method:: readfile(filename)

      Returns the contents of given file, or raises the exception on failure.

   .. method:: writefile(filename, data)

      Writes given contents to the file, or raises the exception on failure.

   .. method:: system(command)

      Executes given command and returns the exit code.

.. class:: BufferedPlatform(args, environ, stdin=sys.stdin, stdout=sys.stdout, warnings=False)

   A platform with buffered input; it only reads whole line when the buffer is empty. It also automatically flushes when printing newline.


:mod:`funge.fingerprint` -- Fingerprint management
====================================================

.. module:: funge.fingerprint
   :synopsis: Manages Funge-98 fingerprints.

This module provides a lookup and base class for Funge-98 fingerprints.

.. class:: FingerprintLookup()

   This class manages a list of available fingerprints.

   .. method:: module_from_name(name)

      Returns a module object from given name, like ``funge.fp.fp_NULL``.

   .. method:: search_module(mod)

      Searches fingerprint classes from the given module, and returns a list of them. See :class:`Fingerprint` for criteria.

   .. method:: add_module(name)

      Adds all fingerprint classes available from a module of the given name to the lookup.

   .. method:: add_class(cls)

      Adds a fingerprint class to the lookup.

.. class:: Fingerprint(semantics)

   A fingerprint object. It is a :class:`~funge.semantics.SemanticsOverlay` with additional methods below.

   Fingerprint class, to be added by :class:`FingerprintLookup`, should have two attributes: ``API`` and ``ID``. The former identifies the incompatible revisions of fingerprint API, where current revision is ``"PyFunge v2"``. (This is only supported revision for now.) The latter is a fingerprint identifier, like ``0x4e554c4c`` for ``NULL`` fingerprint.

   .. method:: init(ip)

      This method is executed when IP loads the fingerprint object. By default it registers itself to IP via :meth:`IP.add_commands() <funge.ip.IP.add_commands>` method.

   .. method:: final(ip)

      This method is executed when IP unloads the fingerprint object. By default it unregisters itself from IP via :meth:`IP.remove_commands() <funge.ip.IP.remove_commands>` method.


:mod:`funge.fp` -- Fingerprints
===================================

.. module:: funge.fp
   :synopsis: Contains default fingerprints.

This package contains implementations of default fingerprints. The complete list of modules is:

* :mod:`funge.fp.fp_3DSP` for :ref:`3DSP`
* :mod:`funge.fp.fp_BASE` for :ref:`BASE`
* :mod:`funge.fp.fp_BOOL` for :ref:`BOOL`
* :mod:`funge.fp.fp_CPLI` for :ref:`CPLI`
* :mod:`funge.fp.fp_DATE` for :ref:`DATE`
* :mod:`funge.fp.fp_DIRF` for :ref:`DIRF`
* :mod:`funge.fp.fp_EVAR` for :ref:`EVAR`
* :mod:`funge.fp.fp_FILE` for :ref:`FILE`
* :mod:`funge.fp.fp_FIXP` for :ref:`FIXP`
* :mod:`funge.fp.fp_FPDP` for :ref:`“FPDP” Double precision floating point <FPDP>`
* :mod:`funge.fp.fp_FPRT` for :ref:`FPRT`
* :mod:`funge.fp.fp_FPSP` for :ref:`“FPSP” Single precision floating point <FPSP>`
* :mod:`funge.fp.fp_FRTH` for :ref:`FRTH`
* :mod:`funge.fp.fp_HRTI` for :ref:`HRTI`
* :mod:`funge.fp.fp_ICAL` for :ref:`ICAL`
* :mod:`funge.fp.fp_IIPC` for :ref:`IIPC`
* :mod:`funge.fp.fp_IMAP` for :ref:`IMAP`
* :mod:`funge.fp.fp_IMTH` for :ref:`IMTH`
* :mod:`funge.fp.fp_INDV` for :ref:`INDV`
* :mod:`funge.fp.fp_JSTR` for :ref:`JSTR`
* :mod:`funge.fp.fp_LONG` for :ref:`LONG`
* :mod:`funge.fp.fp_MODE` for :ref:`MODE`
* :mod:`funge.fp.fp_MODU` for :ref:`MODU`
* :mod:`funge.fp.fp_NCRS` for :ref:`NCRS`
* :mod:`funge.fp.fp_NULL` for :ref:`NULL`
* :mod:`funge.fp.fp_ORTH` for :ref:`ORTH`
* :mod:`funge.fp.fp_PERL` for :ref:`PERL`
* :mod:`funge.fp.fp_REFC` for :ref:`REFC`
* :mod:`funge.fp.fp_ROMA` for :ref:`ROMA`
* :mod:`funge.fp.fp_SCKE` for :ref:`SCKE`
* :mod:`funge.fp.fp_SETS` for :ref:`SETS`
* :mod:`funge.fp.fp_SOCK` for :ref:`SOCK`
* :mod:`funge.fp.fp_STRN` for :ref:`STRN`
* :mod:`funge.fp.fp_SUBR` for :ref:`SUBR`
* :mod:`funge.fp.fp_TERM` for :ref:`TERM`
* :mod:`funge.fp.fp_TIME` for :ref:`TIME`
* :mod:`funge.fp.fp_TOYS` for :ref:`TOYS`

