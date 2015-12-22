from funge.fingerprint import Fingerprint

import sys
try:
    import curses
except ImportError:
    curses = None

class TERM(Fingerprint):
    'Terminal extension'

    API = 'PyFunge v2'
    ID = 0x5445524d

    def init(self, ip):
        if not sys.stdout.isatty():
            self.platform.warn('Standard output is not a TTY, TERM won\'t work correctly')
        curses.setupterm() # could raise exceptions

        self.t_clear = curses.tigetstr('clear')
        self.t_cud = curses.tigetstr('cud')
        self.t_cuu = curses.tigetstr('cuu')
        self.t_home = curses.tigetstr('home')
        self.t_el = curses.tigetstr('el')
        self.t_ed = curses.tigetstr('ed')
        self.t_cup = curses.tigetstr('cup')

        Fingerprint.init(self, ip)

    @Fingerprint.register('C')
    def clear_screen(self, ip):
        self.platform.putstr(self.t_clear)

    @Fingerprint.register('D')
    def move_down(self, ip):
        n = ip.pop()
        if n > 0:
            self.platform.putstr(curses.tparm(self.t_cud, n))
        elif n < 0:
            self.platform.putstr(curses.tparm(self.t_cuu, -n))

    @Fingerprint.register('G')
    def gotoxy(self, ip):
        r, c = ip.popmany(2)
        self.platform.putstr(curses.tparm(self.t_cup, r, c))

    @Fingerprint.register('H')
    def goto_home(self, ip):
        self.platform.putstr(self.t_home)

    @Fingerprint.register('L')
    def goto_eol(self, ip):
        self.platform.putstr(self.t_el)

    @Fingerprint.register('S')
    def goto_eos(self, ip):
        self.platform.putstr(self.t_ed)

    @Fingerprint.register('U')
    def move_up(self, ip):
        n = ip.pop()
        if n > 0:
            self.platform.putstr(curses.tparm(self.t_cuu, n))
        elif n < 0:
            self.platform.putstr(curses.tparm(self.t_cud, -n))

