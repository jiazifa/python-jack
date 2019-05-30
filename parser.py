from enum import Enum
from lexer import Token, TokenType, Lexer
from error import syntax_error, class_diff_filename
from exprAST import ExprAST, UnaryOpAST, BinaryExprAST, \
    INTExprAST, FloatExprAST, VariableExprAST, EmptyExprAST

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

    def _eat(self, t: TokenType, contains: list=[]):
        print(t, self._current_token)
        assert self._current_token.kind == t
        if len(contains) > 0: assert self._current_token.value in contains
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
