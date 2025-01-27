import sys
from Principal import Lexical, Token, TokenType, TabelaSimbolos


lexer = Lexical("temp.txt")
Token = lexer.get_next_token()
symbol_table = TabelaSimbolos()
label = 1
memory_position = 1



errorlog = open("errorlog.txt", "w")
gera2 = open("gera2.obj", "w")


def get_next_token():
    global Token
    Token = lexer.get_next_token()


def gera(label, instruction, attribute1, attribute2):
    with open("gera2.obj", "a") as gera2:  # Abre em modo append
        formatted_label = f"L{label.strip()}" if label.strip().isdigit() else label.strip()
        
        if instruction in ["CALL", "JMP", "JMPF"] and attribute1.strip().isdigit():  # Verifica se é 'CALL', 'JMP', ou 'JMPF' e se o atributo é numérico
            formatted_attr1 = f"L{attribute1.strip()}"
        else:
            formatted_attr1 = attribute1.strip()
        
        formatted_attr2 = attribute2.strip() if attribute2.strip() else ""  # Garante que não haja espaços extras
        
        if instruction == "CALL":
            line = f"{formatted_label}{instruction}  {formatted_attr1} {formatted_attr2}"  # Sem espaço antes de CALL, com 2 espaços entre CALL e L<num>
        else:
            line = f"{formatted_label} {instruction} {formatted_attr1} {formatted_attr2}".strip()
        
        gera2.write(line + "\n")



def geraToken(postfix):
    for elem in postfix:
        if elem == "nao":
            gera("", "NEG", "", "")
        elif elem == "e":
            gera("", "AND", "", "")
        elif elem == "ou":
            gera("", "OR", "", "")
        elif elem == "+":
            gera("", "ADD", "", "")
        elif elem == "-":
            gera("", "SUB", "", "")
        elif elem == "*":
            gera("", "MULT", "", "")
        elif elem == "div":
            gera("", "DIVI", "", "")  
        elif elem == "=":
            gera("", "CEQ", "", "")
        elif elem == "!=":
            gera("", "CDIF", "", "")
        elif elem == "<":
            gera("", "CME", "", "")
        elif elem == ">":
            gera("", "CMA", "", "")
        elif elem == "<=":
            gera("", "CMEQ", "", "")
        elif elem == ">=":
            gera("", "CMAQ", "", "")
        elif elem == "-u":
            gera("", "INV", "", "")  
        elif elem == "verdadeiro":
            gera("", "LDC", "1", "") 
        elif elem == "falso":
            gera("", "LDC", "0", "")  
        elif symbol_table.contains(elem):
            symbol_type = symbol_table.get_type(elem)
            if symbol_type in ["funcao inteiro", "funcao booleano"]:
                gera("", "LDV", "0", "")
            else:
                gera("", "LDV", symbol_table.get_address(elem), "")
        else:
            gera("", "LDC", elem, "")  


def infer_type(postfix_expr):
    type_stack = []

    def is_operator(Token):
        return Token in ["+", "-", "*", "div", "=", "!=", "<", ">", "<=", ">=", "e", "ou", "nao", "+u", "-u"]

    def is_number(Token):
        return Token.isdigit()

    for Token in postfix_expr:
        if not is_operator(Token):
            if is_number(Token):
                type_stack.append("inteiro")
            elif Token in ["verdadeiro", "falso"]:
                type_stack.append("booleano")
            else:
                token_type = symbol_table.get_type(Token)
                if token_type in ["inteiro", "booleano"]:
                    type_stack.append(token_type)
                elif token_type == "funcao inteiro":
                    type_stack.append("inteiro")
                elif token_type == "funcao booleano":
                    type_stack.append("booleano")
                else:
                    raise RuntimeError(f"Tipo inválido para o Token '{Token}'. Linha: {lexer.get_current_line()}")
        else:
            if Token in ["+", "-", "*", "div"]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "inteiro" or left != "inteiro":
                    raise RuntimeError(f"Operadores aritméticos requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("inteiro")
            elif Token in ["+u", "-u"]:
                if not type_stack:
                    raise RuntimeError("Operandos insuficientes.")
                operand = type_stack.pop()
                if operand != "inteiro":
                    raise RuntimeError(f"Operadores unários requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("inteiro")
            elif Token in ["=", "!="]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != left:
                    raise RuntimeError(f"Operadores de igualdade requerem operandos do mesmo tipo. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token in ["<", ">", "<=", ">="]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "inteiro" or left != "inteiro":
                    raise RuntimeError(f"Operadores relacionais requerem inteiros. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token in ["e", "ou"]:
                if len(type_stack) < 2:
                    raise RuntimeError("Operandos insuficientes.")
                right = type_stack.pop()
                left = type_stack.pop()
                if right != "booleano" or left != "booleano":
                    raise RuntimeError(f"Operadores lógicos requerem booleanos. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")
            elif Token == "nao":
                if not type_stack:
                    raise RuntimeError("Operandos insuficientes.")
                operand = type_stack.pop()
                if operand != "booleano":
                    raise RuntimeError(f"Operador 'nao' requer booleano. Linha: {lexer.get_current_line()}")
                type_stack.append("booleano")

    if len(type_stack) != 1:
        raise RuntimeError(f"Erro: expressão malformada. Linha: {lexer.get_current_line()}")

    return type_stack[0]



def get_next_token():
    
    global Token
    Token = lexer.get_next_token()


def analisa_expressao_simples(infix_expression):
    global Token
    if Token.token_type in ["smais", "smenos"]:
        infix_expression.append("+u" if Token.token_type == TokenType.SMAIS else "-u")
        get_next_token()
    term_analysis(infix_expression)
    while Token.token_type in ["smais", "smenos", "sou"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
        term_analysis(infix_expression)


def function_call_analysis():
    address = symbol_table.get_address(Token.lexeme)
    gera("", "CALL", address, "")
    get_next_token()


def procedure_call_analysis(address):
    gera("", "CALL", address, "")


def atrib_analysis(expected_type):
    get_next_token()
    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)
    expression_type = infer_type(postfix)

    if expression_type != expected_type:
        raise RuntimeError(f"Atribuição de tipos diferentes na linha: {lexer.get_current_line()}")

    geraToken(postfix)


def factor_analysis(infix_expression):
    global Token  

    if Token.token_type == "sidentificador":
        if symbol_table.contains(Token.lexeme):
            if symbol_table.get_type(Token.lexeme) in ["funcao inteiro", "funcao booleano"]:
                infix_expression.append(Token.lexeme)
                function_call_analysis()
            elif not symbol_table.is_procedure_or_program(Token.lexeme):
                infix_expression.append(Token.lexeme)
                get_next_token()
            else:
                raise RuntimeError(f"Procedimento usado indevidamente na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Variável não declarada na linha: {lexer.get_current_line()}")
    elif Token.token_type == "snumero":
        infix_expression.append(Token.lexeme)
        get_next_token()
    elif Token.token_type == "snao":
        get_next_token()
        infix_expression.append("nao")
        factor_analysis(infix_expression)
    elif Token.token_type == "sabre_parenteses":
        get_next_token()
        infix_expression.append("(")
        expression_analysis(infix_expression)
        if Token.token_type == "sfecha_parenteses":
            infix_expression.append(")")
            get_next_token()
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
    elif Token.token_type in ["sverdadeiro", "sfalso"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador', 'numero', 'nao' ou '(' na linha: {lexer.get_current_line()}")



def term_analysis(infix_expression):
    global Token
    factor_analysis(infix_expression)
    while Token.token_type in ["smult", "sdiv", "se"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
        factor_analysis(infix_expression)


def expression_analysis(infix_expression):
    global Token
    analisa_expressao_simples(infix_expression)
    if Token.token_type in ["smaior", "smaiorig", "sig", "smenor", "smenorig", "sdif"]:
        infix_expression.append(Token.lexeme)
        get_next_token()
        analisa_expressao_simples(infix_expression)


def analisa_leia():
    global Token
    get_next_token()
    if Token.token_type == "sabre_parenteses":
        get_next_token()
        if Token.token_type == "sidentificador":
            if symbol_table.contains(Token.lexeme) and symbol_table.get_type(Token.lexeme) == "inteiro":
                gera("", "RD", "", "")
                gera("", "STR", symbol_table.get_address(Token.lexeme), "")
                get_next_token()
                if Token.token_type == "sfecha_parenteses":
                    get_next_token()
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Variável não declarada ou tipo incompatível na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se '(' na linha: {lexer.get_current_line()}")


def analisa_escreva():
    global Token
    get_next_token()
    if Token.token_type == "sabre_parenteses":
        get_next_token()
        if Token.token_type == "sidentificador":
            if symbol_table.contains(Token.lexeme) and symbol_table.get_type(Token.lexeme) == "inteiro":
                gera("", "LDV", symbol_table.get_address(Token.lexeme), "")
                gera("", "PRN", "", "")
                get_next_token()
                if Token.token_type == "sfecha_parenteses":
                    get_next_token()
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Espera-se ')' na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Variável não declarada ou tipo incompatível na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se '(' na linha: {lexer.get_current_line()}")


def atrib_chproc():
    global Token
    if symbol_table.contains(Token.lexeme):
        var_type = symbol_table.get_type(Token.lexeme)
        address = symbol_table.get_address(Token.lexeme)
        flag = 0

        get_next_token()
        if var_type == "funcao inteiro":
            var_type = "inteiro"
            flag = 1
        elif var_type == "funcao booleano":
            var_type = "booleano"
            flag = 1

        if Token.token_type == "satribuicao" and var_type in ["inteiro", "booleano", "funcao inteiro", "funcao booleano"]:
            atrib_analysis(var_type)
            if var_type in ["inteiro", "booleano"]:
                if flag == 1:
                    gera("", "STR", "0", "")
                else:
                    gera("", "STR", address, "")
        elif var_type == "procedimento":
            procedure_call_analysis(address)
        else:
            raise RuntimeError(f"Tipo inválido na atribuição/chamada de procedimento na linha {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Variável não declarada na linha {lexer.get_current_line()}")


def analisa_se():
    global Token, label
    get_next_token()

    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)

    geraToken(postfix)

    expression_type = infer_type(postfix)
    if expression_type != "booleano":
        raise RuntimeError(f"Expressão inválida. Linha: {lexer.get_current_line()}")

    aux_label1 = label
    gera("", "JMPF", str(label), "")
    label += 1

    if Token.token_type == "sentao":
        get_next_token()
        comando_simples()

        if Token.token_type == "ssenao":
            aux_label2 = label
            gera("", "JMP", str(label), "")
            label += 1

            gera(str(aux_label1), "NULL", "", "")

            get_next_token()
            comando_simples()

            gera(str(aux_label2), "NULL", "", "")
        else:
            gera(str(aux_label1), "NULL", "", "")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'entao' na linha: {lexer.get_current_line()}")



def analisa_enquanto():
    global Token, label
    get_next_token()

    aux_label1 = label
    gera(str(label), "NULL", "", "")
    label += 1

    infix_expression = []
    expression_analysis(infix_expression)
    postfix = symbol_table.to_postfix(infix_expression)
    expression_type = infer_type(postfix)

    if expression_type != "booleano":
        raise RuntimeError(f"Expressão inválida. Linha: {lexer.get_current_line()}")

    geraToken(postfix)

    if Token.token_type == "sfaca":
        aux_label2 = label
        gera("", "JMPF", str(label), "")
        label += 1

        get_next_token()
        comando_simples()

        gera("", "JMP", str(aux_label1), "")
        gera(str(aux_label2), "NULL", "", "")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'faca' ou operador lógico na linha: {lexer.get_current_line()}")


def comando_simples():
    global Token
    if Token.token_type == "sidentificador":
        atrib_chproc()
    elif Token.token_type == "sse":
        analisa_se()
    elif Token.token_type == "senquanto":
        analisa_enquanto()
    elif Token.token_type == "sleia":
        analisa_leia()
    elif Token.token_type == "sescreva":
        analisa_escreva()
    else:
        analisa_comando()


def analisa_comando():
    global Token
    if Token.token_type == "sinicio":
        get_next_token()
        comando_simples()

        while Token.token_type != "sfim":
            if Token.token_type == "sponto_virgula":
                get_next_token()
                if Token.token_type != "sfim":
                    comando_simples()
            else:
                raise RuntimeError(f"Erro! ';' faltante na linha: {lexer.get_current_line()}")

        get_next_token()
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'inicio' ou ';' inadequado na linha: {lexer.get_current_line()}")


def analisa_func():
    global Token, label, memory_position
    get_next_token()

    if Token.token_type == "sidentificador":
        if not symbol_table.contains(Token.lexeme):
            symbol_table.push(Token.lexeme, "L", "function", str(label))

            gera(str(label), "NULL", "", "")
            label += 1

            get_next_token()
            if Token.token_type == "sdoispontos":
                get_next_token()
                if Token.token_type in ["sinteiro", "sbooleano"]:
                    symbol_table.assign_type_to_function(f"funcao {Token.lexeme}")
                    get_next_token()
                    if Token.token_type == "sponto_virgula":
                        analisa_bloco()
                    else:
                        raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")
                else:
                    raise RuntimeError(f"Erro de Sintaxe! Tipo inválido na linha: {lexer.get_current_line()}")
            else:
                raise RuntimeError(f"Erro de Sintaxe! Espera-se ':' na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Função já declarada na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")

    count = symbol_table.cut_stack()
    if count > 0:
        dalloc_start_position = memory_position - count
        gera("", "DALLOC", str(dalloc_start_position), str(count))
        memory_position = dalloc_start_position

    gera("", "RETURN", "", "")


def analisa_proc():
    global Token, label, memory_position
    get_next_token()

    if Token.token_type == "sidentificador":
        if not symbol_table.contains(Token.lexeme):
            symbol_table.push(Token.lexeme, "L", "procedimento", str(label))
            gera(str(label), "NULL", "", "")
            label += 1

            get_next_token()
            if Token.token_type == "sponto_virgula":
                analisa_bloco()
            else:
                raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")
        else:
            raise RuntimeError(f"Procedimento já declarado na linha: {lexer.get_current_line()}")
    else:
        raise RuntimeError(f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}")

    count = symbol_table.cut_stack()
    if count > 0:
        dalloc_start_position = memory_position - count
        gera("", "DALLOC", str(dalloc_start_position), str(count))
        memory_position = dalloc_start_position

    gera("", "RETURN", "", "")


def analisa_subrotina():
    global Token, label
    flag = 0
    aux_label = None

    if Token.token_type in ["sprocedimento", "sfuncao"]:
        aux_label = label
        gera("", "JMP", str(label), "")
        label += 1
        flag = 1

    while Token.token_type in ["sprocedimento", "sfuncao"]:
        if Token.token_type == "sprocedimento":
            analisa_proc()
        else:
            analisa_func()

        if Token.token_type == "sponto_virgula":
            get_next_token()
        else:
            raise RuntimeError(f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}")

    if flag == 1:
        gera(str(aux_label), "NULL", "", "")


def analisa_tipo():
    if Token.token_type not in ["sinteiro", "sbooleano"]:
        raise RuntimeError(f"Erro de Sintaxe! Tipo inválido na linha: {lexer.get_current_line()}")
    else:
        symbol_table.assign_type_to_variables(Token.lexeme)
    get_next_token()


def analisa_variaveis():
    global memory_position
    count = 0
    while True:
        if Token.token_type == "sidentificador":
            if not symbol_table.contains_var(Token.lexeme):
                symbol_table.push(Token.lexeme, "", "var", str(memory_position + count))
                count += 1
                get_next_token()

                if Token.token_type in ["svirgula", "sdoispontos"]:
                    if Token.token_type == "svirgula":
                        get_next_token()
                        if Token.token_type == "sdoispontos":
                            raise RuntimeError(
                                f"Erro de Sintaxe! Padrão indevido na linha: {lexer.get_current_line()}"
                            )
                    elif Token.token_type == "sdoispontos":
                        break
                else:
                    raise RuntimeError(
                        f"Erro de Sintaxe! Esperava-se ',' ou ':' na linha: {lexer.get_current_line()}"
                    )
            else:
                raise RuntimeError(
                    f"Variável já declarada na linha: {lexer.get_current_line()}"
                )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Esperava-se 'identificador' na linha: {lexer.get_current_line()}"
            )

    gera("", "ALLOC", str(memory_position), str(count))
    memory_position += count
    get_next_token()
    analisa_tipo()


def declaracao_variaveis():
    if Token.token_type == "svar":
        get_next_token()
        if Token.token_type == "sidentificador":
            while Token.token_type == "sidentificador":
                analisa_variaveis()
                if Token.token_type == "sponto_virgula":
                    get_next_token()
                else:
                    raise RuntimeError(
                        f"Erro de Sintaxe! Espera-se ';' na linha: {lexer.get_current_line()}"
                    )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Espera-se 'identificador' na linha: {lexer.get_current_line()}"
            )


def analisa_bloco():
    get_next_token()
    declaracao_variaveis()
    analisa_subrotina()
    analisa_comando()


def main():
    try:
        global Token  
        
        if Token.token_type == "sprograma":
            get_next_token()
            if Token.token_type == "sidentificador":
                symbol_table.push(Token.lexeme, "", "programa", "")
                get_next_token()
                if Token.token_type == "sponto_virgula":
                    gera("", "START", "", "")
                    gera("", "ALLOC", "0", "1")

                    analisa_bloco()

                    if Token.token_type == "sponto":
                        count = symbol_table.cut_stack()
                        dalloc_start_position = memory_position - count
                        gera("", "DALLOC", str(dalloc_start_position), str(count))

                        get_next_token()
                        if Token.token_type == "endfile":
                            print("Compilado com sucesso!")
                            with open("errorlog.txt", "a") as errorlog:
                                errorlog.write("\nCompilado com sucesso!\n\n")

                            symbol_table.print_stack()

                            gera("", "DALLOC", "0", "1")
                            gera("", "HLT", "", "")
                        else:
                            raise RuntimeError(
                                f"Símbolos inválidos após o fim do programa na linha: {lexer.get_current_line()}"
                            )
                    else:
                        raise RuntimeError(
                            f"Espera-se '.' na linha: {lexer.get_current_line()}"
                        )
                else:
                    raise RuntimeError(
                        f"Espera-se ';' na linha: {lexer.get_current_line()}"
                    )
            else:
                raise RuntimeError(
                    f"Espera-se 'identificador' na linha: {lexer.get_current_line()}"
                )
        else:
            raise RuntimeError(
                f"Erro de Sintaxe! Espera-se 'programa' na linha: {lexer.get_current_line()}"
            )

    except Exception as e:
        print(f"Erro: {e}")
        with open("errorlog.txt", "w") as errorlog:
            errorlog.write(f"Linha: {lexer.get_current_line()}\nErro: {e}\n")
        
        with open("gera2.obj", "w") as gera2:
            gera2.truncate()

    finally:
        print("Execução finalizada")


class SymbolInfo:
    def __init__(self, name, scope_level, type_, memory_address):
        self.name = name
        self.scope_level = scope_level
        self.type = type_
        self.memory_address = memory_address


class Node:
    def __init__(self, symbol_info):
        self.symbol_info = symbol_info
        self.next = None


class TabelaSimbolos:
    def __init__(self):
        self.top = None

    def push(self, name, scope_level, type_, memory_address):
        symbol_info = SymbolInfo(name, scope_level, type_, memory_address)
        new_node = Node(symbol_info)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is not None:
            temp = self.top
            self.top = self.top.next
            del temp  

    def is_empty(self):
        return self.top is None

    def peek(self):
        if self.top is not None:
            return self.top.symbol_info
        return None

    def contains_var(self, name):
        aux = self.top
        while aux is not None:
            if aux.symbol_info and aux.symbol_info.scope_level == "L":
                if aux.symbol_info.name == name:
                    return True
                break
            if aux.symbol_info and aux.symbol_info.name == name:
                return True
            aux = aux.next
        return False

    def contains(self, name):
        aux = self.top
        while aux is not None and aux.symbol_info is not None:
            if aux.symbol_info.name == name:
                return True
            aux = aux.next
        return False

    def cut_stack(self):
        count = 0
        while self.top is not None and self.top.symbol_info.scope_level != "L":
            if self.top.symbol_info.type in ["inteiro", "booleano"]:
                count += 1
            self.pop()
        if self.top is not None:
            self.top.symbol_info.scope_level = ""
        return count

    def assign_type_to_variables(self, new_type):
        current = self.top
        while current is not None:
            if current.symbol_info.type == "var":
                current.symbol_info.type = new_type
            current = current.next

    def assign_type_to_function(self, new_type):
        current = self.top
        while current is not None:
            if current.symbol_info.type == "function":
                current.symbol_info.type = new_type
            current = current.next

    def get_type(self, name):
        current = self.top
        while current is not None:
            if current.symbol_info.name == name:
                return current.symbol_info.type
            current = current.next
        return ""

    def get_address(self, name):
        current = self.top
        while current is not None:
            if current.symbol_info.name == name:
                return current.symbol_info.memory_address
            current = current.next
        return ""

    def is_procedure_or_program(self, name):
        current = self.top
        while current is not None:
            if (
                current.symbol_info.name == name
                and current.symbol_info.type in ["procedimento", "programa"]
            ):
                return True
            current = current.next
        return False

    def print_stack(self):
        current = self.top
        while current is not None:
            info = current.symbol_info
            print(
                f"Name: {info.name}, Scope Level: {info.scope_level}, "
                f"Type: {info.type}, Memory Address: {info.memory_address}"
            )
            current = current.next

    def to_postfix(self, input_tokens):
        operators = []
        output = []

        def precedence(op):
            if op in ["+u", "-u", "nao"]:
                return 5
            if op in ["*", "div"]:
                return 4
            if op in ["+", "-"]:
                return 3
            if op in ["=", "!=", "<", ">", "<=", ">="]:
                return 2
            if op == "e":
                return 1
            if op == "ou":
                return 0
            return -1

        def is_operator(token):
            return token in [
                "+", "-", "*", "div", "=", "!=", "<", ">", "<=", ">=", "nao", "e", "ou", "+u", "-u"
            ]

        for token in input_tokens:
            if not is_operator(token) and token not in ["(", ")"]:
                output.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                if operators:
                    operators.pop()
            elif is_operator(token):
                while (
                    operators
                    and operators[-1] != "("
                    and precedence(operators[-1]) >= precedence(token)
                ):
                    output.append(operators.pop())
                operators.append(token)

        while operators:
            output.append(operators.pop())

        return output



if __name__ == "__main__":
    main()
