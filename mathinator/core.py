#!/usr/bin/python3

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

import sys

import ply.lex as lex
import ply.yacc as yacc

import preparer
from modules import *
from globdict import ids, keywords as modkeywords


# tokenizer

queries = {
    'what' : 'WHAT',
    'how many' : 'HOWMANY',
}

reserved = {
    'of' : 'OF',
    'there' : 'THERE',
    'and' : 'AND',
    'but' : 'BUT',
    'between' : 'BET',
}

# make an all-encompassing dictionary of tokens
alldict = {}
alldict.update(queries)
alldict.update(preparer.verbdict)
alldict.update(reserved)
# this bit includes individual module keywords
for moddict in modkeywords:
    alldict.update(moddict)

tokens = [
    'ID',
    'NUM',
    'NL',
] + list(alldict.values())

# ignore punctuation
t_ignore = r' .?'

def t_NL(t):
    r'\n'
    # keep track of lines
    t.lexer.lineno += 1
    return t

def t_ID(t):
    r'[a-z]+'
    t.type = alldict.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def find_column(string, token):
    last_cr = string.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return 'line=' + token.lexer.lineno + ' column=' + column

def t_error(t):
    print('Illegal character "%s" at %s'.format(t.value[0],
                                                find_column(t.value[0], t)))
    t.lexer.skip(1)


# parser

start = 'question'

def p_question(p):
    """question : statements queries"""
    # we want only the answers!
    p[0] = p[2]

def p_statements(p):
    """statements : statement NL statements
                  | statement NL"""

def p_queries(p):
    """queries : query NL queries
               | query NL"""
    try:
        p[0] = str(p[1]) + '\n' + str(p[3])
    except IndexError:
        p[0] = str(p[1])


def p_conj_statement(p):
    """statements : statement AND statement
                 | statement BUT statement"""

def p_conj_query(p):
       """queries : query AND query"""
       p[0] = str(p[1]) + '\n' + str(p[3])

def p_empty(p):
    """empty :"""
    pass

if __name__ == '__main__':
    print('mathinator  Copyright (C) 2014 Shardul C. and Mandar J.\n'
        'This program comes with ABSOLUTELY NO WARRANTY. This is free software, '
        'and you are welcome to redistribute it under certain conditions.\n'
        'For details, please see the COPYING file provided with this program.')
    
    try:
        f = open(sys.argv[1], 'r')
    except NameError:
        print(sys.argv[1] + ': no such file')
        sys.exit(1)
    except IndexError:
        print('Usage is <executable> <input file>')
        sys.exit(2)
    problem = f.read()
    problem = preparer.prepare(problem)
    print(problem)

    lex.lex()
    yacc.yacc()
    print(yacc.parse(problem))
