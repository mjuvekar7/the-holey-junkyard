from funge.exception import IPStopped
from funge.stack import TOSS
from funge.fingerprint import Fingerprint

class IIPC(Fingerprint):
    'Inter IP communication extension'

    API = 'PyFunge v2'
    ID = 0x49495043

    def init(self, ip):
        Fingerprint.init(self, ip)
        if not hasattr(ip.program, 'IIPC_dormantips'):
            ip.program.IIPC_dormantips = []

    def search_ip(self, program, id, resume):
        for ip in program.ips:
            if ip.id == id: return ip
        for ip in program.IIPC_dormantips:
            if ip.id == id:
                if resume:
                    program.IIPC_dormantips.remove(ip)
                    program.add_ip(ip)
                return ip
        return None

    @Fingerprint.register('A')
    def get_ancestor(self, ip):
        ip.push(ip.parentid)

    @Fingerprint.register('D')
    def go_dormant(self, ip):
        ip.program.IIPC_dormantips.append(ip)
        ip.program.remove_ip(ip) # remove myself from queue, but prevent from finalization

    @Fingerprint.register('G')
    def pop(self, ip):
        targetip = self.search_ip(ip.program, ip.pop(), True)
        if targetip is None:
            self.reflect(ip)
        else:
            ip.push(targetip.pop())

    @Fingerprint.register('I')
    def get_self(self, ip):
        ip.push(ip.id)

    @Fingerprint.register('L')
    def peek(self, ip):
        targetip = self.search_ip(ip.program, ip.pop(), False)
        if targetip is None:
            self.reflect(ip)
        else:
            ip.push(targetip.stack[TOSS][-1])

    @Fingerprint.register('P')
    def push(self, ip):
        targetip = self.search_ip(ip.program, ip.pop(), True)
        if targetip is None:
            self.reflect(ip)
        else:
            targetip.push(ip.pop())

