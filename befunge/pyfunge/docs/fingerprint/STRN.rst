.. _STRN:

``"STRN"`` String functions
-----------------------------

:Fingerprint ID: 0x5354524e

This fingerprint, from `RC/Funge-98`__, implements operations on null-terminated string ("0gnirts"). It provides the following commands:

__ http://www.rcfunge98.com/rcsfingers.html#STRN

``A`` : *a*\ :sup:`s` *b*\ :sup:`s` --- *str*\ :sup:`s`
    Append *b* to *a*.

``C`` : *b*\ :sup:`s` *a*\ :sup:`s` --- *n*
    Pushes -1 if *a* is lexicographically less than *b*, 1 if greater than, and 0 otherwise.

``D`` : *str*\ :sup:`s` ---
    Prints the string.

``F`` : *needle*\ :sup:`s` *haystack*\ :sup:`s` --- *str*\ :sup:`s`
    Pushes the longest suffix of *haystack* starting with *needle*. Pushes null string (i.e. one zero) if *needle* is not in *haystack*.

``G`` : *pos*\ :sup:`v` --- *str*\ :sup:`s`
    Gets the string from given position. It scans Funge space rightwards, from *pos* to first zero cell (as done by ``P`` command). Reflects if no zero cell found.

``I`` : --- *str*\ :sup:`s`
    Reads the string from standard input, discarding the trailing newline. Reflects at EOF.

``L`` : *str*\ :sup:`s` *n* --- *str*\ :sup:`s`
    Pushes leftmost (at most) *n* characters of *str*. Reflects if *n* is negative.

``M`` : *str*\ :sup:`s` *s* *n* --- *str*\ :sup:`s`
    Pushes the substring of *str* starting at offset *s* ending at offset *s*\ +\ *n*. The offset is 0 at the first character. If the ending offset is past the end of string, pushes less than *n* characters. Reflects if *n* is negative or the starting offset is out of bound.

``N`` : *str*\ :sup:`s` *n* --- *str*\ :sup:`s`
    Pushes the length of string, except trailing zero. Retains the original string.

``P`` : *str*\ :sup:`s` *pos*\ :sup:`v` ---
    Puts the string to given position. It writes each characters of *str* rightwards, and writes zero cell at the end.

``R`` : *str*\ :sup:`s` *n* --- *str*\ :sup:`s`
    Pushes rightmost (at most) *n* characters of *str*. Reflects if *n* is negative.

``S`` : *n* --- *str*\ :sup:`s`
    Pushes the string representation of *n*.

``V`` : *str*\ :sup:`s` --- *n*
    Parses the string representation of number. It works like :manpage:`atoi(3)` call, but reflects for invalid input.

