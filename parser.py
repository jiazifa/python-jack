from enum import Enum
from lexer import Token, TokenType, Lexer
from error import syntax_error, class_diff_filename
from exprAST import ExprAST, UnaryOpAST, BinaryExprAST, \
    INTExprAST, FloatExprAST, VariableExprAST, EmptyExprAST, ClassExprAST


class Parser:
    _filenames: list
    _current_filename: str
    _syntax_tree: ExprAST
    _lexer: Lexer
    _has_return: bool
    _current_token: Token

    def __init__(self, filenames: list):
        self._filenames = filenames
        self._syntax_tree = None

        self._current_filename = None
        self._has_return = False

        self._lexer = Lexer(filenames[0])
        self._current_filename = self._lexer.filename
        self._current_token = self._lexer.get_next_token()

    def _eat(self, t: TokenType, contains: list = []):
        print(t, self._current_token)
        assert self._current_token.kind == t
        if len(contains) > 0:
            if self._current_token.value not in contains:
                syntax_error(self._current_filename, "one of {content}".format(
                    contains), self._current_token)
        self._current_token = self._lexer.get_next_token()

    def _get_full_name(self, name: str) -> str:
        fullname = str(self._current_filename) + "." + str(name)
        return fullname

    def _get_caller_name(self, fullname: str) -> str:
        names = fullname.split(".")
        if len(names) > 0:
            names.pop(0)
        return "".join(names)

    def _get_function_name(self, fullname: str) -> str:
        names = fullname.split(".")
        if len(names) > 0:
            names.pop(0)
        return "".join(names)

    def _parse_class(self) -> ClassExprAST:
        self._eat(TokenType.KEY_WORDS, ['class'])
        name = self._current_token
        self._eat(TokenType.ID)
        self._eat(TokenType.SYMBOL, ['{'])
        variables = self._parse_variable_declarations()

        classExpr = ClassExprAST(name, variables)
        self._eat(TokenType.SYMBOL, ["}"])
        return classExpr

    def _parse_variable_declarations(self) -> list:
        variables = []
        valid = ["static", "field"]
        while self._current_token.value in valid:
            variable = self._parse_variable_declaration()
            variables.append(variable)
        return variables

    def _parse_variable_declaration(self) -> VariableExprAST:
        valid = ["static", "field"]
        if self._current_token.kind == TokenType.KEY_WORDS \
             and self._current_token.value in valid:

            scope = self._current_token.value
            self._eat(TokenType.KEY_WORDS, valid)
            kind = self._current_token
            self._eat(TokenType.KEY_WORDS, ["int", "string", "boolean"])
            name = self._current_token
            self._eat(TokenType.ID)
            value = None
            if self._current_token.kind == TokenType.SYMBOL\
                 and self._current_token.value == "=":
                self._eat(TokenType.SYMBOL)
                value = self._current_token
                self._eat(value.kind)
            self._eat(TokenType.SYMBOL, [";"])
            return VariableExprAST(scope, kind.value, name, value)
        else:
            syntax_error(self._current_filename, "identifier", self._current_token)

    def _parse_function_list(self):
        pass

    def _parse_function(self):
        pass

    def expr(self) -> ExprAST:
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()
        while self._current_token.kind == TokenType.SYMBOL and self._current_token.value in ["+", "-"]:
            op = self._current_token
            self._eat(TokenType.SYMBOL, ["+", "-"])
            node = BinaryExprAST(op, node, self.term())
        return node

    def term(self) -> ExprAST:
        """
        term: factor ((MUL | DIV) factor) *
        """
        op = self.factor()
        while self._current_token.kind == TokenType.SYMBOL and self._current_token.value in ["*", "/"]:
            self._eat(TokenType.STRING, ["*", "/"])
            op = BinaryExprAST(self._current_token, op, self.factor())
        return op

    def factor(self) -> ExprAST:
        """factor : PLUS factor
               | MINUS factor
               | NUMBER
               | FLOAT
               | LPAREN expr RPAREN
               | variable
        """
        token = self._current_token
        if token.kind == TokenType.SYMBOL:
            if token.value in ["-", "+"]:
                self._eat(TokenType.SYMBOL, ["-", "+"])
                node = UnaryOpAST(token, self.factor())
                return node
            elif token.value == "(":
                self._eat(TokenType.SYMBOL, ["("])
                node = self.expr()
                self._eat(TokenType.SYMBOL, [")"])
                return node
        elif token.kind == TokenType.INT:
            if "." in token.value:
                self._eat(token.kind)
                node = FloatExprAST(token)
            else:
                self._eat(token.kind)
                node = INTExprAST(token)    
            return node
        return EmptyExprAST()

if __name__ == "__main__":
    filename = 'TestsJack/testParseClass.jack'
    parse = Parser([filename])
    binary: ExprAST = parse._parse_class()
    print(binary)
