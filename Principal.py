class TokenType:
    SPROGRAMA = "sprograma"
    SINICIO = "sinicio"
    SFIM = "sfim"
    SPROCEDIMENTO = "sprocedimento"
    SFUNCAO = "sfuncao"
    SSE = "sse"
    SENTAO = "sentao"
    SSENAO = "ssenao"
    SENQUANTO = "senquanto"
    SFACA = "sfaca"
    SATRIBUICAO = "satribuicao"
    SESCREVA = "sescreva"
    SLEIA = "sleia"
    SVAR = "svar"
    SINTEIRO = "sinteiro"
    SBOOLEANO = "sbooleano"
    SIDENTIFICADOR = "sidentificador"
    SNUMERO = "snumero"
    SPONTO = "sponto"
    SPONTO_VIRGULA = "sponto_virgula"
    SVIRGULA = "svirgula"
    SABRE_PARENTESES = "sabre_parenteses"
    SFECHA_PARENTESES = "sfecha_parenteses"
    SMAIOR = "smaior"
    SMAIORIG = "smaiorig"
    SIG = "sig"
    SMENOR = "smenor"
    SMENORIG = "smenorig"
    SDIF = "sdif"
    SMAIS = "smais"
    SMENOS = "smenos"
    SMULT = "smult"
    SDIV = "sdiv"
    SE = "se"
    SOU = "sou"
    SNAO = "snao"
    SDOISPONTOS = "sdoispontos"
    SVERDADEIRO = "sverdadeiro"
    SFALSO = "sfalso"
    ENDFILE = "endfile"
    TOKEN_UNKNOWN = "TOKEN_UNKNOWN"


class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def get_type(self):

        return self.token_type

    def get_type_string(self):
        return self.token_type

    def get_lexeme(self):
        return self.lexeme

    def __repr__(self):
        return f"Token(lexeme='{self.lexeme}', type='{self.token_type}')"


LEXEMA_TO_TOKEN = {
    "programa": TokenType.SPROGRAMA,
    "inicio": TokenType.SINICIO,
    "fim": TokenType.SFIM,
    "procedimento": TokenType.SPROCEDIMENTO,
    "funcao": TokenType.SFUNCAO,
    "se": TokenType.SSE,
    "entao": TokenType.SENTAO,
    "senao": TokenType.SSENAO,
    "enquanto": TokenType.SENQUANTO,
    "faca": TokenType.SFACA,
    ":=": TokenType.SATRIBUICAO,
    "escreva": TokenType.SESCREVA,
    "leia": TokenType.SLEIA,
    "var": TokenType.SVAR,
    "inteiro": TokenType.SINTEIRO,
    "booleano": TokenType.SBOOLEANO,
    "identificador": TokenType.SIDENTIFICADOR,
    "numero": TokenType.SNUMERO,
    ".": TokenType.SPONTO,
    ";": TokenType.SPONTO_VIRGULA,
    ",": TokenType.SVIRGULA,
    "(": TokenType.SABRE_PARENTESES,
    ")": TokenType.SFECHA_PARENTESES,
    ">": TokenType.SMAIOR,
    ">=": TokenType.SMAIORIG,
    "=": TokenType.SIG,
    "<": TokenType.SMENOR,
    "<=": TokenType.SMENORIG,
    "!=": TokenType.SDIF,
    "+": TokenType.SMAIS,
    "-": TokenType.SMENOS,
    "*": TokenType.SMULT,
    "div": TokenType.SDIV,
    "e": TokenType.SE,
    "ou": TokenType.SOU,
    "nao": TokenType.SNAO,
    ":": TokenType.SDOISPONTOS,
    "verdadeiro": TokenType.SVERDADEIRO,
    "falso": TokenType.SFALSO,
}


def get_token(lexeme):
    token_type = LEXEMA_TO_TOKEN.get(lexeme, TokenType.TOKEN_UNKNOWN)
    return Token(token_type, lexeme)


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


class Lexical:
    def __init__(self, filename):
        self.filename = filename
        self.line = 1
        self.tokens = []
        try:
            self.source_file = open(filename, 'r')
        except FileNotFoundError:
            raise RuntimeError("Falha ao abrir arquivo")

    def __del__(self):
        if hasattr(self, 'source_file') and not self.source_file.closed:
            self.source_file.close()

    def analise(self):
        while True:
            self.del_espaco_comentario()
            ch = self.source_file.read(1)
            if not ch:
                self.tokens.append(Token("endfile", "endfile"))
                break
            self.source_file.seek(self.source_file.tell() - 1)
            token = self.get_next_token()
            self.tokens.append(token)

    def del_espaco_comentario(self):
        while True:
            ch = self.source_file.read(1)
            if not ch:
                break

            if ch == '{':
                open_line = self.line
                closed = False
                while True:
                    ch = self.source_file.read(1)
                    if not ch:
                        raise RuntimeError(f"Error: Comentario aberto na linha {open_line} não fechado")
                    if ch == '}':
                        closed = True
                        break
                    if ch == '\n':
                        self.line += 1
                if not closed:
                    raise RuntimeError(f"Error: Comentario aberto na linha {open_line} não fechado")
            elif ch.isspace():
                if ch == '\n':
                    self.line += 1
                continue
            else:
                self.source_file.seek(self.source_file.tell() - 1) 
                break

    def get_next_token(self):
        self.del_espaco_comentario()

        ch = self.source_file.read(1)
        if not ch: 
            return Token("endfile", "endfile")

        lexeme = ""

        if self.is_letter(ch):
            if ch == '_':
                raise RuntimeError(f"Identificadores não podem começar com '_'. Identificador inválido na linha: {self.line}")
            lexeme += ch
            while True:
                ch = self.source_file.read(1)
                if not ch or not (self.is_letter(ch) or self.is_digit(ch) or ch == '_'):
                    break
                lexeme += ch
            if ch:
                self.source_file.seek(self.source_file.tell() - 1) 

            keywords = {
                "programa": "sprograma", "se": "sse", "entao": "sentao", "senao": "ssenao",
                "enquanto": "senquanto", "faca": "sfaca", "inicio": "sinicio", "fim": "sfim",
                "escreva": "sescreva", "leia": "sleia", "var": "svar", "inteiro": "sinteiro",
                "booleano": "sbooleano", "verdadeiro": "sverdadeiro", "falso": "sfalso",
                "procedimento": "sprocedimento", "funcao": "sfuncao", "div": "sdiv",
                "e": "se", "ou": "sou", "nao": "snao"
            }
            if lexeme in keywords:
                return Token(keywords[lexeme], lexeme)
            else:
                return Token("sidentificador", lexeme)

        if self.is_digit(ch):
            lexeme += ch
            while True:
                ch = self.source_file.read(1)
                if not ch or not self.is_digit(ch):
                    break
                lexeme += ch
            if ch:
                self.source_file.seek(self.source_file.tell() - 1) 
            return Token("snumero", lexeme)

        if ch == ':':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("satribuicao", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("sdoispontos", lexeme)

        if ch == '<':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("smenorig", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("smenor", lexeme)

        if ch == '>':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("smaiorig", lexeme)
            self.source_file.seek(self.source_file.tell() - 1)
            return Token("smaior", lexeme)

        if ch == '!':
            lexeme += ch
            if self.source_file.read(1) == '=':
                lexeme += '='
                return Token("sdif", lexeme)
            raise RuntimeError(f"Error: Operador invalido '!' na linha: {self.line}")

        single_char_tokens = {
            ';': "sponto_virgula", '.': "sponto", ',': "svirgula", '(': "sabre_parenteses",
            ')': "sfecha_parenteses", '+': "smais", '-': "smenos", '*': "smult", '=': "sig"
        }
        if ch in single_char_tokens:
            return Token(single_char_tokens[ch], ch)

        raise RuntimeError(f"Simbolo desconhecido '{ch}' na linha: {self.line}")

    def is_letter(self, ch):

        return ch.isalpha()

    def is_digit(self, ch):

        return ch.isdigit()

    def get_tokens(self):

        return self.tokens

    def get_current_line(self):
        return self.line
