.. _EVAR:

``"EVAR"`` Environment variables extension
--------------------------------------------

:Fingerprint ID: 0x45564152

This fingerprint, from `RC/Funge-98`__, manages the environment variables given by ``y`` command. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#EVAR

``G`` : *name*\ :sup:`s` --- *value*\ :sup:`s`
    Pushes the value of given environment variable as a string. If it doesn't exist pushes null string.

``N`` : --- *n*
    Pushes the number of environment variables.

``P`` : *namevalue*\ :sup:`s` ---
    Sets the environment variable. The string should be a form of ``name=value``, or it reflects.

``V`` : *i* --- *namevalue*\ :sup:`s`
    Gets the *i*-th environment variable, counting from zero. The pushed string is a form of ``name=value``. Unlike ``y`` environment variables retrieved by ``V`` is sorted. Reflects if *i* is invalid.

