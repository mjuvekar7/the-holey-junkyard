"""Fingerprint base class and importer."""

from funge.semantics import SemanticsOverlay

class FingerprintLookup(object):
    def __init__(self):
        self.fprints = {}

    def __contains__(self, fprint):
        return fprint in self.fprints

    def __getitem__(self, fprint):
        return self.fprints[fprint]

    def module_from_name(self, name): 
        obj = __import__(name)
        for part in name.split('.')[1:]:
            obj = getattr(obj, part)
        return obj

    def search_module(self, mod):
        objects = []
        for name in dir(mod):
            if name.startswith('_'): continue
            obj = getattr(mod, name)
            if obj is Fingerprint: continue
            if issubclass(type(obj), type) and issubclass(obj, Fingerprint):
                objects.append(obj)
        return objects

    def add_module(self, name):
        mod = self.module_from_name(name)
        for obj in self.search_module(mod):
            self.add_class(obj)

    def add_class(self, cls):
        if not issubclass(cls, Fingerprint): return
        if not hasattr(cls, 'API') or cls.API != 'PyFunge v2': return

        if cls.ID == 0: raise ValueError
        self.fprints[cls.ID] = cls

class Fingerprint(SemanticsOverlay):
    def init(self, ip):
        ip.add_commands(self)

    def final(self, ip):
        ip.remove_commands(self)

