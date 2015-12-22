"""PyFunge command-line frontend."""

from funge import __version__ as VERSION
from funge.program import Program, DebuggingProgram
from funge.fingerprint import FingerprintLookup
from funge.languages import befunge93, funge98, funge98opt

import os, sys
import os.path
import time
import getopt
import string


import funge.fp
DEFAULT_FPRINT_PATH = [os.path.dirname(funge.fp.__file__)]
if os.environ.get('PYFUNGE_FPRINT_PATH'):
    DEFAULT_FPRINT_PATH += os.environ.get['PYFUNGE_FPRINT_PATH'].split(os.pathsep)
DEFAULT_FPRINTS = [name[3:] for name in funge.fp.__all__ if name.startswith('fp_')]

def version():
    print >>sys.stderr, '''\
PyFunge %s
the functional, compliant and (to be) optimizing Funge-98 implementation.
Copyright (c) 2004, 2009, Kang Seonghoon and contributors.
''' % VERSION

def usage(progname):
    version()
    print >>sys.stderr, '''\
Usage: %s [options] filename [args...]

General options:
-h, --help
    Shows this message.
-V, --version
    Shows version of PyFunge.
-w, --warnings
    Enable warnings, for example, when encountering unimplemented insructions.
-x, --skip-first-line
    Skip first line of the source code. Useful for #! lines.

Funge options:
-v standard, --std standard
    Selects the supported language standards.
        "93", "befunge93" and so on
            Run in Befunge-93 mode.
        "98", "funge98" and so on
            Run in Funge-98 mode. (default)
-d dimension, --dimension dimension
    Sets how many dimensions are in the Funge space.
        "1"
            Run in Unefunge (one-dimensional) mode.
        "2"
            Run in Befunge (two-dimensional) mode. (default)
        "3"
            Run in Trefunge (three-dimensional) mode.
-1, --unefunge
    Short for "--dimension 1".
-2, --befunge
    Short for "--dimension 2".
-3, --trefunge
    Short for "--dimension 3".
--statistics
    Shows statistics after the program is terminated.

Befunge-93 options:
--division-by-zero value
    Sets default value when dividing by zero.
        number
            Division by zero results in given value.
        "prompt"
            PyFunge will ask for a result of division by zero. (default)
        "stop"
            The program will be terminated when dividing by zero.
    If warning is enabled and "--division-by-zero prompt" is not used,
    the warning will be issued in such case.

Funge-98 options:
-f fingerprints, --fprint fingerprints
    Comma-delimited list of fingerprints to be used. Fingerprints are
    implemented via Python modules which name prepended with "fp_".
    For example, to load fp_SAMP.py you have to use "-f SAMP".
    Type "--list-fprints" for available and default fingerprints.
--disable-fprint
    Disable all fingerprints.
-I fingerprintpath, --fprint-include fingerprintpath
    Uses given path as additional Python import path when loading fingerprints. 
    See also PYFUNGE_FPRINT_PATH environment variable.
--concurrent
    Enable the concurrent funge. (default)
--filesystem
    Enable the filesystem funge. (default)
-C, --no-concurrent
    Disable the concurrent funge.
-F, --no-filesystem
    Disable the filesystem funge.
--list-fprints
    Lists all available fingerprints and exits. -I option affects this output
    if exists, so it can verify custom fingerprints.

Environment variables:
PYFUNGE_NO_PSYCO
    By default PyFunge uses Psyco for performance. When this variable is set
    Psyco is disabled. (Useful for profiling or some Psyco-unfriendly OSes)
PYFUNGE_FPRINT_PATH
    Same to -I option, but with lower precedence. Syntax is same to PYTHONPATH
    environment variable, i.e. delimited by "%s".
''' % (progname, os.pathsep)

def list_fingerprints(fprintpath):
    lookup = FingerprintLookup()
    allmodules = []
    for path in fprintpath:
        for fname in os.listdir(path):
            if not (fname.startswith('fp_') and fname.endswith('.py')): continue
            modname = fname[:-3]
            if modname not in allmodules:
                allmodules.append((modname[3:], modname))

    print >>sys.stderr, 'All fingerprints available:'
    print >>sys.stderr
    for name, modname in allmodules:
        mod = lookup.module_from_name(modname)
        for obj in lookup.search_module(mod):
            if not hasattr(obj, 'ID'): continue

            try:
                asciiname = ('%x' % obj.ID).decode('hex')
                if any(ch not in string.printable for ch in asciiname):
                    asciiname = None
            except ValueError:
                asciiname = None

            try:
                desc = obj.__doc__.splitlines()[0]
            except Exception:
                desc = ''

            if asciiname:
                print >>sys.stderr, '    %#x "%s" %s' % (obj.ID, asciiname, desc)
            else:
                print >>sys.stderr, '    %#x %s' % (obj.ID, desc)
            print >>sys.stderr, '        Commands: %s' % ','.join(map(chr, obj.commandmap))
            print >>sys.stderr

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hVwxv:d:123f:I:CF',
                ['help', 'version', 'warnings', 'skip-first-line', 'std=',
                 'dimension=', 'unefunge', 'befunge', 'trefunge', 'statistics',
                 'division-by-zero=', 'fprint=', 'disable-fprint', 'fprint-include=',
                 'concurrent', 'filesystem', 'no-concurrent', 'no-filesystem',
                 'list-fprints'])
    except getopt.GetoptError, err:
        print >>sys.stderr, 'Error: %s' % err
        print >>sys.stderr, 'Type "%s --help" for usage.' % argv[0]
        return 1

    warnings = False
    skipfirstline = False
    fprints = DEFAULT_FPRINTS[:]
    fprintpath = DEFAULT_FPRINT_PATH[:]
    standard = dimension = None
    statistics = False
    divbyzero = None
    concurrent = filesystem = None
    listfprints = False
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(argv[0])
            return 0
        elif opt in ('-V', '--version'):
            version()
            return 0
        elif opt in ('-w', '--warnings'):
            warnings = True
        elif opt in ('-x', '--skip-first-line'):
            skipfirstline = True
        elif opt in ('-v', '--std'):
            iarg = arg.lower().replace('-','')
            if iarg in ('93', 'befunge93'):
                standard = 93
            elif iarg in ('98', 'funge98'):
                standard = 98
            else:
                print >>sys.stderr, 'Error: Invalid language standard %r.' % arg
                return 1
        elif opt in ('-d', '--dimension'):
            if arg in ('1', '2', '3'):
                dimension = int(arg)
            else:
                print >>sys.stderr, 'Error: Invalid dimension %r.' % arg
                return 1
        elif opt in ('-1', '--unefunge'):
            dimension = 1
        elif opt in ('-2', '--befunge'):
            dimension = 2
        elif opt in ('-3', '--trefunge'):
            dimension = 3
        elif opt == '--statistics':
            statistics = True
        elif opt == '--division-by-zero':
            try:
                divbyzero = int(arg)
            except ValueError:
                divbyzero = arg.lower()
                if divbyzero not in ('prompt', 'stop'):
                    print >>sys.stderr, 'Error: Invalid division by zero option %r.' % arg
                    return 1
        elif opt in ('-f', '--fprint'):
            fprints = filter(None, map(str.strip, arg.split(',')))
        elif opt == '--disable-fprint':
            fprints = []
        elif opt in ('-I', '--fprint-include'):
            fprintpath.append(arg.strip())
        elif opt == '--concurrent':
            concurrent = True
        elif opt == '--filesystem':
            filesystem = True
        elif opt in ('-C', '--no-concurrent'):
            concurrent = False
        elif opt in ('-F', '--no-filesystem'):
            filesystem = False
        elif opt == '--list-fprints':
            listfprints = True
        else:
            assert False

    sys.path.extend(fprintpath)
    if listfprints:
        list_fingerprints(fprintpath)
        return 0

    if not args:
        version()
        print >>sys.stderr, 'Type "%s --help" for usage.' % argv[0]
        return 0

    filename = args[0]
    if filename.endswith('.bf'):
        if dimension is None: dimension = 2
        if standard is None: standard = 93
    elif filename.endswith('.u98'):
        if dimension is None: dimension = 1
        if standard is None: standard = 98
    elif filename.endswith('.b98'):
        if dimension is None: dimension = 2
        if standard is None: standard = 98
    elif filename.endswith('.t98'):
        if dimension is None: dimension = 3
        if standard is None: standard = 98
    if dimension is None: dimension = 2

    if standard == 93:
        if concurrent is not None or filesystem is not None:
            print >>sys.stderr, 'Error: Befunge-93 doesn\'t support concurrent or filesystem funge.'
            return 1
        if dimension != 2:
            print >>sys.stderr, 'Error: Befunge-93 only supports two-dimensional space.'
            return 1
        if divbyzero == 'prompt' or divbyzero is None:
            semantics = befunge93.Befunge93
        elif divbyzero == 'stop':
            semantics = befunge93.Befunge93_divbyzero_stop
        else:
            semantics = lambda plat: befunge93.Befunge93_divbyzero_value(plat, divbyzero)
    elif standard == 98:
        if divbyzero is not None:
            print >>sys.stderr, 'Error: Funge-98 doesn\'t support --division-by-zero option.'
            return 1
        if concurrent is None: concurrent = True
        if filesystem is None: filesystem = True
        semantics = {
            (1, False, False): funge98.Unefunge98,
            (1, False, True): funge98opt.FilesystemUnefunge98,
            (1, True, False): funge98opt.ConcurrentUnefunge98,
            (1, True, True): funge98opt.ConcurrentFilesystemUnefunge98,
            (2, False, False): funge98.Befunge98,
            (2, False, True): funge98opt.FilesystemBefunge98,
            (2, True, False): funge98opt.ConcurrentBefunge98,
            (2, True, True): funge98opt.ConcurrentFilesystemBefunge98,
            (3, False, False): funge98.Trefunge98,
            (3, False, True): funge98opt.FilesystemTrefunge98,
            (3, True, False): funge98opt.ConcurrentTrefunge98,
            (3, True, True): funge98opt.ConcurrentFilesystemTrefunge98,
        }[dimension, concurrent, filesystem]
    else:
        print >>sys.stderr, 'Error: Cannot detect language standard. Use "-v 93" or "-v 98".'
        return 1

    if filename == '-':
        fp = sys.stdin
    else:
        try:
            fp = open(filename, 'rb')
        except Exception, err:
            print >>sys.stderr, 'Error: Cannot read source code; %s' % err
            return 1
    if skipfirstline: fp.readline()
    code = fp.read()

    # XXX debugging purpose only, more robust debugger needed
    try:
        stoppos = eval('(' + os.environ['pyfunge_stopat'] + ')')
        prog = DebuggingProgram(semantics, args, stoppos=stoppos, warnings=warnings)
    except Exception:
        prog = Program(semantics, args=args, warnings=warnings)

    for fpmod in fprints:
        prog.fplookup.add_module('fp_' + fpmod)
    prog.load_code(code)
    prog.create_ip()

    if filename != '-':
        dirname = os.path.dirname(filename)
        if dirname != '':
            try:
                os.chdir(dirname)
            except Exception, err:
                print >>sys.stderr, 'Error: Cannot chdir into source directory; %s' % err
                return 1
    exitcode = prog.execute()
    return exitcode

