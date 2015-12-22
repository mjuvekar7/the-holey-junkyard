.. _SCKE:

``"SCKE"`` GLFunge98's extension to SOCK
-----------------------------------------------

:Fingerprint ID: 0x534f434b

.. versionadded:: 0.5-rc2

This fingerprint, from GLfunge98, adds more commands to :ref:`SOCK <SOCK>` fingerprint. It provides the following commands:

``H`` : *host*\ :sup:`s` --- *addr*
    Same to SOCK's ``I`` command, but it could resolve the hostname via :manpage:`gethostbyname(3)`. Reflects on failure.

``P`` : *handle* --- *status*
    Checks read buffer of the socket specified by *handle*. It will then push 1 if the socket has some data to read now, or 0 if not. Reflects on failure.

