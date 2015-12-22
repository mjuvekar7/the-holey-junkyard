"""Implementation of optional Funge-98 commands (filesystem and concurrent).
"""

from funge.exception import IPStopped
from funge.vector import Vector
from funge.semantics import Semantics
from funge.languages.funge98 import Unefunge98, Befunge98, Trefunge98

import os
from itertools import izip, count

class FilesystemFunge(Semantics):
    is_filesystem = True
    has_systemcmd = True

    @Semantics.register('=')
    def do_execute(self, ip):
        command = ip.pop_string()
        ip.stack.push(self.platform.system(command))

    @Semantics.register('i')
    def input_file(self, ip):
        filename = ip.pop_string()
        flag = ip.pop()
        position = ip.pop_vector()

        try:
            contents = self.platform.readfile(filename)

            if flag & 0x01:
                x = position[0]; ys = position[1:]
                put = ip.space.put
                for ch in contents:
                    put((x,) + ys, ord(ch), False)
                    x += 1
                ip.space.notifyrect(position, position.replace(x - 1))
                size = Vector([x - position[0]] + [1] * (ip.dimension - 1))
            else:
                size = ip.space.putspace(position, contents)

            ip.push_vector(size)
            ip.push_vector(position)
        except IOError:
            self.reflect(ip)

    @Semantics.register('o')
    def output_file(self, ip):
        filename = ip.pop_string()
        flag = ip.pop()
        position = ip.pop_vector()
        size = ip.pop_vector()

        if flag & 0x01:
            trimmed = True
        else:
            trimmed = False

        contents = ip.space.getspace(position, size, trimmed)

        try:
            self.platform.writefile(filename, contents)
        except IOError:
            self.reflect(ip)

class ConcurrentFunge(Semantics):
    is_concurrent = True

    @Semantics.register('@')
    def stop(self, ip):
        raise IPStopped()

    @Semantics.register('t')
    def split(self, ip):
        newip = ip.program.clone_ip(ip)
        self.walk(newip)

# declares all available combinations.
class FilesystemUnefunge98(FilesystemFunge, Unefunge98): pass
class FilesystemBefunge98(FilesystemFunge, Befunge98): pass
class FilesystemTrefunge98(FilesystemFunge, Trefunge98): pass
class ConcurrentUnefunge98(ConcurrentFunge, Unefunge98): pass
class ConcurrentBefunge98(ConcurrentFunge, Befunge98): pass
class ConcurrentTrefunge98(ConcurrentFunge, Trefunge98): pass
class ConcurrentFilesystemUnefunge98(ConcurrentFunge, FilesystemFunge, Unefunge98): pass
class ConcurrentFilesystemBefunge98(ConcurrentFunge, FilesystemFunge, Befunge98): pass
class ConcurrentFilesystemTrefunge98(ConcurrentFunge, FilesystemFunge, Trefunge98): pass

