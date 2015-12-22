.. _FILE:

``"FILE"`` File I/O functions
-------------------------------

:Fingerprint ID: 0x46494c45

This fingerprint, from `RC/Funge-98`__, implements file-related functions. It uses an IP-local list of file handles associated to I/O buffer in the Funge space. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#FILE

``C`` : *handle* ---
    Closes the file.

``D`` : *path*\ :sup:`s` ---
    Removes the given file.

``G`` : *handle* --- *handle* *line*\ :sup:`s` *len*
    Reads one line from the given file. Also pushes the number of characters so it can detect mid-line null characters. Pushes null string at EOF.

``L`` : *handle* --- *handle* *pos*\ :sup:`v`
    Pushes the current location of the given file pointer.

``O`` : *bufpos*\ :sup:`v` *mode* *path*\ :sup:`s` --- *handle*
    Opens a file with given mode and I/O buffer.

    - If *mode* is 0, the file can be only read. (``fopen``'s ``"r"`` mode)
    - If *mode* is 1, the file can be only written and it truncates at first. (``fopen``'s ``"w"`` mode)
    - If *mode* is 2, the file can be only written but it starts at end of the file. (``fopen``'s ``"a"`` mode)
    - If *mode* is 3, the file can be both read and written and it starts at start of the file. (``fopen``'s ``"r+"`` mode)
    - If *mode* is 4, the file can be both read and written but it truncates at first. (``fopen``'s ``"w+"`` mode)
    - If *mode* is 5, the file can be both read and written but it starts at end of the file. (``fopen``'s ``"a+"`` mode)
    - Everything else is error.

``P`` : *handle* *str*\ :sup:`s` --- *handle*
    Writes the string to the given file.

``R`` : *handle* *n* --- *handle*
    Reads *n* bytes from the file, and writes it to I/O buffer in Funge space rightwards.

``S`` : *handle* *mode* *n* --- *handle*
    Changes the given file pointer.

    - If *mode* is 0, the file pointer is set to *n*-th byte from beginning.
    - If *mode* is 1, the file pointer is set to *n*-th byte from current location.
    - If *mode* is 2, the file pointer is set to *n*-th byte from end. (useful for files opened for append)
    - Everything else is error.

``W`` : *handle* *n* --- *handle*
    Reads *n* bytes from I/O buffer in Funge space rightwards, and writes it to the file.

All commands reflects on failure. For every string written to the file only the least significant byte is used. When the fingerprint is unloaded every opened files are closed automatically.

