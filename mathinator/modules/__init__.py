# This file is part of mathinator.
# 
# mathinator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# mathinator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with mathinator.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2014 Shardul C. and Mandar J.

import os
import globdict

__all__ = []
modglobals, modlocals = globals(), locals()

# dynamically import all the package modules
for filename in os.listdir(__name__):
    # process all python files in directory that don't start with underscore
    # (which also keeps this module from importing itself)
    if (not filename.startswith('_')) and filename.split('.')[-1] == 'py':
        modulename = filename.split('.')[0]  # filename without extension
        package_module = '.'.join([__name__, modulename])
        module = __import__(package_module, modglobals, modlocals, [modulename])
        for name in module.__dict__:
            if not name.startswith('_'):
                modglobals[name] = module.__dict__[name]
                if name == 'keywords':
                    globdict.keywords.append(module.__dict__['keywords'])
                __all__.append(name)
