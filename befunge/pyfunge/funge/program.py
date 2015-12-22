"""Main entry point to Funge program.

This module connects all other modules: funge.semantics for Funge commands,
funge.space for Funge space, funge.ip for individual IP, funge.stack for
stack stack, funge.fingerprint for fingerprints, and funge.platform for
platform-dependent operations.

One should use this module to execute Funge code, unless internal information
is needed (e.g. writing debugger).
"""

from funge.vector import Vector
from funge.stack import TOSS, SOSS
from funge.ip import IP
from funge.fingerprint import FingerprintLookup
from funge.platform import BufferedPlatform
from funge.exception import IPQuitted, IPStopped

import sys, os

class Program(object):
    FUNGE_HANDPRINT = 0x50794698 # "PyF\x98"
    FUNGE_VERSION = 492 # 0.5-rc2

    def __init__(self, semantics, platform=None, args=None, environ=None,
            warnings=False):
        if args is None:
            args = sys.argv
        if environ is None:
            environ = os.environ
        if platform is None:
            cls = BufferedPlatform # XXX
            platform = cls(args=args, environ=environ, warnings=warnings)

        self.semantics = semantics(platform)
        self.space = self.semantics.create_space()
        self.platform = platform
        self.fplookup = FingerprintLookup()
        self.ips = []
        self.ipnext = 1

    def generate_ipid(self):
        id = self.ipnext
        self.ipnext += 1
        return id

    def add_ip(self, ip):
        self.ips.insert(0, ip)
        return ip

    def remove_ip(self, ip):
        try:
            self.ips.remove(ip)
            return ip
        except ValueError:
            return None

    def create_ip(self):
        id = self.generate_ipid()
        ip = IP(self, id)
        self.semantics.init_ip(ip)
        return self.add_ip(ip)

    def clone_ip(self, ip):
        newip = IP(self, self.generate_ipid(), parent=ip)
        newip.delta = -newip.delta
        self.add_ip(newip)
        return newip

    def load_code(self, code):
        self.space.putspace((0,) * self.space.dimension, code)

    def execute_step(self):
        i = 0
        for ip in self.ips[:]:
            try:
                self.semantics.command(ip)
                self.semantics.walk(ip)
            except IPStopped:
                del self.ips[i]
                ip.final()
            except IPQuitted:
                origips = self.ips[:]
                del self.ips[:]
                for ip in origips:
                    ip.final()
                raise
            else:
                i += 1

    def execute(self):
        ips = self.ips
        try:
            if self.execute_step.im_func is Program.execute_step.im_func:
                # shortcut for execute_step. (im_func is required for identity test)
                command = self.semantics.command
                walk = self.semantics.walk
                while ips:
                    while len(ips) == 1:
                        ip = ips[0]
                        try:
                            command(ip)
                            walk(ip)
                        except IPStopped:
                            del ips[:]
                            ip.final()
                        except IPQuitted:
                            del ips[:]
                            ip.final()
                            raise

                    while len(ips) > 1:
                        i = 0
                        for ip in ips[:]:
                            try:
                                command(ip)
                                walk(ip)
                            except IPStopped:
                                del ips[i]
                                ip.final()
                            except IPQuitted:
                                origips = ips[:]
                                del ips[:]
                                for ip in origips:
                                    ip.final()
                                raise
                            else:
                                i += 1
            else:
                execute_step = self.execute_step
                while ips: execute_step()
            return 0
        except IPQuitted, err:
            return err.exitcode

class DebuggingProgram(Program):
    def __init__(self, semantics, args, stoppos=None, warnings=False):
        Program.__init__(self, semantics, args=args, warnings=warnings)
        self.stopposition = stoppos

    def dump_ips(self):
        flag = False
        for ip in self.ips:
            if flag:
                print >>sys.stderr, '|',
            else:
                flag = True

            print >>sys.stderr, '%d:' % ip.id,
            try:
                print >>sys.stderr, chr(self.space.get(ip.position)),
            except Exception:
                print >>sys.stderr, ' ',
            print >>sys.stderr, ip.position, ip.delta, len(ip.stack[TOSS]),
            if len(ip.stack) > 1:
                print >>sys.stderr, ip.stack[SOSS][-20:],
            print >>sys.stderr, ip.stack[TOSS][-20:],

    def execute_step(self):
        if any(ip.position == self.stopposition for ip in self.ips):
            self.debugging = True

        if self.debugging:
            self.dump_ips()
            raw_input()
        Program.execute_step(self)

    def execute(self):
        self.debugging = False
        try:
            return Program.execute(self)
        except Exception:
            print >>sys.stderr, '-' * 60
            self.dump_ips()
            print >>sys.stderr
            raise

