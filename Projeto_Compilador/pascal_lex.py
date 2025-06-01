import ply.lex as lex

literals = [';', ',', ':', '(', ')', '=', '*', '+', '-', '.', '<', '>', '[', ']']
tokens = ['stringARG', 'num', 'identifier', 'PROGRAM', 'BEGIN', 'END', 'VAR', 'TYPE', 
          'FOR', 'TO', 'DOWNTO', 'DO', 'WHILE', 'WRITELN', 'READLN', 'IF', 'THEN', 'ELSE', 
          'TRUE', 'FALSE', 'NOT', 'AND', 'OR', 'DIV', 'MOD', 'ARRAY', 'OF', 'DOUBLEDOT', 'LENGTH']

def t_PROGRAM(t):
    r'\b[pP][rR][oO][gG][rR][aA][mM]\b'
    t.value = t.value.lower()
    return(t)

def t_BEGIN(t):
    r'\b[bB][eE][gG][iI][nN]\b'
    t.value = t.value.lower()
    return(t)

def t_END(t):
    r'\b[eE][nN][dD]\b'
    t.value = t.value.lower()
    return(t)

def t_VAR(t):
    r'\b[vV][aA][rR]\b'
    t.value = t.value.lower()
    return(t)

def t_TYPE(t):
    r'\b[iI][nN][tT][eE][gG][eE][rR]\b|\b[bB][oO][oO][lL][e][aA][nN]\b|\b[sS][tT][rR][iI][nN][gG]\b|\b[dD][oO][uU][bB][lL][eE]\b'
    t.value = t.value.lower()
    return(t)
  
def t_FOR(t):
    r'\b[fF][oO][rR]\b'
    t.value = t.value.lower()
    return(t)

def t_TO(t):
    r'\b[tT][oO]\b'
    t.value = t.value.lower()
    return(t)

def t_DOWNTO(t):
    r'\b[dD][oO][wW][nN][tT][oO]\b'
    t.value = t.value.lower()
    return(t)

def t_DO(t):
    r'\b[dD][oO]\b'
    t.value = t.value.lower()
    return(t)

def t_WHILE(t):
    r'\b[wW][hH][iI][lL][eE]\b'
    t.value = t.value.lower()
    return(t)

def t_WRITELN(t):
    r'\b[wW][rR][iI][tT][eE][lL][nN]\b|[wW][rR][iI][tT][eE]\b'
    t.value = t.value.lower()
    return(t)

def t_READLN(t):
    r'\b[rR][eE][aA][dD][lL][nN]\b|\b[rR][eE][aA][dD]\b'
    t.value = t.value.lower()
    return(t)

def t_IF(t):
    r'\b[iI][fF]\b'
    t.value = t.value.lower()
    return(t)

def t_THEN(t):
    r'\b[tT][hH][eE][nN]\b'
    t.value = t.value.lower()
    return(t)

def t_ELSE(t):
    r'\b[eE][lL][sS][eE]\b'
    t.value = t.value.lower()
    return(t)

def t_TRUE(t):
    r'\b[tT][rR][uU][eE]\b'
    t.value = t.value.lower()
    return(t)

def t_FALSE(t):
    r'\b[fF][aA][lL][sS][eE]\b'
    t.value = t.value.lower()
    return(t)

def t_NOT(t):
    r'\b[nN][oO][tT]\b'
    t.value = t.value.lower()
    return(t)

def t_AND(t):
    r'\b[aA][nN][dD]\b'
    t.value = t.value.lower()
    return(t)

def t_OR(t):
    r'\b[oO][rR]\b'
    t.value = t.value.lower()
    return(t)

def t_DIV(t):
    r'\b[dD][iI][vV]\b'
    t.value = t.value.lower()
    return(t)

def t_MOD(t):
    r'\b[mM][oO][dD]\b'
    t.value = t.value.lower()
    return(t)

def t_ARRAY(t):
    r'\b[aA][rR][rR][aA][yY]\b'
    t.value = t.value.lower()
    return(t)

def t_OF(t):
    r'\b[oO][fF]\b'
    t.value = t.value.lower()
    return(t)

def t_LENGTH(t):
    r'\b[lL][eE][nN][gG][tT][hH]\b'
    t.value = t.value.lower()
    return(t)

def t_DOUBLEDOT(t):
    r'\.\.'
    return(t)

def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return(t)

def t_num(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_stringARG(t):
    r'\'(\\.|[^\'\\])*\''
    t.value = t.value[1:-1]
    return t

def t_comment(t):
    r'\{[^}]*\}'
    pass

t_ignore = " \t\n"

def t_error(t):
    print('Caráter ilegal: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

