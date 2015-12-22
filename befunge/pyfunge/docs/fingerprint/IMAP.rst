.. _IMAP:

``"IMAP"`` Instruction remap extension
------------------------------------------

:Fingerprint ID: 0x494d4150

.. versionadded:: 0.5-rc2

This fingerprint, from `RC/Funge-98`__, implements the commands remapping other commands. It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#IMAP

``C`` : ---
    Clears all command mappings.

``M`` : *newcmd* *oldcmd* ---
    Makes the *oldcmd* does behave like the *newcmd*. *newcmd* itself is not affected.

``O`` : *cmd* ---
    Restores the command *cmd* to the original function.

There are many options regarding to this fingerprint, due to a freedom allowed by the specification. PyFunge uses the following rules:

- Any command can be remapped. For example, you can set next cell to be executed to -42 and remap command -42 to ``z`` so IP won't reflect. Of course, even you remap some command to the space it will take one tick.
- PyFunge does not support chained remapping, so ``M`` command always look up *newcmd* from the original command list. In the other words, if you remap ``v`` as ``^`` and ``^`` as ``v`` it won't cause an infinite loop and rather swaps two commands. Despite that PyFunge's structure makes the chained remap easier than non-chained remap, PyFunge sticks to this behavior since it prohibits an infinite loop.
- There is a distinction between actual commands and remappings: if ``(`` and ``)`` changes command mapping, it will change actual commands and won't touch remappings. But after they are executed the original remapping will be restored. For example assuming ``X`` is remapped to ``Y``, ``X`` command in the new fingerprint won't affect both ``X`` and ``Y`` mappings, and ``Y`` will affect both ``X`` and ``Y``.
- Even after IMAP fingerprint is unloaded, the mapping will be retained and could be changed after IMAP fingerprint is reloaded then.

