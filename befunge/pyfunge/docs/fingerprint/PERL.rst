.. _PERL:

``"PERL"`` Generic Interface to the Perl Language
----------------------------------------------------

:Fingerprint ID: 0x5045524c

.. versionadded:: 0.5-rc2

This fingerprint, from `Cat's Eye Technologies`__, implements a basic interface to `Perl programming language <http://perl.org/>`_. It provides the following commands:

__ http://catseye.tc/projects/funge98/library/PERL.html

``E`` : *code*\ :sup:`s` --- *result*\ :sup:`s`
    Evaluates *code* (via Perl ``eval()``) and returns its stringified result. Reflects on any failure.

``I`` : *code*\ :sup:`s` --- *result*
    Evaluates *code* (via Perl ``eval()``) and returns its integer result. Reflects on any failure, or when the result is not a integer.

``S`` : --- *shelled*
    Pushes 1 if the Perl interpreter should be shelled. Since PyFunge is obviously not written in Perl, it pushes 0 always.

