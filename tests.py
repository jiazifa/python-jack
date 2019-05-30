import unittest
from lexer import Lexer, TokenType, Token
from parser import Parser
from exprAST import ExprAST, UnaryOpAST, BinaryExprAST, \
    INTExprAST, FloatExprAST, VariableExprAST, EmptyExprAST


class test_lexer(unittest.TestCase):

    def make_lexer(self, filename: str):
        return Lexer(filename)

    def make_parse(self, filenames: list):
        return Parser(filenames)

    def test_token_id(self):
        filename = 'TestsJack/testTokenId.jack'
        lexer = self.make_lexer(filename)
        expects = [
            ("token_a", TokenType.ID),
            ("token_b", TokenType.ID),
            ("token_c", TokenType.ID),
        ]
        for e in expects:
            token = lexer.get_next_token()
            print(token)
            self.assertEqual(token.kind, e[1])
            self.assertEqual(token.value, e[0])

    def test_token_keywords(self):
        filename = 'TestsJack/testTokenKeywords.jack'
        lexer = self.make_lexer(filename)
        expects = [
            ("class", TokenType.KEY_WORDS),
            ("constructor", TokenType.KEY_WORDS),
            ("function", TokenType.KEY_WORDS),
            ("method", TokenType.KEY_WORDS),
            ("field", TokenType.KEY_WORDS),
            ("static", TokenType.KEY_WORDS),
            ("int", TokenType.KEY_WORDS),
            ("char", TokenType.KEY_WORDS),
            ("boolean", TokenType.KEY_WORDS),
            ("void", TokenType.KEY_WORDS),
            ("true", TokenType.BOOL),
            ("false", TokenType.BOOL),
            ("this", TokenType.KEY_WORDS),
            ("if", TokenType.KEY_WORDS),
            ("else", TokenType.KEY_WORDS),
            ("while", TokenType.KEY_WORDS),
            ("return", TokenType.KEY_WORDS),
        ]
        for e in expects:
            token = lexer.get_next_token()
            self.assertEqual(token.kind, e[1])
            self.assertEqual(token.value, e[0])

    def test_token_symbols(self):
        filename = 'TestsJack/testTokenSymbols.jack'
        lexer = self.make_lexer(filename)
        expects = [
            ("{", TokenType.SYMBOL),
            ("}", TokenType.SYMBOL),
            ("(", TokenType.SYMBOL),
            (")", TokenType.SYMBOL),
            ("[", TokenType.SYMBOL),
            ("]", TokenType.SYMBOL),
            (".", TokenType.SYMBOL),
            (",", TokenType.SYMBOL),
            (";", TokenType.SYMBOL),
            ("+", TokenType.SYMBOL),
            ("-", TokenType.SYMBOL),
            ("*", TokenType.SYMBOL),
            ("/", TokenType.SYMBOL),
            ("&", TokenType.SYMBOL),
            ("|", TokenType.SYMBOL),
            ("~", TokenType.SYMBOL),
            ("<", TokenType.SYMBOL),
            (">", TokenType.SYMBOL),
            ("=", TokenType.SYMBOL),
            (">=", TokenType.SYMBOL),
            ("<=", TokenType.SYMBOL),
            ("==", TokenType.SYMBOL),
            ("!=", TokenType.SYMBOL),
            (";", TokenType.SYMBOL),
        ]
        for e in expects:
            token = lexer.get_next_token()
            self.assertEqual(token.kind, e[1])
            self.assertEqual(token.value, e[0])

    def test_token_line(self):
        filename = 'TestsJack/testTokenLine.jack'
        lexer = self.make_lexer(filename)
        expects = [
            ("a", TokenType.ID, 2),
            ("k", TokenType.ID, 4),
            ("d", TokenType.ID, 6),
        ]
        for e in expects:
            token = lexer.get_next_token()
            self.assertEqual(token.kind, e[1])
            self.assertEqual(token.value, e[0])
            self.assertEqual(token.row, e[2])
    
    def test_parse_expr(self):
        filename = 'TestsJack/testParseExpr.jack'
        parse = self.make_parse([filename])
        binary: ExprAST = parse.expr()
        self.assertEqual(type(binary), BinaryExprAST)