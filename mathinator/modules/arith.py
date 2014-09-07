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

from globdict import ids, Attribute

keywords = {
    'sum' : 'SUM',
    'total' : 'TOTL',
    'plus' : 'PLUS',
    'difference' : 'DIFF',
    'minus' : 'MIN',
    'number' : 'NUMB',
}

def p_arith_statement(p):
    '''statement : THERE BE NUM ID'''
    ids.update([(p[4], Attribute('number', p[3]))])

#def p_arith_statement_poss(p):
#    '''statement : ID HAVE NUM ID'''
#    ids.update([(p[1], Attribute(p[4], p[3]))])

def p_arith_query_total(p):
    '''query : WHAT BE TOTL NUMB OF ID AND ID'''
    total = str(ids[p[6]].value + ids[p[8]].value)
    p[0] = 'The total number of ' + p[6] + ' and ' + p[8] + ' is '  + total

def p_arith_query_difference(p):
    '''query : WHAT BE DIFF BET NUMB OF ID AND ID'''
    diff = str(abs(ids[p[7]].value - ids[p[9]].value))
    p[0] = 'The difference between the number of ' + p[7] + ' and ' + p[9] + ' is ' + diff

#def p_arith_query(p):
#    '''query : WHAT BE ADD empty NUMB OF ID AND ID
#             | WHAT BE ADD OF NUMB OF ID AND ID'''
#    p[0] = ids[p[7]].value + ids[p[9]].value
