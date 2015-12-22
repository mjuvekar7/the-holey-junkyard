.. _DIRF:

``"DIRF"`` Directory functions extension
-------------------------------------------

:Fingerprint ID: 0x44495246

This fingerprint, from `RC/Funge-98`__, implements directory-related functions. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#DIRF

``C`` : *path*\ :sup:`s` ---
    Changes current working directory to given directory.

``M`` : *path*\ :sup:`s` ---
    Creates given directory.

``R`` : *path*\ :sup:`s` ---
    Removes given directory.

All commands reflects on failure.

