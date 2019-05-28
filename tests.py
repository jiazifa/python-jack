import unittest
from lexer import Lexer, TokenType, Token

class test_lexer(unittest.TestCase):

    def make_lexer(self, text: str):
        return Lexer(text)

    def test_token_id(self):
        content = "a"
        lexer = self.make_lexer(content)
        token = lexer.get_next_token()
        self.assertEqual(token.value, "a")
        self.assertEqual(token.kind, TokenType.ID)

    def test_token_keywords(self):
        targetType = TokenType.KEY_WORDS
        for value in ["class", "class", "constructor", "function", "method", "field", "static", "int", "char", "boolean", "void", "true", "false", "this", "if", "else", "while", "return"]:
            expectValue = content = value
            lexer = self.make_lexer(content)
            token = lexer.get_next_token()
            self.assertEqual(token.value, expectValue)
            self.assertEqual(token.kind, targetType)

        expectValue = content = "classType"
        content += "/**/"
        content += "//////"
        lexer = self.make_lexer(content)
        token = lexer.get_next_token()
        self.assertEqual(token.value, expectValue)
        self.assertEqual(token.kind, TokenType.ID)

    def test_token_symbols(self):
        targetType = TokenType.SYMBOL
        for value in ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "~", "<", ">", "=", ">=", "<=", "==", "!=",]:
            expectValue = content = value
            lexer = self.make_lexer(content)
            token = lexer.get_next_token()
            self.assertEqual(token.value, expectValue)
            self.assertEqual(token.kind, targetType)
    
    def test_token_num(self):
        targetType = TokenType.INT
        import random
        expectValue = content = str(random.randint(0, 1000))
        lexer = self.make_lexer(content)
        token = lexer.get_next_token()
        self.assertEqual(token.value, expectValue)
        self.assertEqual(token.kind, targetType)

    def test_token_string(self):
        targetType = TokenType.STRING
        import random
        expectValue = content = """ "test_values" """
        expectValue = "test_values"
        lexer = self.make_lexer(content)
        token = lexer.get_next_token()
        self.assertEqual(token.value, expectValue)
        self.assertEqual(token.kind, targetType)

    def test_token_char(self):
        targetType = TokenType.CHAR
        import random
        expectValue = content = """ 'C' """
        expectValue = "C"
        lexer = self.make_lexer(content)
        token = lexer.get_next_token()
        self.assertEqual(token.value, expectValue)
        self.assertEqual(token.kind, targetType)