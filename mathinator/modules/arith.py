__all__ = ['p_arith_statement', 'p_arith_subject', 'p_arith_query', 'p_arith_query_add']

subjects = {}
keywords = {
    'sum':'SUM'
}

def p_arith_statement(p):
    'statement : subject IS NUMBER'
    subjects[str(p[1])] = p[3]

def p_arith_subject(p):
    'subject : subject WORD'
    '        | empty WORD'
    p[0] = p[1] + [p[2]]

def p_arith_query(p):
    'statement : WHAT IS subject'
    p[0] = subjects.get(p[3])

def p_arith_query_add(p):
    'statement : WHAT IS SUM OF subject AND subject'
    p[0] = subjects.get(p[5]) + subjects.get(p[7])

