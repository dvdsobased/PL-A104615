# Relatório Processamento de Linguagens

## Índice

- [1. Introdução](#1-introdução)
- [2. Guia de Utilização](#2-guia-de-utilização)
- [3. Arquitetura Geral do Compilador](#3-arquitetura-geral-do-compilador)
- [4. Análise Léxica](#4-análise-léxica)
- [5. Análise Sintática](#5-análise-sintática)
- [6. Análise Semântica](#6-análise-semântica)
- [7. Geração de código](#7-geração-de-código)
- [8. Testes](#8-testes)
- [9. Conclusão](#9-conclusão)

---
## 1. Introdução

Este relatório descreve o desenvolvimento de um compilador para a linguagem Pascal Standard, realizado no âmbito da unidade curricular de Processamento de Linguagens.

O principal objetivo do projeto foi aplicar os conceitos teóricos de compiladores, através da implementação de todas as fases fundamentais: análise léxica, análise sintática, análise semântica e geração de código. O compilador desenvolvido reconhece uma versão simplificada, mas representativa, da linguagem Pascal, sendo capaz de traduzir programas para uma máquina virtual didática (EWVM).

Durante o desenvolvimento, foram utilizadas ferramentas como o **Python** e a biblioteca **PLY (Python Lex-Yacc)** para construir o analisador léxico e o analisador sintático. A geração de código foi feita diretamente nas regras da gramática (tradução dirigida pela sintaxe), resultando em instruções compreendidas pela EWVM.

O compilador suporta declarações de variáveis (simples e arrays), comandos de entrada/saída (`readln`, `writeln`), estruturas de controlo (`if`, `while`, `for`), expressões aritméticas e booleanas, entre outras funcionalidades da linguagem Pascal.

O presente relatório documenta toda a arquitetura do compilador, explica a implementação técnica de cada fase e apresenta os testes realizados com programas de exemplo. Finalmente, são também analisadas limitações e possíveis melhorias para uma versão futura.

## 2. Guia de Utilização

Para executar o programa devemos realizar os seguintes passos:

1. Inserir o programa Pascal que queremos compilar no ficheiro `pascalProgram.pas`;
2. Executar o analisador sintático através do seguinte comando:
```
cat pascalProgram.pas | python pascal_sin.py
```
3. Copiar a código traduzido e colar na VM
```bash
Pascal Program Traduzido:
pushi 0
start
pushi 0
storeg 0
pushg 0
not
jz skipIf0
pushs "O utilizador está inativo."
writes
writeln
jump skipElse0
skipIf0:
pushs "O utilizador está ativo."
writes
writeln
skipElse0:
stop
```
4. Correr o código colado na VM e verificar se o resultado é o esperado.

## 3. Arquitetura Geral do Compilador

O compilador desenvolvido está dividido em três componentes principais, cada um responsável por uma fase distinta do processo de compilação. A implementação foi modularizada em diferentes ficheiros Python, com responsabilidades bem definidas:

- **`pascal_lex.py`** – responsável pela análise léxica, transformando o código fonte Pascal numa sequência de tokens, identificando palavras reservadas, identificadores, números, operadores, strings e outros símbolos relevantes.

- **`pascal_sin.py`** – implementa a análise sintática e a geração de código. A gramática da linguagem é definida neste ficheiro usando `ply.yacc`, e o código para a máquina virtual (EWVM) é gerado diretamente em cada regra de produção, através de tradução dirigida pela sintaxe.

- **`utils.py`** – contém funções auxiliares de apoio à geração de código, como `compile_operand` (compilação de operandos numéricos ou variáveis) e utilitários para trabalhar com strings.

Além destes módulos, o compilador inclui uma série de ficheiros de teste (`.pas`) que contêm programas escritos em Pascal e que foram utilizados para validar o funcionamento do compilador.

A arquitetura adotada segue um modelo tradicional de compilador, com a geração de código integrada diretamente nas ações sintáticas, o que simplifica a tradução.

Para gerir o estado interno durante o parsing, foram utilizadas estruturas auxiliares como:

- `parser.indexes`: mapeia variáveis ao seu índice na stack global;
- `parser.types`: guarda o tipo de cada variável;
- `parser.arrays`: armazena informação adicional sobre arrays (limites, tamanho e tipo de elementos);
- `parser.loopsCount`, `parser.ifCount`, `parser.elseCount`: utilizados para gerar rótulos únicos em estruturas de controlo.

Esta separação modular permitiu uma implementação organizada e facilitou a identificação e resolução de problemas ao longo do desenvolvimento.

## 4. Análise Léxica

A análise léxica foi implementada no ficheiro `pascal_lex.py`, com recurso à biblioteca `PLY` (Python Lex-Yacc), concretamente ao módulo `lex`. Esta fase do compilador tem como função transformar o código fonte Pascal numa sequência de *tokens*, ou seja, unidades léxicas que representam os blocos básicos da linguagem, como palavras reservadas, identificadores, operadores, símbolos e literais.

### 4.1 Tokens e literals definidos

Os tokens definidos no analisador são palavras reservadas, identificadores, literais numéricos e de texto, bem como operadores e símbolos especiais. As palavras reservadas são reconhecidas através de funções específicas, e os símbolos literais são definidos diretamente na lista `literals`.

```python
literals = [';', ',', ':', '(', ')', '=', '*', '+', '-', '.', '<', '>', '[', ']']
tokens = ['stringARG', 'num', 'identifier', 'PROGRAM', 'BEGIN', 'END', 'VAR', 'TYPE', 
          'FOR', 'TO', 'DOWNTO', 'DO', 'WHILE', 'WRITELN', 'READLN', 'IF', 'THEN', 'ELSE', 
          'TRUE', 'FALSE', 'NOT', 'AND', 'OR', 'DIV', 'MOD', 'ARRAY', 'OF', 'DOUBLEDOT', 'LENGTH']
```
Os seguintes literais são definidos diretamente no analisador léxico:

- `;` – Fim de instrução
- `,` – Separador de elementos
- `:` – Declaração de tipo ou parte do operador `:=`
- `(` `)` – Parênteses
- `=` – Igualdade
- `*` – Multiplicação
- `+` – Adição
- `-` – Subtração
- `.` – Fim de programa
- `<` `>` – Comparações
- `[` `]` – Indexação em arrays ou strings

Estes tokens representam palavras reservadas, tipos de dados, operadores e símbolos compostos reconhecidos via expressões regulares:

- `stringARG` – Strings literais (ex: `'texto'`)
- `num` – Números inteiros ou reais
- `identifier` – Identificadores (nomes de variáveis, funções, etc.)
- `PROGRAM` – Palavra reservada `program`
- `BEGIN` – Palavra reservada `begin`
- `END` – Palavra reservada `end`
- `VAR` – Palavra reservada `var`
- `TYPE` – Tipos de dados (`integer`, `boolean`, etc.)
- `FOR` – Palavra reservada `for`
- `TO` – Palavra reservada `to`
- `DOWNTO` – Palavra reservada `downto`
- `DO` – Palavra reservada `do`
- `WHILE` – Palavra reservada `while`
- `WRITELN` – Palavra reservada `writeln` (ou `write`)
- `READLN` – Palavra reservada `readln` (ou `read`)
- `IF` – Palavra reservada `if`
- `THEN` – Palavra reservada `then`
- `ELSE` – Palavra reservada `else`
- `TRUE` – Valor booleano verdadeiro
- `FALSE` – Valor booleano falso
- `NOT` – Operador lógico de negação
- `AND` – Operador lógico `and`
- `OR` – Operador lógico `or`
- `DIV` – Divisão inteira
- `MOD` – Resto da divisão inteira
- `ARRAY` – Palavra reservada para declarar arrays
- `OF` – Palavra reservada usada em `array of ...`
- `DOUBLEDOT` – Símbolo `..`, usado para intervalos em arrays
- `LENGTH` – Função incorporada `length(...)`

### 4.2 Palavras reservadas
As palavras reservadas são reconhecidas por funções próprias, cada uma com uma expressão regular case-insensitive. Por exemplo, para reconhecer a palavra reservada `program`:
```python
def t_PROGRAM(t):
    r'\b[pP][rR][oO][gG][rR][aA][mM]\b'
    t.value = t.value.lower()
    return(t)

```
Esta abordagem é repetida para todas as outras palavras reservadas, como `begin`, `end`, `if`, `then`, `else`, `while`, `for`, `readln`, `writeln`, entre outras.
Cada token converte a palavra para minúsculas, garantindo consistência no processamento posterior.

### 4.3 Identificadores e valores literais

O token `identifier`reconhece nomes de variáveis e procedimentos:
```python
def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return(t)

```
Os números (inteiros ou reais) são processados pelo token `num`, que converte automaticamente o valor para `int` ou `float`:

```python
def t_num(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

```
As strings, delimitadas por aspas simples, são tratadas da seguinte forma:

```python
def t_stringARG(t):
    r'\'(\\.|[^\'\\])*\''
    t.value = t.value[1:-1]
    return t
```
### 4.4 Intervalos e arrays
A linguagem suporta declarações de arrays com intervalos do tipo 1..5. Este operador é reconhecido com o token `DOUBLEDOT`:
```python
def t_DOUBLEDOT(t):
    r'\.\.'
    return(t)
```
A própria palavra reservada `array` também é reconhecida por uma função específica:
```python
def t_ARRAY(t):
    r'\b[aA][rR][rR][aA][yY]\b'
    t.value = t.value.lower()
    return(t)
```

### 4.5 Comentários e ignorar espaços
Os comentários no estilo Pascal `({ ... })` são ignorados durante a análise léxica:
```python
def t_comment(t):
    r'\{[^}]*\}'
    pass
```
Também ignora espaços, tabulações e quebras de linha:
```python
t_ignore = " \t\n"

```

### 4.6 Tratamento de erros léxicos
Se for encontrado um carácter ilegal que não corresponde a nenhum token definido, o analisador imprime uma mensagem e ignora o carácter, permitindo continuar a permite continuar a análise léxica:

```python
def t_error(t):
    print('Caráter ilegal: ', t.value[0])
    t.lexer.skip(1)

```


Em síntese, o analisador léxico implementado apresenta uma estrutura completa e eficaz, conseguindo reconhecer corretamente os principais componentes da linguagem Pascal, como identificadores, palavras reservadas, operadores, arrays e valores literais. Esta fase garante que o código-fonte seja convertido numa sequência clara e coerente de tokens, facilitando o processamento correto na etapa seguinte da análise sintática.

## 5. Análise Sintática

A análise sintática do compilador Pascal foi desenvolvida no ficheiro pascal_syn.py, utilizando a biblioteca PLY, que fornece ferramentas para definir gramáticas com base em regras de produção. Esta fase do compilador tem dois objetivos principais:

- Validar se a sequência de tokens produzida pelo analisador léxico forma um programa Pascal sintaticamente válido;
- Traduzir a árvore sintática abstrata (AST) para código intermédio executável na máquina virtual EWVM.

Durante a análise sintática, são ainda mantidas estruturas auxiliares para o contexto da tradução.

Neste processo, também foram incluídas verificações de coerência semântica dentro das regras sintáticas, como a validação de tipos nas atribuições (`p_statement_define_*`) e o tratamento de erros de indexação.

No final do processo, o parser imprime o código EWVM gerado, permitindo a sua execução ou análise posterior.

### 5.1 Estrutura geral do programa

O ponto de entrada de qualquer programa Pascal é analisado pela seguinte regra:

```python
def p_program(p):
    """
    PascalProgram : PROGRAM identifier ';' VarSection CodeBlock
    """
    p[0] = p[4] + p[5]
```

Esta regra corresponde a um programa Pascal típico que começa com a palavra-chave `PROGRAM`, seguida do nome do programa, uma secção opcional de variáveis e, por fim, o bloco de código principal entre `BEGIN` e `END`.

### 5.2 Declarações de variáveis e arrays

As variáveis são declaradas após a palavra reservada `VAR`, e a sua interpretação depende do tipo definido.

```pascal
VAR
  x, y : integer;
  nome : string;
```

O código seguinte trata declarações com as regras:

```python
def p_varSingleStatement(p):
    """
    VarSingleStatement : VarStatementIdentifiers ':' VarType ';'
    """
```

Para arrays, o compilador calcula o comprimento do array e guarda os seus metadados num dicionário para posterior acesso:

```python
def p_varType_array(p):
    """
    VarType : ARRAY '[' num DOUBLEDOT num ']' OF TYPE
    """
```

### 5.4 Bloco de Código e Instruções
As instruções principais do corpo do programa estão contidas entre `BEGIN` e `END.`:

```pascal
BEGIN
  ReadLn(x);
  WriteLn('Valor: ', x);
END.
```

Estas instruções são tratadas por:
```python
def p_codeBlock(p):
    """CodeBlock : BEGIN CodeLines END '.'"""
```

Cada linha de código pode terminar com `;`, mas também se aceita a última sem ponto e vírgula. Esta flexibilidade é gerida com as regras:
```python
def p_statement_with_optional_semicolon(p):
    """StatementWithOptionalSemicolon : Statement ';' | Statement"""
```

### 5.3 Condições e Estruturas de Controlo
O analisador suporta `IF`, `WHILE`, e `FOR`, incluindo blocos aninhados e `else if`.

```python
def p_statement_if_then_else(p):
    """Statement : IF Condition THEN LoopContent ElseChain"""
```

```python
def p_statement_while(p):
    """Statement : WHILE Condition DO LoopContent"""
```

```python
def p_forLoop(p):
    """ForLoop : FOR identifier ':' '=' Fator Direction Fator DO LoopContent"""
```

Os identificadores únicos como `loopStart`, `skipIf` e `loopEnd` garantem que os saltos no código EWVM não se sobrepõem.

### 5.4 Leitura e Escrita

A análise sintática reconhece também instruções de `readln` e `writeln` com diferentes tipos, tratadas com regras específicas. O compilador deteta o tipo da variável com base em `parser.types` e gera código adequado:

```python
def p_statement_read(p):
    """
    Statement : READLN '(' identifier ')'
    """
```

```python
def p_statement_write(p):
    """Statement : WRITELN '(' Arguments ')'"""
```

### 5.5 Expressões Aritméticas e Operações
As expressões aritméticas são processadas de forma recursiva e convertidas diretamente em instruções EWVM:

```python
def p_expression_add(p):
    """Expression : Expression '+' Term"""

```
A função `compile_operand`, definida no ficheiro `utils.py`, é utilizada para gerar o código adequado conforme o tipo do operando:

```python
def compile_operand(op, p):
    if isinstance(op, int):
        return f"pushi {op}\n"
```

### 5.6 Arrays e Indexação
A indexação de arrays está também suportada, tanto para leitura como para escrita. O compilador ajusta o índice com base no `lower_bound` do array:
```python
def p_fator_arrayElement(p):
    """
    Fator : identifier '[' NumValue ']'
    """
    ...

```

O acesso e atribuição a elementos de arrays é suportado:

```python
def p_fator_arrayElement(p):
    """Fator : identifier '[' Fator ']'"""

def p_statement_define_arraySpecial(p):
    """Statement : identifier '[' Fator ']' ':' '=' Value"""

```
O compilador ajusta o índice com base no limite inferior e usa as instruções `loadn` e `storen` da EWVM para manipular os valores.

### 5.7 Funções Integradas
O compilador suporta a função `length()` tanto para arrays como para strings:

```python
def p_lengthFunc(p):
    """
    NumValue : LENGTH '(' identifier ')'
    """
    ...
```

### 5.8 Geração do Código Final
No final da análise, se o programa for válido, é impresso o código EWVM completo:
```python
if parser.success:
    print("Programa válido:\n", texto)

```
Este código pode depois ser executado no interpretador EWVM para simular o comportamento do programa Pascal.

## 6. Análise Semântica

A análise semântica é responsável por garantir que, mesmo que o código esteja sintaticamente correto, respeita as regras de coerência de tipos e uso válido de variáveis. No compilador desenvolvido, esta análise foi integrada na fase sintática, sendo realizada diretamente nas regras do parser com recurso a estruturas auxiliares e exceções explícitas (`raise Exception`).

### 6.1 Gestão de Tipos e Atribuições

Cada variável declarada é associada ao seu tipo semântico na tabela `parser.types`. Este mapeamento é usado posteriormente para validar instruções de leitura, escrita, atribuição e acesso a arrays.
```python
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

```
Este excerto garante que apenas variáveis integer ou double podem receber valores numéricos, rejeitando atribuições ilegais como `x:='abc'` para `x:integer`.

### 6.2 Atribuição entre Variáveis

Por sua vez, é também verificada a a compatibilidade entre variáveis no momento da atribuição:
```python
def p_statement_define_identifier(p):
    """
    Statement : identifier ':' '=' identifier
    """
    if (p.parser.types[p[1]] == p.parser.types[p[4]]) or \
       (p.parser.types[p[1]] == 'integer' and p.parser.types[p[4]] == 'double') or \
       (p.parser.types[p[1]] == 'double' and p.parser.types[p[4]] == 'integer'):
        p[0] = f"pushg {p.parser.indexes[p[4]]}\nstoreg {p.parser.indexes[p[1]]}"
    else:
        raise Exception(f"Semantic Error: Cannot ASSIGN '{p[4]}' value to '{p[1]}'")

```
### 6.3 Verificação de Tipos em Condições
A atribuição de valores booleanos também está sujeita a verificação:
```python
def p_statement_define_boolean(p):
    """
    Statement : identifier ':' '=' Condition
    """
    if p.parser.types[p[1]] == 'boolean':
        p[0] = p[4] + f"storeg {p.parser.indexes[p[1]]}"
    else:
        raise Exception(f"Semantic Error: Cannot ASSIGN boolean value to '{p[1]}'")

```

### 6.4 Validação de Acessos a Arrays
O acesso a arrays é validado semanticamente com base em `parser.arrays`. É gerado erro se se tentar aceder a um índice de uma variável que não seja array:
```python
def p_fator_arrayElement(p):
    """
    Fator : identifier '[' Fator ']'
    """
    ...
    else:
        raise Exception(f"Semantic Error: Index access cannot be applied to '{p[1]}'")

```
Adicionalmente ajusta-se corretamente o índice com base no `lower_bound` definido na declaração:
```python
if lower_bound != 0:
    code += f"pushi {lower_bound-base_index}\nsub\n"
```

### 6.5 Função LENGTH
A função `length(...)` está restrita semanticamente a strings e arrays:
```python
def p_fator_lengthFunc(p):
    """
    Fator : LENGTH '(' identifier ')'
    """
    if p.parser.types[p[3]] == 'string':
        p[0] = f"pushg {p.parser.indexes[p[3]]}\nstrlen\n"
    elif p[3] in p.parser.arrays:
        p[0] = f"pushi {arr_info['length']}\n"
    else:
        raise Exception(f"Semantic Error: LENGTH cannot be applied to '{p[3]}'")
```
### 6.6 Inicialização de Variáveis e Arrays
O compilador garante que todas as variáveis e arrays são inicializados com valores por omissão, evitando referências indefinidas. A instrução correta é gerada com base no tipo.

Cada variável declarada é inicializada no momento da declaração:
```python
if p[3] == 'string':
    p[0] = p[0] + 'pushs ""'
elif p[3] == 'integer':
    p[0] = p[0] + 'pushi 0'

```

Para arrays, por sua vez, o compilador reserva espaço contínuo:
```python
for idx in range(arr_info['length']):
    if arr_info['element_type'] == 'string':
        p[0] += 'pushs ""'

```

## 7. Geração de Código EWVM

A geração de código é a fase responsável por transformar a árvore sintática anotada e validada semanticamente num conjunto de instruções para a máquina virtual **EWVM** (Educational Virtual Machine), usada como alvo final da compilação.

No compilador implementado, esta geração de código é feita diretamente nas regras do parser através da construção de strings contendo instruções EWVM, associadas a cada produção da gramática.

### 7.1 Inicialização de Variáveis

Cada variável declarada é alocada sequencialmente na stack, com base na posição atual (`parser.index`). As instruções geradas dependem do tipo:

```pascal
var a: integer;
```
```
pushi 0
```
No caso dos arrays:
```pascal
var x: array[1..3] of string;
```

```
pushs ""
pushs ""
pushs ""
```

### 7.2 Atribuições e Leituras

A escrita de valores em variáveis traduz-se em instruções `storeg`, sendo precedida pelo valor a colocar na stack:
```pascal
a := 5;
```

```
pushi 5
storeg 0
```

No caso de leitura com `readln`, o tipo da variável determina o pipeline de conversão necessário:
```pascal
readln(a);
```

```
read
atoi
storeg 0
```

### 7.3 Escrita de Dados
A instrução `writeln` pode aceitar múltiplos argumentos. Cada argumento é analisado para determinar o tipo de escrita correta:

```pascal
writeln('resultado:', a);
```

```
pushs "resultado:"
writes
pushg 0
writei
writeln
```

### 7.4 Expressões e Operadores
As expressões aritméticas e booleanas são traduzidas diretamente para instruções como `add`, `sub`, `mul`, `div`, `mod`, `and`, `or`, etc. Os operandos são empilhados na ordem correta:

```pascal
writeln('resultado:', a);
```

```
pushg 1
pushi 3
add
storeg 0
```
### 7.5 Controlo de Fluxo
*Condições (if / else)*:

O compilador gera etiquetas únicas (`skipIfX`, `skipElseY`) para gerir saltos condicionais:
```pascal
if a = 5 then
  writeln('ok')
else
  writeln('fail');

```

```
pushg 0
pushi 5
equal
jz skipIf0
pushs "ok"
writes
writeln
jump skipElse0
skipIf0:
pushs "fail"
writes
writeln
skipElse0:

```

*Ciclos `while`*:

```pascal
while a < 10 do
  a := a + 1;
```
```
whileLoopStart0:
pushg 0
pushi 10
inf
jz whileLoopEnd0
pushg 0
pushi 1
add
storeg 0
jump whileLoopStart0
whileLoopEnd0:

```

*Ciclos `for`*:
```pascal
for i := 1 to 3 do
  writeln(i);

```
```
pushi 1
storeg 0
loopStart0:
pushi 3
pushg 0
supeq
jz loopEnd0
pushg 0
writei
writeln
pushg 0
pushi 1
add
storeg 0
jump loopStart0
loopEnd0:

```

### 7.6 Estrutura Final do Programa
O programa Pascal é encapsulado com instruções de arranque e paragem da EWVM:
```
start
<corpo gerado>
stop
```

A geração de código no compilador foi feita de forma modular e progressiva, permitindo adaptar facilmente o output às regras da EWVM. A utilização de estruturas auxiliares (`types`, `indexes`, `arrays`) permite produzir instruções corretas e contextualizadas, garantindo que o programa Pascal se traduz corretamente num conjunto de instruções executável na EWVM.

## 8. Testes

Para validar o funcionamento do compilador Pascal desenvolvido, foram elaborados alguns testes representativos com diferentes estruturas da linguagem. Estes testes permitiram verificar não só a correção sintática e semântica, mas também a geração correta de código para a EWVM, assegurando que o comportamento em tempo de execução corresponde ao esperado.

- Teste 1:
```pascal
program ParOuImpar;
var
  num: integer;
  par: boolean;
begin
  num := 4;
  par := (num mod 2) = 0;
  if par then
    writeln(num, ' é par')
  else
    writeln(num, ' é ímpar')
end.
```

- Teste 2:
```pascal
program NegarBooleano;
var
    valor: boolean;
begin
    valor := true;
    writeln('Valor original: ', valor);
    valor := not valor;
    writeln('Valor negado: ', valor);
end.
```

- Teste 3:
```pascal
program NumeroNoIntervalo;
var
    num: integer;
begin
    writeln('Introduza um número:');
    readln(num);

    if (num >= 10) and (num <= 100) then
        writeln('Está no intervalo [10, 100].')
    else
        writeln('Fora do intervalo.');
end.
```

- Teste 4:
```pascal
program ContemLetraA;
var
    texto: string;
    i: integer;
    encontrou: boolean;
begin
    writeln('Introduza uma string:');
    readln(texto);

    encontrou := false;
    i := 1;
    while (i <= length(texto)) and (not encontrou) do
    begin
        if texto[i] = 'a' then
            encontrou := true;
        i := i + 1;
    end;
    if encontrou then
        writeln('Contém a letra a.')
    else
        writeln('Não contém a letra a.');
end.
```

- Teste 5:
```pascal
program ListaNomes;
var
 nomes: array[1..3] of string;
 i: integer;
begin
  writeln('Introduza 3 nomes:');
  for i := 1 to 3 do
    readln(nomes[i]);

  writeln('Os nomes inseridos foram:');
  for i := 1 to 3 do
    writeln(nomes[i]);
end.
```

- Teste 6:
```pascal
program LetraAPorCinco;
var
  i: integer;
  letras: string;
begin
  letras := 'A';
  for i := 1 to 5 do
    writeln(letras)
end.
```

- Teste 7:
```pascal
program TesteNot;
var
  ativo: boolean;
begin
  ativo := false;
  if not ativo then
    writeln('O utilizador está inativo.')
  else
    writeln('O utilizador está ativo.')
end.
```
## 9. Conclusão

O desenvolvimento deste compilador para uma versão simplificada da linguagem Pascal permitiu consolidar os conhecimentos, desde a análise léxica até à geração de código para uma máquina virtual didática (EWVM).

Durante o projeto, foi possível compreender na prática como cada fase de um compilador contribui para a tradução correta de um programa: a análise léxica garantiu o reconhecimento dos elementos básicos da linguagem; a análise sintática estruturou os programas em construções válidas; a análise semântica assegurou coerência no uso de variáveis, tipos e estruturas de dados; e a geração de código transformou os programas em instruções executáveis pela EWVM.

As principais dificuldades enfrentadas surgiram na implementação de estruturas complexas como arrays, ciclos for e while, e condições if-then-else aninhadas, especialmente na gestão correta de índices, rótulos únicos e compatibilidade semântica entre diferentes tipos de dados. No entanto, a abordagem modular adotada e o uso de estruturas auxiliares para manter o contexto tornaram possível ultrapassar estes desafios.

O compilador resultante consegue traduzir uma parte significativa da linguagem Pascal, incluindo variáveis simples e estruturadas, expressões aritméticas e lógicas, comandos de entrada e saída, ciclos e condições. Além disso, suporta funcionalidades adicionais como a função integrada length, leitura de strings e escrita de múltiplos argumentos em writeln.

Este projeto revelou-se uma experiência extremamente enriquecedora e demonstrou, na prática, como os conceitos teóricos de compiladores podem ser aplicados para construir uma ferramenta funcional.
