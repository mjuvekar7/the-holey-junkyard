from funge.fingerprint import Fingerprint

class IMAP(Fingerprint):
    'Instruction remap extension'

    API = 'PyFunge v2'
    ID = 0x494D4150

    # Implementation strategy:
    # 1. IP has a mapping of commands (IMAP_mapping).
    # 2. When "M" remaps the command, it finds original command from the mapping
    #    (no chained remapping) and call IP.add_command for new semantics.
    #    If the mapping contains previously remapped one, it pops previous
    #    semantics off and pushes it.
    # 3. "(" and ")" are overridden, so it takes care of command mapping.
    #    Before the execution it takes out all the remapped commands (only the
    #    mapping remains), and after the execution it rewires the commands.
    #
    # Notes:
    # - It won't affect other unmapped commands, as they depends on underlying
    #   semantics and not remapped (i.e. IP.commands) commands. "Acts like"
    #   doesn't necessarily mean it should obey remapped semantics.
    # - It would conflict with other command-remapping fingerprints.

    def init(self, ip):
        Fingerprint.init(self, ip)
        if not hasattr(ip, 'IMAP_mapping'):
            ip.IMAP_mapping = {}

    @Fingerprint.register('C')
    def clear(self, ip):
        for cmd in ip.IMAP_mapping:
            ip.remove_command(cmd)
        ip.IMAP_mapping.clear()

    @Fingerprint.register('M')
    def remap(self, ip):
        oldcmd = ip.pop()
        newcmd = ip.pop()

        if newcmd in ip.IMAP_mapping:
            callback = ip.prevcommands[newcmd][-1]
        else:
            callback = ip.commands[newcmd]

        if oldcmd in ip.IMAP_mapping:
            ip.remove_command(oldcmd)
        ip.add_command(oldcmd, callback)
        ip.IMAP_mapping[oldcmd] = newcmd

    @Fingerprint.register('O')
    def reset(self, ip):
        cmd = ip.pop()
        if cmd in ip.IMAP_mapping:
            ip.remove_command(cmd)
            del ip.IMAP_mapping[cmd]

    @Fingerprint.register('(')
    def load_semantics(self, ip):
        for cmd in ip.IMAP_mapping:
            ip.remove_command(cmd)
        self.semantics.load_semantics(ip)
        newcommands = ip.commands.copy()
        for oldcmd, newcmd in ip.IMAP_mapping.items():
            ip.add_command(oldcmd, newcommands[newcmd])

    @Fingerprint.register(')')
    def unload_semantics(self, ip):
        for cmd in ip.IMAP_mapping:
            ip.remove_command(cmd)
        self.semantics.unload_semantics(ip)
        newcommands = ip.commands.copy()
        for oldcmd, newcmd in ip.IMAP_mapping.items():
            ip.add_command(oldcmd, newcommands[newcmd])

