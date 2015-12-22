.. _introduction:

##############
Introduction
##############

PyFunge is an interpreter for Funge family of languages, written in Python (hence the name).

If you are not familiar to these languages, see `What is Funge?`_ subsection. If you consider yourself a Funge expert, skip to :ref:`invocation` section.


What is Funge?
================

Funge is a family of languages based on multi-dimensional grid. Sounds strange? Look this famous example::
       
                             v
         v"Hello, world!"*250<
    ,_@#:<

This *program* prints "Hello, world!" to standard output. You should see a visible flow of execution, as every characters (even whitespaces, though they are practically ignored) in the code is significant. Let's follow how this code is executed.

Funge has a notion of instruction pointer (IP) and direction (delta). IP determines what character is to be executed, while delta determines what direction IP should be updated. Every Funge program starts at left-top corner, with IP moving right.

The program encounters first non-space character at top-right corner, which is ``v``. It makes IP move down next time, and it encounters another flow-controlling command, ``<``, which makes IP move left. Obviously there are more such commands, including ``>`` for right and ``^`` for up.

Next command, ``0``, pushes zero to the stack. *What? There's a stack?* Yeah, that's right. Funge has the stack used for mostly everything, and here the program pushes the string to be printed. Next two command ``5`` and ``2`` also pushes that number to the stack, and ``*`` performs a multiplication: pops two numbers and pushes the product of them, in this case 10.

Next series of commands, ``"!dlrow ,olleH"`` (in the execution order), pushes the string to the stack. ``"`` is special: it enables *stringmode* so commands except ``"`` pushes a code of that exact character. Since the first pushed item is popped last, we have to push the string in reverse order. That's why IP and delta is set to move left.

When IP is at third line it loops over the string. ``:`` duplicates the top of stack, ``#`` skips next command, ``_`` pops one number and makes IP move left or right according to that number, ``,`` pops the number and prints one character with that code, and finally ``@`` terminates the program. Well, of course this cannot explain this program.

Since one character must be both checked if that's end of string and printed, we have to duplicate the character for later use. ``_`` tests the duplicated character: IP moves left if it is nonzero, right if it is zero. Because IP has moved from right we have to separate two code flow, and we end up using ``#`` so normal loop won't trigger ``@``.

And when IP hits leftmost boundary of code it *warps* to rightmost boundary, so it will make the loop. Thus after printing "Hello, world!" and newline (code 10), the top of stack has zero and it finally terminates.

This hopefully shows the feature of Funge, except that the program can modify itself via ``g`` and ``p`` command. It is, as you have seen, quite hard to follow the program and code in, as you have to think of direction every time; though it is an interesting concept it has few practical usage. There is even a word for such programming language: `esoteric programming language`_. That's mostly for fun and intellectual challenge.

.. _`esoteric programming language`: http://en.wikipedia.org/wiki/Esoteric_programming_language


Funge *family* of languages
=============================

Funge is not a single language: it had several revisions, it doesn't have to two-dimensional only, and so on.

Above example is written in Befunge-93. It was the first [1]_ language of Funge family (1993), and the space is confined within 80 columns and 25 lines. It makes the interpreter simple but also limits what Befunge-93 programs can do. Befunge-93 was followed by mostly forgotten extensions like Befunge-97, that was finally followed by Funge-98 (1998).

Funge-98 is a feature-rich extension to Befunge-93, as it gives the program nearly-infinite multi-dimensional space, several stacks (called *stack stack*), interaction with external system, and extension mechanism. It makes full conformance quite challenging and there is even an extensive and very large test suite for Befunge-98, Mycology_.

.. _Mycology: http://users.tkk.fi/~mniemenm/befunge/mycology.html

Funge-98 standard defines three languages: Unefunge-98 for one-dimensional space, Befunge-98 for two-dimensional space, Trefunge-98 for three-dimensional space. The standard also mentions a possibility for other kinds of code space, though it's yet to be realized.

.. [1] Note that this was not the first multi-dimensional language: see Biota_ for example.
.. _Biota: http://esolangs.org/wiki/Biota


What's PyFunge then?
======================

PyFunge started its life in 2004 as toy implementation of Funge languages, with certain degrees of abstraction so most things can be easily replaced with other concepts. While it has been forgotten for five years, I (Kang Seonghoon) revived the project in 2009 right after I saw aforementioned Mycology_ test suite mentions it.

Now its goal is a comprehensive implementation of Funge languages, not limited to just an interpreter, but a optimizing compiler (very hard!), graphical IDE and useful tools for Funge programmers.

