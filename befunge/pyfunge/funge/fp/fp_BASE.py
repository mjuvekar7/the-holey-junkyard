from funge.fingerprint import Fingerprint

class BASE(Fingerprint):
    'I/O for numbers in other bases'

    API = 'PyFunge v2'
    ID = 0x42415345

    @Fingerprint.register('B')
    def output_binary(self, ip):
        ip.push(2)
        self.output_base(ip)

    @Fingerprint.register('H')
    def output_hexadecimal(self, ip):
        ip.push(16)
        self.output_base(ip)

    @Fingerprint.register('I')
    def input_base(self, ip):
        base = ip.pop()
        if not 2 <= base <= 36:
            self.reflect(ip)
            return

        self.platform.flush()

        if base <= 10:
            basechar = range(48, 48 + base)
        else:
            basechar = range(48, 58) + range(65, 65 + (base-10)) + range(97, 97 + (base-10))

        # similar to BufferedPlatform.getint, but with variable base
        getchar = self.platform.getchar
        ungetchar = self.platform.ungetchar
        try:
            # should not read sign. see the comment in BufferedPlatform.getint.

            ch = 0
            while ch not in basechar:
                ch = getchar()

            string = []
            while ch in basechar:
                string.append(ch)
                ch = getchar()

            if ch != 10: ungetchar(ch)
            value = int(''.join(map(chr, string)), base)
        except Exception:
            self.reflect(ip)
        else:
            ip.push(value)

    @Fingerprint.register('N')
    def output_base(self, ip):
        base, n = ip.popmany(2)
        if not 2 <= base <= 36:
            self.reflect(ip)
            return

        if n > 0:
            s = ''
        elif n < 0:
            n = -n
            s = '-'
        else:
            s = '0'

        while n > 0:
            s = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[n % base] + s
            n //= base

        self.platform.putstr(s)

    @Fingerprint.register('O')
    def output_octal(self, ip):
        ip.push(8)
        self.output_base(ip)

