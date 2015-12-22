"""Platform-dependent abstractions."""

import os, sys

class Platform(object):
    def __init__(self, args, environ, warnings=False):
        self.args = args
        self.environ = environ
        self.warnings = warnings

    def warn(self, message):
        if self.warnings:
            print >>sys.stderr, 'Warning: %s' % message

    def prompt(self, message, process=(lambda s:s)):
        while 1:
            sys.stderr.write(message)
            try:
                return process(raw_input())
            except Exception:
                pass

    def flush(self): raise NotImplemented
    def getchar(self): raise NotImplemented
    def putchar(self, ch): raise NotImplemented
    def getint(self): raise NotImplemented
    def putint(self, num): raise NotImplemented
    def putstr(self, s): raise NotImplemented
    def readfile(self, filename): raise NotImplemented
    def writefile(self, filename, data): raise NotImplemented
    def system(self, command): raise NotImplemented

class BufferedPlatform(Platform):
    unbuffered_io = False

    def __init__(self, args, environ, stdin=sys.stdin, stdout=sys.stdout, warnings=False):
        Platform.__init__(self, args, environ, warnings=warnings)
        self.stdin = stdin
        self.stdout = stdout
        self.linebuffer = ''

    def flush(self):
        self.stdout.flush()

    def getchar(self):
        if not self.linebuffer:
            self.linebuffer = self.stdin.readline()
        ch = self.linebuffer[0]
        self.linebuffer = self.linebuffer[1:]
        return ord(ch)

    def ungetchar(self, ch):
        self.linebuffer = chr(ch & 0xff) + self.linebuffer

    def putchar(self, ch):
        ch &= 0xff
        self.stdout.write(chr(ch))
        if ch == 10: self.flush()

    def getint(self):
        # getint should not read negative sign. from funge-98 spec:
        #
        #   Decimal input reads and discards characters until it encounters
        #   decimal digit characters, at which point it reads a decimal number
        #   from those digits, up until (but not including) the point at which
        #   input characters stop being digits, or the point where the next
        #   digit would cause a cell overflow, whichever comes first. 
        #
        # note that since python integer doesn't overflow, second condition is
        # always false.

        self.flush()

        # search for first digit
        ch = 0
        while not 48 <= ch < 58:
            ch = self.getchar()

        # read number
        num = 0
        while 48 <= ch < 58:
            num = num * 10 + ch - 48
            ch = self.getchar()

        if ch != 10: self.ungetchar(ch)
        return num

    def putint(self, num):
        self.stdout.write('%d ' % num)

    def putstr(self, s): 
        self.stdout.write(s)
        if '\n' in s: self.flush()

    def readfile(self, filename):
        f = open(filename, 'r')
        data = f.read()
        f.close()
        return data

    def writefile(self, filename, data):
        f = open(filename, 'w')
        f.write(data)
        f.close()

    def system(self, command):
        return os.system(command)

