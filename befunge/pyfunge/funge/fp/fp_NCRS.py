from funge.fingerprint import Fingerprint

import sys
try:
    import curses
except ImportError:
    curses = None

class NCRS(Fingerprint):
    'Ncurses extension'

    API = 'PyFunge v2'
    ID = 0x4e435253

    def init(self, ip):
        if not sys.stdout.isatty():
            self.platform.warn('Standard output is not a TTY, NCRS won\'t work correctly')
        Fingerprint.init(self, ip)
        ip.NCRS_window = None

    def final(self, ip):
        if ip.NCRS_window is not None:
            curses.endwin()
        del ip.NCRS_window

    @Fingerprint.register('B')
    def beep(self, ip):
        if curses.beep() == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('C')
    def clear(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        mode = ip.pop()
        if mode == 0:
            result = window.erase()
        elif mode == 1:
            result = window.clrtoeol()
        elif mode == 2:
            result = window.clrtobot()
        else:
            result = curses.ERR

        if result == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('E')
    def toggle_echo(self, ip):
        if ip.pop():
            result = curses.echo()
        else:
            result = curses.noecho()

        if result == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('G')
    def get(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        ip.push(window.getch())

    @Fingerprint.register('I')
    def init_fini(self, ip):
        if ip.pop():
            try:
                ip.NCRS_window = curses.initscr()
            except Exception:
                self.reflect(ip)
        else:
            if curses.endwin() == curses.ERR:
                self.reflect(ip)
            else:
                ip.NCRS_window = None

    @Fingerprint.register('K')
    def toggle_keypad(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        flag = (ip.pop() != 0)
        if window.keypad(flag) == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('M')
    def gotoxy(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        r, c = ip.popmany(2)
        if window.move(r, c) == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('N')
    def toggle_input(self, ip):
        if ip.pop():
            result = curses.nocbreak()
        else:
            result = curses.cbreak()

        if result == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('P')
    def put(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        ch = ip.pop()
        if window.addch(ch) == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('R')
    def refresh(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        if window.refresh() == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('S')
    def write(self, ip):
        window = ip.NCRS_window
        if window is None:
            self.reflect(ip)
            return

        s = ip.pop_string()
        if window.addstr(s) == curses.ERR:
            self.reflect(ip)

    @Fingerprint.register('U')
    def unget(self, ip):
        if curses.ungetch(ip.pop()) == curses.ERR:
            self.reflect(ip)

