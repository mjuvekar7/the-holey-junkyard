from funge.fingerprint import Fingerprint

import datetime

class DATE(Fingerprint):
    'Date Functions'

    API = 'PyFunge v2'
    ID = 0x44415445

    def to_ordinal(self, y, m, d):
        if y == 0:
            raise ValueError('Year 0 doesn\'t exist in Gregorian calendar')
        if y < 0:
            y += 1 # e.g. 1 BCE = year 0, 2 BCE = year -1, and so on

        # uses the fact that Gregorian calendar repeats in 400-year cycle
        cycle = (y - 1) // 400
        y = (y - 1) % 400 + 1
        ord = datetime.date(y, m, d).toordinal() - 1 # so 0001-01-01 == ord 0
        return cycle * 146097 + ord

    def from_ordinal(self, ord):
        cycle = ord // 146097
        ord %= 146097
        date = datetime.date.fromordinal(ord + 1)
        if cycle < 0:
            return date.year + cycle * 400 - 1, date.month, date.day
        else:
            return date.year + cycle * 400, date.month, date.day

    @Fingerprint.register('A')
    def add_days(self, ip):
        days, d, m, y = ip.popmany(4)
        try:
            y, m, d = self.from_ordinal(self.to_ordinal(y, m, d) + days)
            ip.push(y)
            ip.push(m)
            ip.push(d)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('C')
    def from_julian_day(self, ip):
        jd = ip.pop()
        y, m, d = self.from_ordinal(jd - 1721426)
        ip.push(y)
        ip.push(m)
        ip.push(d)

    @Fingerprint.register('D')
    def difference(self, ip):
        d2, m2, y2, d1, m1, y1 = ip.popmany(6)
        try:
            ip.push(self.to_ordinal(y1, m1, d1) - self.to_ordinal(y2, m2, d2))
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('J')
    def to_julian_day(self, ip):
        d, m, y = ip.popmany(3)
        try:
            ip.push(self.to_ordinal(y, m, d) + 1721426)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('T')
    def from_doy(self, ip):
        days, y = ip.popmany(2)
        newy, m, d = self.from_ordinal(self.to_ordinal(y, 1, 1) + days)
        if y != newy:
            self.reflect(ip)
        else:
            ip.push(y)
            ip.push(m)
            ip.push(d)

    @Fingerprint.register('W')
    def to_dow(self, ip):
        d, m, y = ip.popmany(3)
        try:
            ip.push(self.to_ordinal(y, m, d) % 7)
        except Exception:
            self.reflect(ip)

    @Fingerprint.register('Y')
    def to_doy(self, ip):
        d, m, y = ip.popmany(3)
        try:
            ip.push(self.to_ordinal(y, m, d) - self.to_ordinal(y, 1, 1))
        except Exception:
            self.reflect(ip)

