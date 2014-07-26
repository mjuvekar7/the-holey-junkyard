import re
from sys import modules as mods
import ply.ply.lex as lex
import ply.ply.yacc as yacc

import preparer

##
# modules
##

module_keywords = {}
import modules
from modules import *
for mod in modules.__all__:
    __import__('modules.' + mod)
    module = mods['modules.' + mod]
    module_keywords[module] = getattr(module, '_keywords')
    from module import *

##
# tokenizer
##

queries = {
    'what' : 'WHAT',
    'how many' : 'HOWMANY',
}

tokens = [
    'ID',
    'NUM',
    'OF',
    'THERE'
] + list(queries.values()) + [verb[0].upper() for verb in preparer.verbs]
for key_dict in module_keywords:
    tokens += list(keydict.values())

t_ID = r'(\w* )*[a-z]+'
t_OF = r'\bof\b'
t_THERE = r'\bthere\b'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

##
# parser
##

def p_question(p):
    '''question : statements "\n" queries'''
    # we want only the answers!
    p[0] = p[2]

def p_statements(p):
    '''statements : statements
                  | statement'''

def p_queries(p):
    '''queries : queries
               | query'''
    p[0] = p[1]

if __name__ == '__main__':
    f = open('infile', 'r')
    problem = f.read()
    preparer.prepare(problem)

    reflags = re.ASCII | re.IGNORECASE
    lex.lex(flags=reflags)
    yacc.yacc()
    print(yacc.parse(problem))
