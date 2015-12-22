from funge.fingerprint import Fingerprint

import os

# XXX should mark as unsafe
class FILE(Fingerprint):
    'File I/O functions'

    API = 'PyFunge v2'
    ID = 0x46494C45

    def init(self, ip):
        Fingerprint.init(self, ip)
        self.files = {}
        self.nextfile = 1

    def final(self, ip):
        Fingerprint.init(self, ip)
        for fp, _ in self.files.values():
            fp.close()

    @Fingerprint.register('C')
    def command67(self, ip):
        handle = ip.pop()
        try:
            self.files.pop(handle)[0].close()
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('D')
    def command68(self, ip):
        filename = ip.pop_string()
        try:
            os.remove(filename)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('G')
    def command71(self, ip):
        handle = ip.pop()
        try:
            fp, _ = self.files[handle]
            string = fp.readline()
        except Exception:
            self.reflect(ip)
        else:
            ip.push(handle)
            ip.push_string(string)
            ip.push(len(string))

    @Fingerprint.register('L')
    def command76(self, ip):
        handle = ip.pop()
        try:
            fp, _ = self.files[handle]
            ip.push(handle)
            ip.push(fp.tell())
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('O')
    def command79(self, ip):
        filename = ip.pop_string()
        method = ip.pop()
        buffer = ip.pop_vector()

        try:
            mode = {0: 'rb', 1: 'wb', 2: 'ab', 3: 'r+b', 4: 'w+b', 5: 'a+b'}[method]
            fp = open(filename, mode)
            handle = self.nextfile
            self.nextfile += 1
            self.files[handle] = (fp, buffer)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(handle)

    @Fingerprint.register('P')
    def command80(self, ip):
        string = ip.pop_string()
        handle = ip.pop()
        try:
            fp, _ = self.files[handle]
            fp.write(string)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(handle)

    @Fingerprint.register('R')
    def command82(self, ip):
        nbytes = ip.pop()
        handle = ip.pop()
        try:
            fp, buffer = self.files[handle]
            string = fp.read(nbytes)
        except Exception:
            self.reflect(ip)
        else:
            delta = self.delta_right
            put = ip.space.put
            for ch in string:
                put(buffer, ord(ch))
                buffer += delta
            ip.push(handle)

    @Fingerprint.register('S')
    def command83(self, ip):
        offset, method = ip.popmany(2)
        handle = ip.pop()
        try:
            fp, _ = self.files[handle]
            fp.seek(offset, method) # Python uses same constant for method
        except Exception:
            self.reflect(ip)
        else:
            ip.push(handle)

    @Fingerprint.register('W')
    def command87(self, ip):
        nbytes = ip.pop()
        handle = ip.pop()
        try:
            fp, buffer = self.files[handle]
            delta = self.delta_right
            get = ip.space.get
            cells = []
            for i in xrange(nbytes):
                cells.append(get(buffer) & 255)
                buffer += delta
            string = ''.join(map(chr, cells))
            fp.write(string)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(handle)


