def compile_operand(op, p):
        if isinstance(op, int):
            p.parser.nextWrite = "integer"
            return f"pushi {op}\n"
        elif isinstance(op, float):
            p.parser.nextWrite = "double"
            return f"pushf {op}\n"
        elif isinstance(op, str) and op in p.parser.indexes:
            p.parser.nextWrite = p.parser.types[p[1]]
            return f"pushg {p.parser.indexes[op]}\n"
        
        else:
            return op  # already compiled code
        
import re

def is_single_char_string(code):
    return bool(re.fullmatch(r'pushs\s+"(.)"\n', code))