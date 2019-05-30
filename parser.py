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

    def _eat(self, t: TokenType):
        print(t, self._current_token)
        assert self._current_token.kind == t
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
        token = self._current_token
        while token.kind == TokenType.SYMBOL and token.value in ["+", "-"]:
            op = token
            first = node
            self._eat(TokenType.SYMBOL)
            node = BinaryExprAST(op, first, self.term())
        return node

    def term(self) -> ExprAST:
        """
        term: factor ((MUL | DIV) factor) *
        """
        node = self.factor()
        token = self._current_token
        while token.kind == TokenType.SYMBOL and token.value in ["*", "/"]:
            op = token
            self._eat(op.kind)
            node = BinaryExprAST(op, node, self.factor())
        return node

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
                self._eat(TokenType.SYMBOL)
                node = UnaryOpAST(token, self.factor())
                return node
            elif token.value == "(":
                self._eat(TokenType.SYMBOL)
                node = self.expr()
                self._eat(TokenType.SYMBOL)
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
    filename = 'TestsJack/testParseExpr.jack'
    parse = Parser([filename])
    binary: ExprAST = parse.expr()
    print(binary)