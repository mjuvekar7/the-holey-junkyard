from funge.fingerprint import Fingerprint

class REFC(Fingerprint):
    'Referenced Cells Extension'

    API = 'PyFunge v2'
    ID = 0x52454643

    def init(self, ip):
        Fingerprint.init(self, ip)

        try:
            self.references = ip.program.REFC_references
        except AttributeError:
            self.references = ip.program.REFC_references = {}
            ip.program.REFC_nextref = 1

    @Fingerprint.register('D')
    def dereference(self, ip):
        handle = ip.pop()
        try:
            ip.push_vector(self.references[handle])
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('R')
    def reference(self, ip):
        vector = ip.pop_vector()
        handle = ip.program.REFC_nextref
        ip.program.REFC_nextref += 1
        self.references[handle] = vector
        ip.push(handle)

