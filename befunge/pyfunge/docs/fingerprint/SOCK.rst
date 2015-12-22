.. _SOCK:

``"SOCK"`` TCP/IP socket extension
-----------------------------------------------

:Fingerprint ID: 0x534f434b

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements commands for the network socket, including but not limited to TCP and UDP (contraty to the name). It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#SOCK

``A`` : *handle* --- *remoteport* *remoteaddr* *newhandle*
    Accepts a connection from the socket specified by *handle*. (Same to :manpage:`accept(2)`.) On success, it pushes the remote address information and new socket handle for communicating to the other end.

``B`` : *handle* *family* *port* *addr* ---
    Binds the socket specified by *handle* to listen from *addr* and *port*. (Same to :manpage:`bind(2)`.) It cannot be used after prior ``B`` or ``C`` commands.

    *family* is checked for validity (see ``S`` command for possible values), but PyFunge doesn't use that value.

``C`` : *handle* *family* *port* *addr* ---
    Connects the socket specified by *handle* to *addr* and *port*. (Same to :manpage:`connect(2)`.) It cannot be used after prior ``B`` or ``C`` commands.

    *family* is checked for validity (see ``S`` command for possible values), but PyFunge doesn't use that value.

``I`` : *addr*\ :sup:`s` --- *addr*
    Converts the IPv4 address representation to integer representation, suitable to use in the other commands. (Same to :manpage:`inet_aton(3)`.) Reflects if *addr* is in the invalid format.

``K`` : *handle* ---
    Shuts (or kills) down the socket specified by *handle*. (Same to :manpage:`shutdown(2)` and :manpage:`close(2)`.) Once killed socket cannot be used any more.

``L`` : *backlog* *handle* ---
    Listens from the socket specified by *handle*, with the given backlog size. (Same to :manpage:`listen(2)`.)

``O`` : *value* *option* *handle* ---
    Sets the option to the socket specified by *handle*. (Same to :manpage:`setsockopt(2)`.) *option* can be one of the following values:

    - If *option* is 1, it refers to ``SO_DEBUG`` option.
    - If *option* is 2, it refers to ``SO_REUSEADDR`` option.
    - If *option* is 3, it refers to ``SO_KEEPALIVE`` option.
    - If *option* is 4, it refers to ``SO_DONTROUTE`` option.
    - If *option* is 5, it refers to ``SO_BROADCAST`` option.
    - If *option* is 6, it refers to ``SO_OOBINLINE`` option.
    - Otherwise it reflects.

``R`` : *target* *size* *handle* --- *nread*
    Reads *size* bytes from the socket specified by *handle*. (Same to :manpage:`recv(2)`.) Read bytes are stored to the Funge space starting at *target* (relative to the storage offset) rightwards, and actual number of bytes read is pushed. Reflects if *size* is negative.

``S`` : *family* *type* *protocol* --- *handle*
    Creates the socket with given *protocol*, *type* and *family*. (Same to :manpage:`socket(2)`.) The arguments can be one of the following values:

    - If *family* is 1, it refers to the Unix socket (``AF_UNIX``). If *family* is 2, it refers to the IPv4 socket (``AF_INET``).
    - If *type* is 1, it refers to the datagram socket (``SOCK_DGRAM``). If *type* is 2, it refers to the stream socket (``SOCK_STREAM``).
    - If *protocol* is 1, it refers to TCP. If *protocol* is 2, it refers to UDP. This *protocol* value is different from actual value given to :manpage:`socket(2)`, as it uses :manpage:`getprotocobyname(3)` call.
    - If one or more arguments are invalid, it reflects.

``S`` : *source* *size* *handle* --- *nwritten*
    Writes *size* bytes to the socket specified by *handle*. (Same to :manpage:`send(2)`.) Written bytes are read from the Funge space starting at *target* (relative to the storage offset) rightwards, and actual number of bytes written is pushed. Reflects if *size* is negative.

All commands reflect on failure.

