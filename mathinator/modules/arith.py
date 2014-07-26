import id_dict

_keywords = {
    'sum' : 'ADD',
    'total' : 'ADD',
    'plus' : 'ADD',
    'difference' : 'SUB',
    'subtract' : 'SUB',
    'minus' : 'SUB',
    'number' : 'NUMB',
}

def p_arith_statement(p):
    '''statement : THERE BE NUM ID "\n"'''
    id_dict.update([(p[4], Attribute('number', p[3]))])

def p_arith_statement_poss(p):
    '''statement : ID HAVE NUM ID "\n"'''
    id_dict.update([(p[1], Attribute(p[4], p[3]))])

def p_arith_query(p):
    '''query : WHAT BE ADD "" NUMB OF ID "\n" ID "\n"
             | WHAT BE ADD OF NUMB OF ID "\n" ID "\n"'''
    p[0] = id_dict[p[7]].value + id_dict[p[9]].value
