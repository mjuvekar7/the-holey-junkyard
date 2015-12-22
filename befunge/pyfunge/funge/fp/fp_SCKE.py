from funge.fingerprint import Fingerprint

import socket
import select
import struct

class SCKE(Fingerprint):
    'GLFunge98\'s extension to SOCK'

    API = 'PyFunge v2'
    ID = 0x53434b45

    def init(self, ip):
        Fingerprint.init(self, ip)
        # SCKE shares same socket mappings with SOCK.
        if not hasattr(ip.program, 'SOCK_sockets'):
            ip.program.SOCK_sockets = {}
            ip.program.SOCK_nextid = 1

    @Fingerprint.register('H')
    def gethostbyname(self, ip):
        try:
            addr = socket.inet_aton(socket.gethostbyname(ip.pop_string()))
            ip.push(struct.unpack('I', addr)[0])
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('P')
    def peek(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]
            result = select.select([sock.fileno()], [], [], 0)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(len(result[0]))

