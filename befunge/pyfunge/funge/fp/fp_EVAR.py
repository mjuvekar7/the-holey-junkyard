from funge.fingerprint import Fingerprint

class EVAR(Fingerprint):
    'Environment variables extension'

    API = 'PyFunge v2'
    ID = 0x45564152

    @Fingerprint.register('G')
    def command71(self, ip):
        name = ip.pop_string()
        try:
            ip.push_string(self.platform.environ[name])
        except Exception:
            ip.push(0)

    @Fingerprint.register('N')
    def command78(self, ip):
        ip.push(len(self.platform.environ))

    @Fingerprint.register('P')
    def command80(self, ip):
        namevalue = ip.pop_string()
        if '=' not in namevalue:
            self.reflect(ip)
        else:
            name, value = namevalue.split('=', 1)
            self.platform.environ[name] = value

    @Fingerprint.register('V')
    def command86(self, ip):
        environ = self.platform.environ
        n = ip.pop()
        if 0 <= n < len(environ):
            # should be consistent with previous result, unless environ is changed
            name = sorted(environ.keys())[n]
            ip.push_string('%s=%s' % (name, environ[name]))
        else:
            self.reflect(ip)

