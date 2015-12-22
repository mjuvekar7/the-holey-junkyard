from funge.fingerprint import Fingerprint

import socket
import struct

def pop_family(ip):
    return {1: socket.AF_UNIX, 2: socket.AF_INET}[ip.pop()]

def pop_type(ip):
    return {1: socket.SOCK_DGRAM, 2: socket.SOCK_STREAM}[ip.pop()]

def pop_proto(ip):
    return socket.getprotobyname({1: 'tcp', 2: 'udp'}[ip.pop()])

def pop_sockopt(ip):
    return {1: socket.SO_DEBUG, 2: socket.SO_REUSEADDR,
            3: socket.SO_KEEPALIVE, 4: socket.SO_DONTROUTE,
            5: socket.SO_BROADCAST, 6: socket.SO_OOBINLINE}[ip.pop()]

def pop_address(ip):
    host, port = ip.popmany(2)
    host = struct.pack('I', host)
    return (socket.inet_ntoa(host), port)

def push_address(ip, addr):
    host, port = addr
    ip.push(port)
    ip.push(struct.unpack('I', socket.inet_aton(host))[0])

class SOCK(Fingerprint):
    'tcp/ip socket extension'

    API = 'PyFunge v2'
    ID = 0x534F434B

    def init(self, ip):
        Fingerprint.init(self, ip)
        if not hasattr(ip.program, 'SOCK_sockets'):
            ip.program.SOCK_sockets = {}
            ip.program.SOCK_nextid = 1

    @Fingerprint.register('A')
    def accept(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]

            newsock, addr = sock.accept()
            newid = ip.program.SOCK_nextid
            ip.program.SOCK_sockets[newid] = newsock
            ip.program.SOCK_nextid += 1
        except Exception:
            self.reflect(ip)
        else:
            push_address(ip, addr)
            ip.push(newid)

    @Fingerprint.register('B')
    def bind(self, ip):
        try:
            addr = pop_address(ip)
            family = pop_family(ip)
            sock = ip.program.SOCK_sockets[ip.pop()]
            sock.bind(addr)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('C')
    def connect(self, ip):
        try:
            addr = pop_address(ip)
            family = pop_family(ip)
            sock = ip.program.SOCK_sockets[ip.pop()]
            sock.connect(addr)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('I')
    def from_address(self, ip):
        try:
            addr = socket.inet_aton(ip.pop_string())
            ip.push(struct.unpack('I', addr)[0])
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('K')
    def shutdown(self, ip):
        try:
            sock = ip.program.SOCK_sockets.pop(ip.pop())
            sock.close()
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('L')
    def listen(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]
            n = ip.pop()
            sock.listen(n)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('O')
    def setsockopt(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]
            option = pop_sockopt(ip)
            value = ip.pop()
            sock.setsockopt(socket.SOL_SOCKET, option, value)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('R')
    def read(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]
            length = ip.pop()
            buffer = ip.pop_vector() + ip.offset
            if length < 0:
                self.reflect(ip)
                return
            str = sock.recv(length)
        except Exception:
            self.reflect(ip)
        else:
            for ch in str:
                ip.space.put(buffer, ord(ch))
                buffer += self.delta_right
            ip.push(len(str))

    @Fingerprint.register('S')
    def socket(self, ip):
        try:
            proto = pop_proto(ip)
            type = pop_type(ip)
            family = pop_family(ip)

            sock = socket.socket(family, type, proto)
            newid = ip.program.SOCK_nextid
            ip.program.SOCK_sockets[newid] = sock
            ip.program.SOCK_nextid += 1
        except Exception:
            self.reflect(ip)
        else:
            ip.push(newid)

    @Fingerprint.register('W')
    def write(self, ip):
        try:
            sock = ip.program.SOCK_sockets[ip.pop()]
            length = ip.pop()
            buffer = ip.pop_vector() + ip.offset
            if length < 0:
                self.reflect(ip)
                return

            str = ''
            for i in xrange(length):
                str += chr(ip.space.get(buffer))
                buffer += self.delta_right
            result = sock.send(str)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(result)

