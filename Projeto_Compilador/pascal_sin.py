import ply.yacc as yacc
from pascal_lex import tokens, literals
from utils import compile_operand, is_single_char_string
        
def p_program(p):
    """
    PascalProgram : PROGRAM identifier ';' VarSection CodeBlock
    """
    p[0] = p[4] + p[5]
    print(f"\nPascal Program Traduzido:\n{p[0]}\n")

def p_varSection(p):
    """
    VarSection : VAR VarStatements
    """
    print("Indexes", p.parser.indexes)
    p[0] = p[2]

def p_varSection_empty(p):
    """
    VarSection :
    """
    p[0] = ''

def p_varStatements_mutiple(p):
    """
    VarStatements : VarStatements VarSingleStatement
    """
    p[0] = p[1] + p[2]

def p_varStatements_single(p):
    """
    VarStatements : VarSingleStatement
    """
    p[0] = p[1]

def p_varSingleStatement(p):
    """
    VarSingleStatement : VarStatementIdentifiers ':' VarType ';'
    """
    p[0] = ''
    
    for i, identifier in enumerate(p[1]):
        if isinstance(p[3], dict) and p[3].get('kind') == 'array':
            print(f"Var Captured -> {identifier}: {p[3].get('kind')}({p[3].get('element_type')})")
            
            arr_info = p[3]
            p.parser.types[identifier] = f"array({arr_info['element_type']})"
            p.parser.indexes[identifier] = p.parser.index
            p.parser.arrays[identifier] = {
                'length': arr_info['length'],
                'lower_bound': arr_info['lower_bound'],
                'element_type': arr_info['element_type']
            }

            for idx in range(arr_info['length']):
                if arr_info['element_type'] in ('integer', 'boolean'):
                    p[0] += 'pushi 0'
                elif arr_info['element_type'] == 'double':
                    p[0] += 'pushf 0.0'
                elif arr_info['element_type'] == 'string':
                    p[0] += 'pushs ""'
                else:
                    print(f"Unknown array element type: {arr_info['element_type']}")

                if idx != arr_info['length'] - 1:
                    p[0] += '\n'

                p.parser.index += 1

        else:
            print(f"Var Captured -> {identifier}: {p[3]}")

            p.parser.indexes[identifier] = p.parser.index
            p.parser.index += 1
            
            if p[3] == 'integer':
                p.parser.types[identifier] = 'integer'
                p[0] = p[0] + 'pushi 0'
            elif p[3] == 'double':
                p.parser.types[identifier] = 'double'
                p[0] = p[0] + 'pushf 0.0'
            elif p[3] == 'boolean':
                p.parser.types[identifier] = 'boolean'
                p[0] = p[0] + 'pushi 0'
            elif p[3] == 'string':
                p.parser.types[identifier] = 'string'
                p[0] = p[0] + 'pushs \"\"'
            else:
                print(f"Unknown type: {p[3]} for {identifier}")
        
        p[0] = p[0] + '\n'

def p_varType_simple(p):
    """
    VarType : TYPE
    """
    p[0] = p[1]

def p_varType_array(p):
    """
    VarType : ARRAY '[' num DOUBLEDOT num ']' OF TYPE
    """
    lower_bound = int(p[3])
    upper_bound = int(p[5])
    element_type = p[8]
    array_length = upper_bound - lower_bound + 1

    p[0] = {
        'kind': 'array',
        'element_type': element_type,
        'length': array_length,
        'lower_bound': lower_bound
    }
    
def p_varStatementIdentifiers_multiple(p):
    """
    VarStatementIdentifiers : VarStatementIdentifiers ',' identifier
    """
    p[0] = p[1] + [p[3]]

def p_varStatementIdentifiers_single(p):
    """
    VarStatementIdentifiers : identifier
    """
    p[0] = [p[1]]

def p_codeBlock(p):
    """
    CodeBlock : BEGIN CodeLines END '.'
    """
    p[0] = f"start\n{p[2]}\nstop"

def p_codeLines(p):
    """
    CodeLines : CodeLinesWithSemiColon StatementWithSemicolon
              | CodeLinesWithSemiColon StatementWithOptionalSemicolon
              | StatementWithOptionalSemicolon
    """
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    else:
        p[0] = p[1]

def p_codeLines_semicolon_multiple(p):
    """
    CodeLinesWithSemiColon : CodeLinesWithSemiColon StatementWithSemicolon
    """
    p[0] = p[1] + '\n' + p[2]

def p_codeLines_semicolon_single(p):
    """
    CodeLinesWithSemiColon : StatementWithSemicolon
    """
    p[0] = p[1]

def p_statement_with_semicolon(p):
    """
    StatementWithSemicolon : Statement ';'
    """
    p[0] = p[1]

def p_statement_with_optional_semicolon(p):
    """
    StatementWithOptionalSemicolon : Statement ';'
                                   | Statement
    """
    p[0] = p[1]

def p_statement_write(p):
    """
    Statement : WRITELN '(' Arguments ')'
    """
    p[0] = ''
    for i, argWrite in enumerate(p[3]):
        p[0] = p[0] + argWrite
    if i >= len(p[3]) - 1:
        if p[1] == 'writeln':
            p[0] = p[0] + 'writeln'

def p_arguments_multiple(p):
    """
    Arguments : Arguments ',' Arg
    """
    p[0] = p[1] + [p[3]]

def p_arguments_single(p):
    """
    Arguments : Arg
    """
    p[0] = [p[1]]

def p_arg(p):
    """
    Arg : Value
    """
    
    if p.parser.nextWrite == "number":
        p[0] = p[1]  + "writef\n"
    elif p.parser.nextWrite == "integer": 
        p[0] = p[1]  + "writei\n"
    elif p.parser.nextWrite == "double":
        p[0] = p[1]  + "writef\n"
    elif p.parser.nextWrite == "boolean":
        p[0] = p[1]  + "writei\n"
    elif p.parser.nextWrite == "string": 
        p[0] = p[1] + "writes\n"
    else: p[0] = ""

def p_statement_read(p):
    """
    Statement : READLN '(' identifier ')'
    """
    if (p.parser.types[p[3]] == 'integer'):
        p[0] = f'read\natoi\nstoreg {p.parser.indexes[p[3]]}'
    elif (p.parser.types[p[3]] == 'string'):
        p[0] = f'read\nstoreg {p.parser.indexes[p[3]]}'
    elif (p.parser.types[p[3]] == 'double'):
        p[0] = f'read\natof\nstoreg {p.parser.indexes[p[3]]}'

def p_statement_read_arraySpecial(p):
    """
    Statement : READLN '(' identifier '[' Fator ']' ')'
    """
    arr_info = p.parser.arrays[p[3]]
    base_index = p.parser.indexes[p[3]]
    lower_bound = arr_info['lower_bound']
    
    # Stack global pointer
    code = "pushgp\n"

    # Index
    code += p[5]

    # Adjust index
    if lower_bound != 0:
        code += f"pushi {lower_bound-base_index}\nsub\n"

    # Value to store in given index
    if (arr_info['element_type'] == 'integer'):
        code += f'read\natoi\nstoren'
    elif (arr_info['element_type'] == 'string'):
        code += f'read\nstoren'
    elif (arr_info['element_type'] == 'double'):
        code += f'read\natof\nstoren'

    p[0] = code

def p_statement_define(p):
    """
    Statement : identifier ':' '=' Value
    """
    p[0] = p[4] + f"storeg {p.parser.indexes[p[1]]}"

def p_statement_define_boolean(p):
    """
    Statement : identifier ':' '=' Condition
    """
    if p.parser.types[p[1]] == 'boolean':
        p[0] = p[4] + f"storeg {p.parser.indexes[p[1]]}"
    else: 
        raise Exception(f"Semantic Error: Cannot ASSIGN boolean value to '{p[1]}'")
    
def p_statement_define_identifier(p):
    """
    Statement : identifier ':' '=' identifier
    """
    if (p.parser.types[p[1]] == p.parser.types[p[4]]) or (p.parser.types[p[1]] == 'integer' and p.parser.types[p[4]] == 'double') or (p.parser.types[p[1]] == 'double' and p.parser.types[p[4]] == 'integer'):
        p[0] = f"pushg {p.parser.indexes[p[4]]}\n" + f"storeg {p.parser.indexes[p[1]]}"
    else: 
        raise Exception(f"Semantic Error: Cannot ASSIGN '{p[4]}' value to '{p[1]}'")
    
def p_statement_define_num(p):
    """
    Statement : identifier ':' '=' num
    """
    if p.parser.types[p[1]] == 'integer':
        p[0] = f"pushi {p[4]}\n" + f"storeg {p.parser.indexes[p[1]]}"
    elif p.parser.types[p[1]] == 'double':
        p[0] = f"pushf {p[4]}\n" + f"storeg {p.parser.indexes[p[1]]}"
    else: 
        raise Exception(f"Semantic Error: Cannot ASSIGN numeric value to '{p[1]}'")

def p_statement_define_string(p):
    """
    Statement : identifier ':' '=' stringARG
    """
    if p.parser.types[p[1]] == 'string':
        p[0] = f"pushs \"{p[4]}\"\n" + f"storeg {p.parser.indexes[p[1]]}"
    else: 
        raise Exception(f"Semantic Error: Cannot ASSIGN string value to '{p[1]}'")

def p_statement_define_arraySpecial(p):
    """
    Statement : identifier '[' Fator ']' ':' '=' Value
    """
    arr_info = p.parser.arrays[p[1]]
    base_index = p.parser.indexes[p[1]]
    lower_bound = arr_info['lower_bound']
    
    # Stack global pointer
    code = "pushgp\n"

    # Index
    code += p[3]

    # Adjust index
    if lower_bound != 0:
        code += f"pushi {lower_bound-base_index}\nsub\n"

    # Value to store in given index
    code += p[7]+"storen"

    p[0] = code

def p_statement_forLoop(p):
    """
    Statement : ForLoop
    """
    p[0] = p[1]

def p_statement_while(p):
    """
    Statement : WHILE Condition DO LoopContent
    """
    loop_id = p.parser.loopsCount
    p[0] = (
        f"whileLoopStart{loop_id}:\n" +
        p[2] +  # Condition
        f"jz whileLoopEnd{loop_id}\n" +
        p[4] +  # LoopContent
        f"\njump whileLoopStart{loop_id}\n" +
        f"whileLoopEnd{loop_id}:\n"
    )
    p.parser.loopsCount += 1

def p_statement_if_then_else(p):
    """
    Statement : IF Condition THEN LoopContent ElseChain
    """
    if_id = p.parser.ifCount
    else_id = p.parser.elseCount

    p[0] = (
        p[2] +
        f"jz skipIf{if_id}\n" +
        p[4] + "\n" +
        f"jump skipElse{else_id}\n" +
        f"skipIf{if_id}:\n" +
        p[5] +
        f"skipElse{else_id}:\n"
    )

    p.parser.ifCount += 1
    p.parser.elseCount += 1

def p_condition_parentheses(p):
    """
    Condition : '(' Condition ')'
    """
    p[0] = p[2]

def p_condition_and(p):
    """
    Condition : Condition AND Condition
    """
    p[0] = p[1] + p[3] + "and\n"

def p_condition_or(p):
    """
    Condition : Condition OR Condition
    """
    p[0] = p[1] + p[3] + "or\n"

def p_condition_true(p):
    """
    Condition : TRUE
    """
    p[0] = "pushi 1\n"

def p_condition_false(p):
    """
    Condition : FALSE
    """
    p[0] = "pushi 0\n"

def p_condition_not(p):
    """
    Condition : NOT Condition
    """
    p[0] = p[2] + "not\n"

def p_condition_identifier(p):
    """
    Condition : identifier
    """
    p[0] = f"pushg {p.parser.indexes[p[1]]}\n"

def p_condition_equal(p):
    """
    Condition : Value '=' Value
    """

    left_code = p[1]
    right_code = p[3]

    result = ""

    if is_single_char_string(left_code):
        result += left_code + "pushi 0\ncharat\n"
    else:
        result += left_code

    if is_single_char_string(right_code):
        result += right_code + "pushi 0\ncharat\n"
    else:
        result += right_code

    result += "equal\n"
    p[0] = result

def p_condition_notequal(p):
    """
    Condition : Value '<' '>' Value
    """
    p[0] = p[1] + p[4] + "equal\nnot\n"

def p_condition_infeq(p):
    """
    Condition : Value '<' '=' Value
    """
    p[0] = p[1] + p[4] + "infeq\n"

def p_condition_supeq(p):
    """
    Condition : Value '>' '=' Value
    """
    p[0] = p[1] + p[4] + "supeq\n"

def p_condition_inf(p):
    """
    Condition : Value '<' Value
    """
    p[0] = p[1] + p[3] + "inf\n"

def p_condition_sup(p):
    """
    Condition : Value '>' Value
    """
    p[0] = p[1] + p[3] + "sup\n"

def p_elsechain_full(p):
    """
    ElseChain : ElseifSectionList ElseSection
    """
    p[0] = p[1] + p[2]

def p_elsechain_elseonly(p):
    """
    ElseChain : ElseSection
    """
    p[0] = p[1]

def p_elseifSectionList(p):
    """
    ElseifSectionList : ElseifSectionList ElseifSection
    """
    p[0] = p[1] + p[2]

def p_elseifSectionList_single(p):
    """
    ElseifSectionList : ElseifSection
    """
    p[0] = p[1]

def p_elseifSection(p):
    """
    ElseifSection : ELSE IF Condition THEN LoopContent
    """
    if_id = p.parser.ifCount
    else_id = p.parser.elseCount

    p[0] = (
        p[3] +
        f"jz skipIf{if_id}\n" +
        p[5] + "\n" +
        f"jump skipElse{else_id}\n" +
        f"skipIf{if_id}:\n"
    )

    p.parser.ifCount += 1

def p_elseSection(p):
    """
    ElseSection : ELSE LoopContent
    """
    p[0] = p[2]+"\n"

def p_elseSection_empty(p):
    """
    ElseSection : 
    """
    p[0] = ""

def p_forLoop(p):
    """
    ForLoop : FOR identifier ':' '=' Fator Direction Fator DO LoopContent
    """
    if p[6] == 'to':
        p[0] = f"{p[5]}storeg {p.parser.indexes[p[2]]}\nloopStart{p.parser.loopsCount}:\n{p[7]}pushg {p.parser.indexes[p[2]]}\nsupeq\njz loopEnd{p.parser.loopsCount}"
        p[0] = p[0] + "\n" + p[9]
        p[0] = "\n" + p[0] + f"\npushg {p.parser.indexes[p[2]]}\npushi 1\nadd\nstoreg {p.parser.indexes[p[2]]}\njump loopStart{p.parser.loopsCount}\nloopEnd{p.parser.loopsCount}:"
    else:
        p[0] = f"{p[5]}storeg {p.parser.indexes[p[2]]}\nloopStart{p.parser.loopsCount}:\n{p[7]}pushg {p.parser.indexes[p[2]]}\ninfeq\njz loopEnd{p.parser.loopsCount}"
        p[0] = p[0] + "\n" + p[9]
        p[0] = "\n" + p[0] + f"\npushg {p.parser.indexes[p[2]]}\npushi 1\nsub\nstoreg {p.parser.indexes[p[2]]}\njump loopStart{p.parser.loopsCount}\nloopEnd{p.parser.loopsCount}:"

    p.parser.loopsCount = p.parser.loopsCount + 1

def p_direction(p):
    """
    Direction : TO
              | DOWNTO
    """
    p[0] = p[1]

def p_LoopContent_mutiple(p):
    """
    LoopContent : BEGIN CodeLines END
    """
    p[0] = p[2]

def p_LoopContent_single(p):
    """
    LoopContent : Statement
    """
    p[0] = p[1]

def p_value_stringARG(p):
    """
    Value : stringARG
    """
    p[0] = f"pushs \"{p[1]}\"\n"
    p.parser.nextWrite = "string"

def p_value_boolean(p):
    """
    Value : TRUE
          | FALSE
    """
    if (p[1] == 'true'):
        p[0] = f"pushi 1\n"
    elif (p[1] == 'false'):
        p[0] = f"pushi 0\n"

    p.parser.nextWrite = "boolean"

def p_value_expression(p):
    """
    Value : Expression
    """
    p[0] = p[1]
    
def p_expression_add(p):
    """
    Expression : Expression '+' Term
    """
    code = ""

    code += compile_operand(p[1], p)
    code += compile_operand(p[3], p)
    code += "add\n"
    p[0] = code
    p.parser.nextWrite = "number"

def p_expression_sub(p):
    """
    Expression : Expression '-' Term
    """
    code = ""

    code += compile_operand(p[1], p)
    code += compile_operand(p[3], p)
    code += "sub\n"
    p[0] = code
    p.parser.nextWrite = "number"

def p_expression_term(p):
    """
    Expression : Term
    """
    p[0] = p[1]

def p_termo_mult_fator(p):
    """
    Term : Term '*' Fator
    """
    code = ""

    code += compile_operand(p[1], p)
    code += compile_operand(p[3], p)
    code += "mul\n"
    p[0] = code

def p_termo_div_fator(p):
    """
    Term : Term DIV Fator
    """
    code = ""

    code += compile_operand(p[1], p)
    code += compile_operand(p[3], p)
    code += "div\n"
    p[0] = code

def p_termo_mod_fator(p):
    """
    Term : Term MOD Fator
    """
    code = ""

    code += compile_operand(p[1], p)
    code += compile_operand(p[3], p)
    code += "mod\n"
    p[0] = code

def p_termo_fator(p):
    """
    Term : Fator
    """
    p[0] = p[1]

def p_fator_arrayElement(p):
    """
    Fator : identifier '[' Fator ']'
    """
    code = ""
    if p.parser.types[p[1]] == 'string':
        base_index = p.parser.indexes[p[1]]
        # Fetch string from the stack
        code = f"pushg {base_index}\n"

        # Load index expression and adjust it
        code += p[3] + "pushi 1\nsub\n"
        
        # Get ASCII code of string[p[3]]
        code += "charat\n"

        p.parser.nextWrite = p.parser.types[p[1]]
        
    elif p[1] in p.parser.arrays:
        arr_info = p.parser.arrays[p[1]]
        base_index = p.parser.indexes[p[1]]
        lower_bound = arr_info['lower_bound']
        
        code = "pushgp\n"
        # Load index expression
        code += p[3]

        # Adjust index 
        if lower_bound != 0:
            code += f"pushi {lower_bound-base_index}\nsub\n"

        # Load from given index
        code += "loadn\n"

        p.parser.nextWrite = arr_info['element_type']

    else:
        raise Exception(f"Semantic Error: Index access cannot be applied to '{p[1]}'")

    p[0] = code

def p_fator_exp(p):
    """
    Fator : '(' Expression ')'
    """
    p[0] = p[2]

def p_fator_identifier(p):
    """
    Fator : identifier
    """
    p[0] = compile_operand(p[1], p)

def p_fator_lengthFunc(p):
    """
    Fator : LENGTH '(' identifier ')'
    """
    if p.parser.types[p[3]] == 'string':
        p[0] = f"pushg {p.parser.indexes[p[3]]}\nstrlen\n"
    elif p[3] in p.parser.arrays:
        arr_info = p.parser.arrays[p[3]]
        p[0] = f"pushi {arr_info['length']}\n"
    else:
        raise Exception(f"Semantic Error: LENGTH cannot be applied to '{p[3]}'")

def p_fator_num(p):
    """
    Fator : num
    """
    p[0] = compile_operand(p[1], p)

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

parser = yacc.yacc(debug=True)
parser.indexes = {}
parser.types = {}
parser.arrays = {}
parser.index = 0
parser.nextWrite = ""
parser.loopsCount = 0
parser.ifCount = 0
parser.elseCount = 0

import sys
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
texto = sys.stdin.read()

parser.success = True
parser.parse(texto)
if parser.success:
    print("Programa válido:\n", texto)
else:
    print("Programa inválido... Corrija e tente novamente!")