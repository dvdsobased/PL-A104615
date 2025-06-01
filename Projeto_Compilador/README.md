# PL-Project

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
