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

import text2num.text2num as text2num

be = [
    'be',
    'was',
    'were',
    'am',
    'are',
    'is',
    'will be',
]

have = [
    'have',
    'had',
    'have',
    'will have',
]

verbs = [be, have]
verbdict = {
    'be' : 'BE',
    'have' : 'HAVE',
}

def prepare(problem):
    problem = problem.lower()
    problem = problem.replace('. ', '.\n').replace('? ', '?\n')

    statements, queries = [], []
    for line in problem.splitlines(True):
        if line.endswith('?\n'):
            queries.append(line)
        else:
            statements.append(line)

    problem = ''
    for statement in statements:
        problem += statement
    for query in queries:
        problem += query

    words = problem.split()
    for i in range(0, len(words)):
        for verb in verbs:
            if words[i] in verb:
                words[i] = verb[0]
        
        try:
            words[i] = str(text2num.text2num(words[i].rstrip('.?')))
        except text2num.NumberException:
            pass
        
        if words[i] in ['a', 'an', 'the']:
            words[i] = ''
    
    problem = ''
    for word in words:
        problem += word
        if word.endswith(('.', '?')):
            problem += '\n'
        else:
            problem += ' '

    return problem
