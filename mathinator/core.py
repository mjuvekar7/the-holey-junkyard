import ply.lex as lex
import ply.yacc as yac

import modules
import importlib

module_names = ['arith']
modules = []
for module in module_names:
    modules.append(importlib.import_module(module, package='modules'))

# define tokens
assignments = {
    'is':'IS'
}

queries = {
    'what':'WHAT'
}

common = {
    'of':'OF',
    'and':'AND'
}

tokens = [
    'WORD',
    'NUMBER'
]

t_ignore = r'\s[.?!]'

def t_WORD(t):
    r'\b\w+\b'
    types = dict(assignments.items() + queries.items() + common.items())
    t.type = types.get(t.value, 'WORD')
    return t

def t_NUMBER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_error(t):
    print('Illegal character' + t.value)

def p_statements(p):
    'statements : statements statement'
    '           | empty statement'
    p[0] = p[1] + [p[2]]

def p_empty(p):
    'empty : '
    pass

def generate():
    tokens.append(list(assignments.values()))
    tokens.append(list(queries.values()))
    tokens.append(list(common.values()))
    for module in modules:
        tokens.append(list(module.keywords.values()))
    tokens = list(set(tokens))
    lex.lex()
    yacc.yacc()

if __name__ == '__main__':
    generate()
    yacc.parse('the number of apples is 2')
    print(arith.subjects)
