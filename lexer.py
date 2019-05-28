from enum import Enum
from utils import VALID_SINGLE_SYMBOL

class TokenType(Enum):
    KEY_WORDS = 1,
    ID = 2,       # 标识符
    INT = 3,      # 整型数字
    BOOL = 4,     # 布尔类型
    CHAR = 5,     # 字符
    STRING = 6,   # 字符串
    SYMBOL = 7,   # 合法的符号
    NONE = 8,     # 无类型
    ERROR = 9,    # 错误
    ENDOFFILE = 10 # 文件结束

class Token:
    kind: TokenType
    value: str

    def __init__(self, kind: TokenType, value: any):
        self.kind = kind
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.val)
        )

    def __repr__(self):
        return self.__str__()

class Lexer:
    text: str
    pos: int
    current_char: str

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self._setupkeywords()
        self._setupsymbols()

    def error(self):
        raise Exception('Invalid character')

    def _setupkeywords(self):
        kind = TokenType.KEY_WORDS
        self._keywords = {}
        self._keywords["class"] = Token(kind, "class")
        self._keywords["class"] = Token(kind, "class")
        self._keywords["constructor"] = Token(kind, "constructor")
        self._keywords["function"] = Token(kind, "function")
        self._keywords["method"] = Token(kind, "method")
        self._keywords["field"] = Token(kind, "field")
        self._keywords["static"] = Token(kind, "static")
        self._keywords["int"] = Token(kind, "int")
        self._keywords["char"] = Token(kind, "char")
        self._keywords["boolean"] = Token(kind, "boolean")
        self._keywords["void"] = Token(kind, "void")
        self._keywords["true"] = Token(kind, "true")
        self._keywords["false"] = Token(kind, "false")
        self._keywords["this"] = Token(kind, "this")
        self._keywords["if"] = Token(kind, "if")
        self._keywords["else"] = Token(kind, "else")
        self._keywords["while"] = Token(kind, "while")
        self._keywords["return"] = Token(kind, "return")

    def _setupsymbols(self):
        kind = TokenType.SYMBOL
        self._symbols = {}
        self._symbols["{"] = Token(kind, "{")
        self._symbols["}"] = Token(kind, "}")
        self._symbols["("] = Token(kind, "(")
        self._symbols[")"] = Token(kind, ")")
        self._symbols["["] = Token(kind, "[")
        self._symbols["]"] = Token(kind, "]")
        self._symbols["."] = Token(kind, ".")
        self._symbols[","] = Token(kind, ",")
        self._symbols[";"] = Token(kind, ";")
        self._symbols["+"] = Token(kind, "+")
        self._symbols["-"] = Token(kind, "-")
        self._symbols["*"] = Token(kind, "*")
        self._symbols["/"] = Token(kind, "/")
        self._symbols["&"] = Token(kind, "&")
        self._symbols["|"] = Token(kind, "|")
        self._symbols["~"] = Token(kind, "~")
        self._symbols["<"] = Token(kind, "<")
        self._symbols[">"] = Token(kind, ">")
        self._symbols["="] = Token(kind, "=")

        self._symbols[">="] = Token(kind, ">=")
        self._symbols["<="] = Token(kind, "<=")
        self._symbols["=="] = Token(kind, "==")
        self._symbols["!="] = Token(kind, "!=")

    def _advance(self):
        self.pos += 1
        self._set_current_char()

    def _recede(self):
        self.pos -= 1
        self._set_current_char()
    
    def _set_current_char(self):
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _peek(self, n: int=1):
        num = self.pos + n
        if num > len(self.text) - 1:
            return None
        return self.text[num]

    def _skip_whitespace(self):
        while self.current_char is not None \
                and self.current_char.isspace():
            self._advance()

    def _skip_single_line_comment(self):
        comment = ""
        while self.current_char is not None \
                and self.current_char not in ["\r", "\n"]:
            comment += self.current_char
            self._advance()

    def _skip_comment_block(self):
        while self.current_char is not None:
            if self.current_char == "*" and self._peek() == "/": break
            self._advance()
    
    def _identifier(self):
        identifier: str = ""
        while self.current_char is not None \
            and (self.current_char.isalpha() \
            or self.current_char.isdigit() \
            or self.current_char == '_'):

            identifier += self.current_char
            self._advance()
        idf = self._keywords.get(identifier) or Token(TokenType.ID, identifier)
        return idf

    def _num(self):
        num: str = ""
        while self.current_char is not None and \
            (self.current_char.isdigit() or self.current_char == "."):
            num += self.current_char
            self._advance()
        assert num.isnumeric()
        return Token(TokenType.INT, num)

    def _logistic_symbol(self):
        symbol: str = ""
        while self.current_char is not None \
            and self.current_char in VALID_SINGLE_SYMBOL:
            symbol += self.current_char
            self._advance()
        token = self._symbols.get(symbol)
        if not token: self.error()
        return token

    def _string(self):
        string: str = ""
        self._advance()
        while self.current_char is not None:
            char: str = self.current_char
            if char != '"':
                string += char
                self._advance()
            else: break
        return Token(TokenType.STRING, string)

    def _char(self):
        char: str = ""
        self._advance()
        if char != '\\' or char != '\'':
            char += self.current_char
            self._advance()
        else: self.error()
        return Token(TokenType.CHAR, char)

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            char: str = self.current_char
            # 空格
            if char.isspace():
                self._skip_whitespace()
                continue

            if char.isalpha(): # 字符
                return self._identifier()

            if char.isdigit(): # 数字
                return self._num()

            # comment
            if char == "#":
                self._skip_single_line_comment()

            if char == "/":
                if self._peek() == "/":
                    self._skip_single_line_comment()
                elif self._peek() == "*":
                    self._skip_comment_block()

            # 符号
            if char in VALID_SINGLE_SYMBOL:
                return self._logistic_symbol()

            if char == '"':
                return self._string()
            
            if char == '\'':
                return self._char()

            return Token(TokenType.ENDOFFILE, None)

        return Token(TokenType.ERROR, None)