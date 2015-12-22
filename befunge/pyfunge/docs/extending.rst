.. _extending:

#####################
Extending PyFunge
#####################

PyFunge can be extended with various means. In particular, since PyFunge comes as a library you can experiment with them. (See :ref:`internals` for extensive API documentation.)


.. _writing-fingerprint:

Writing fingerprint
=====================

You can write your own Funge-98 fingerprints and use them in PyFunge. Thanks to Python's dynamic nature, PyFunge can directly load your fingerprint; even fingerprints shipped with PyFunge are dynamically loaded.

The typical Funge-98 fingerprint looks like this::

    from funge.fingerprint import Fingerprint

    class HELO(Fingerprint):
        'Prints "Hello, world!"'

        API = 'PyFunge v2'
        ID = 0x48454c4f

        @Fingerprint.register('P')
        def print_hello(self, ip):
            self.platform.putstr('Hello, world!\n')

        @Fingerprint.register('S')
        def store_hello(self, ip):
            ip.push_string('Hello, world!\n')

You can save this Python code as ``fp_HELO.py`` and load it with :option:`-f`::

    $ pyfunge -f HELO -v98 -
    "OLEH"4(PS>:#,_@
    (EOF)
    Hello, world!
    Hello, world!

The name of Python code is not important, so you can change it to anything like ``fp_abracadabra.py`` and use correct option (in this case ``-f abracdabra``). Even one module can contain several fingerprints. But by convention it uses same name with the ASCII representation of fingerprint ID, and only contains one fingerprint.

From now on this document assume that you are friendly in Python, or at least have written some programs in it.


Fingerprint class
---------------------

Every fingerprint has a common base class: :class:`funge.fingerprint.Fingerprint`. Actually this class provides nothing, besides from ``register`` decorator used to register new command. After the fingerprint module is imported PyFunge scans for a subclass of Fingerprint, and instantiates it when ``(`` is executed.

Let's analyze the HELO fingerprint above. It needs two attributes to function correctly.

* ``API`` attribute says this fingerprint class is written for the correct API version. It should be ``"PyFunge v2"`` for current version. If the later version changes fingerprint API, it will work hard to support earlier versions.
* ``ID`` attribute says this fingerprint is mapped to the given ID. In this example, we use ID 0x48454c4f, or ``HELO`` in the ASCII representation.

In addition you can give a docstring to describe this fingerprint shortly. Of course that is optional, and will only be seen with :option:`--list-fprints`.

Then it registers two commands: ``P`` and ``S``. This command callback receives one parameter (not counting for *self*), *ip*. This object, an instance of :class:`funge.ip.IP` class, exposes many methods and attributes:

* :attr:`~funge.ip.IP.dimension` gives the number of dimension.
* :attr:`~funge.ip.IP.position` gives the current position of IP. You can also change it.
* :attr:`~funge.ip.IP.delta` gives the current direction (delta) of IP. You can also change it.
* :attr:`~funge.ip.IP.space` gives the attached Funge space. You can read from Funge space via :meth:`~funge.space.Space.get` or write to it via :meth:`~funge.space.Space.put`.
* :meth:`~funge.ip.IP.push` pushes one value to the stack. You can also use :meth:`~funge.ip.IP.push_string` or :meth:`~funge.ip.IP.push_vector` to push a null-terminated string or vector.
* Likewise, :meth:`~funge.ip.IP.pop`, :meth:`~funge.ip.IP.pop_string` and :meth:`~funge.ip.IP.pop_vector` pops one value, string or vector from the stack. It ignores the stack underflow and returns zeroes for your convenience.
* :meth:`~funge.ip.IP.popmany` is handy; you can replace ``c = ip.pop(); b = ip.pop(); a = ip.pop()`` with ``c, b, a = ip.popmany(3)``.

Command callbacks are ordinary methods in the fingerprint class; the decorator, i.e. ``@Fingerprint.register(...)``, does register those methods for later use. The command can be two or more characters, in that case it registers many same commands::

    @Fingerprint.register('0123456789')
    def push_number(self, ip):
        ip.push(ip.space.get(ip.position) - ord('0'))

Fingerprint class itself got many methods from the underlying semantics. For example, ``self.reflect(ip)`` will reflect the IP. (Actual method is in :class:`funge.languages.funge98.Unefunge98` --- check it!) Also you can walk to next instruction, using ``self.walk(ip)``.

One last thing to note is a :class:`~funge.vector.Vector` class, since every coordinates in PyFunge is a vector. For example you can change the delta of IP to non-cardinal one::

    @Fingerprint.register('K')
    def knight_walk(self, ip):
        import random

        if random.randint(0, 1):
            x, y = 1, 2
        else:
            x, y = 2, 1
        if random.randint(0, 1): x = -x
        if random.randint(0, 1): y = -y

        ip.delta = Vector.zero(ip.dimension).replace(_0=x, _1=y)

Since we deal not only with Befunge but Trefunge, we should build a generic vector. This won't work in Unefunge, but you can add some sanity check for it::

    @Fingerprint.register('K')
    def knight_walk(self, ip):
        # reflect in Unefunge.
        if ip.dimension < 2:
            self.reflect(ip)
            return

        # ...


Initialization and finalization
----------------------------------

The fingerprint class can have two special methods: :meth:`init` and :meth:`final`. These methods also receives the IP parameter, and are executed right after ``(`` or ``)``.

::

    class USLS(Fingerprint):
        'Some useless fingerprint without any command.'
        API = 'PyFunge v2'; ID = 0x55534c53

        def init(self, ip):
            self.platform.putstr('Hey, you just loaded the useless fingerprint.\n')

        def final(self, ip):
            self.platform.putstr('Hey, you just unloaded the useless fingerprint.\n')

By default these methods register the commands to IP, so you may want to call the original methods in Fingerprint if you override them::

    def init(self, ip):
        Fingerprint.init(self, ip)
        self.platform.putstr('Hey, you just loaded the useless fingerprint and '
                             '(possibly) some commands.\n')

If these methods raise the exception the loading or unloading rolls back and ``(`` or ``)`` reflects. But you still have to roll back your own changes, if any::

    def init(self, ip):
        Fingerprint.init(self, ip)
        if self.some_check():
            # check failed: rolls back and raise the exception.
            Fingerprint.final(self, ip) # unregisters already registered commands
            raise RuntimeError('check failed!')

Also note that these methods can be executed out of order, and it is possible that the command callback is called even after :meth:`final` method is called. So work can be done in :meth:`final` is in fact quite limited.


Storing additional information
--------------------------------

Sometimes your fingerprint needs to store some informations, like IP flags or call stack. Since Python is a dynamic language you are free to store them in any context, but you have to know where to store exactly.

If the information is only stored between the load and unload, you can just store it in the fingerprint class::

    def init(self, ip):
        Fingerprint.init(self, ip)
        self.exoticflag = False

    @Fingerprint.register('X')
    def toggle_exotic(self, ip):
        self.exoticflag = not self.exoticflag

If the information is local to IP (but should be retained after unload), you can store it in the IP object. If the information is global you should store it in the :class:`~funge.program.Program` object (``ip.program``). Since they are public objects, you have to use some unique prefix for the name.

::

    def init(self, ip):
        Fingerprint.init(self, ip)

        # initialize default value if none.
        if not hasattr(ip, 'EXOT_exoticflag'):
            ip.EXOT_exoticflag = False
        if not hasattr(ip.program, 'EXOT_globalflag'):
            ip.program.EXOT_globalflag = False

    @Fingerprint.register('X')
    def toggle_exotic(self, ip):
        if ip.pop():
            ip.program.EXOT_globalflag = not ip.program.EXOT_globalflag
        else:
            ip.EXOT_exoticflag = not ip.EXOT_exoticflag

In the any case, do not use the global variable besides from constants. It won't work correctly.

