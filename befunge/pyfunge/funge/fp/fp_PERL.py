from funge.fingerprint import Fingerprint

import subprocess

class PERL(Fingerprint):
    'Generic Interface to the Perl Language'

    API = 'PyFunge v2'
    ID = 0x5045524c

    def eval_perl(self, code):
        return subprocess.Popen(['perl', '-e', 'print eval($ARGV[0])', code],
                stdout=subprocess.PIPE).communicate()[0]

    @Fingerprint.register('E')
    def eval(self, ip):
        code = ip.pop_string()
        try:
            ip.push_string(self.eval_perl(code))
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('I')
    def eval_int(self, ip):
        code = ip.pop_string()
        try:
            ip.push(int(self.eval_perl(code)))
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('S')
    def shelled(self, ip):
        ip.push(1) # perl interpreter shall be shelled as needed

