# Copyright (C) 2014 Shardul C. and Mandar J.
# 
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

# all keywords of all modules
keywords = []

# of the form id (string) : Attribute
ids = {}

# Attribute can contain *anything*, from a single number value to arrays of
# items possessed by IDs to height/weight of IDs, etc.
class Attribute:
    def __init__(self, name='', value=0):
        self.name = name
        self.value = value
