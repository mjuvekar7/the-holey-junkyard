.. _MODE:

``"MODE"`` Funge-98 Standard Modes
--------------------------------------

:Fingerprint ID: 0x4d4f4445

This fingerprint, from `Cat's Eye Technologies`__, implements four modes applicable to IP. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/MODE.html

``H`` : ---
    Toggles *hovermode* on and off. Hovermode is disabled by default. If hovermode is enabled the following commands are altered:

    ``<`` : ---
        Decreases X component of delta: in the other words it accelerates delta leftwards.

    ``^`` : ---
        Decreases Y component of delta: in the other words it accelerates delta upwards. Reflects in Unefunge mode.

    ``l`` : ---
        Decreases Z component of delta: in the other words it accelerates delta towards lower layers. Reflects in Unefunge and Befunge mode.

    ``>`` : ---
        Increases X component of delta: in the other words it accelerates delta rightwards.

    ``v`` : ---
        Increases Y component of delta: in the other words it accelerates delta downwards. Reflects in Unefunge mode.

    ``h`` : ---
        Increases Z component of delta: in the other words it accelerates delta towards upper layers. Reflects in Unefunge and Befunge mode.

    ``_`` : *value* ---
        Acts like modified semantics of ``<`` and ``>``.

    ``|`` : *value* ---
        Acts like modified semantics of ``^`` and ``v``. Reflects in Unefunge mode.

    ``m`` : *value* ---
        Acts like modified semantics of ``l`` and ``h``. Reflects in Unefunge and Befunge mode.

    The original specification didn't mention about ``l``, ``h`` and ``m`` commands, but it is logical to extend hovermode to them.

``I`` : ---
    Toggles *invertmode* on and off. If invertmode is enabled, IP pushes the value to the bottom instead of the top of the stack.

``Q`` : ---
    Toggles *queuemode* on and off. If queuemode is enabled, IP pops the value from the bottom instead of the top of the stack.

``S`` : ---
    Toggles *switchmode* on and off. If switchmode is enabled the following commands are altered:

    ``[`` : ---
        Acts like Funge-98 ``[`` command, but also changes the current cell in the Funge space to ``]``.

    ``]`` : ---
        Acts like Funge-98 ``]`` command, but also changes the current cell in the Funge space to ``[``.

    ``{`` : ... *n* --- *offset*; ...
        Acts like Funge-98 ``{`` command, but also changes the current cell in the Funge space to ``}``.

    ``}`` : *offset*; ... *n* ---
        Acts like Funge-98 ``}`` command, but also changes the current cell in the Funge space to ``{``.

    ``(`` : *id*\ :sup:`A` --- *idvalue* 1
        Acts like Funge-98 ``(`` command, but also changes the current cell in the Funge space to ``)``.

    ``)`` : *id*\ :sup:`A` ---
        Acts like Funge-98 ``)`` command, but also changes the current cell in the Funge space to ``(``.

