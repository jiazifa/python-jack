from enum import Enum
from io import TextIOWrapper
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
    ENDOFFILE = 10  # 文件结束


class Token:
    kind: TokenType
    value: str
    row: int

    def __init__(self, kind: TokenType, value: str, row: int=-1):
        self.kind = kind
        self.value = value
        self.row = row

    def __str__(self):
        return 'Token({type}, {value}, {row})'.format(
            type=self.type,
            value=repr(self.val),
            row=str(self.row)
        )

    def __repr__(self):
        return self.__str__()


DEFAULT_KEY_WORDS = {
    "class": Token(TokenType.KEY_WORDS, "class"),
    "class": Token(TokenType.KEY_WORDS, "class"),
    "constructor": Token(TokenType.KEY_WORDS, "constructor"),
    "function": Token(TokenType.KEY_WORDS, "function"),
    "method": Token(TokenType.KEY_WORDS, "method"),
    "field": Token(TokenType.KEY_WORDS, "field"),
    "static": Token(TokenType.KEY_WORDS, "static"),
    "int": Token(TokenType.KEY_WORDS, "int"),
    "char": Token(TokenType.KEY_WORDS, "char"),
    "boolean": Token(TokenType.KEY_WORDS, "boolean"),
    "void": Token(TokenType.KEY_WORDS, "void"),
    "true": Token(TokenType.KEY_WORDS, "true"),
    "false": Token(TokenType.KEY_WORDS, "false"),
    "this": Token(TokenType.KEY_WORDS, "this"),
    "if": Token(TokenType.KEY_WORDS, "if"),
    "else": Token(TokenType.KEY_WORDS, "else"),
    "while": Token(TokenType.KEY_WORDS, "while"),
    "return": Token(TokenType.KEY_WORDS, "return"),
}

DEFAULT_SYMBOL_TABLE = {
    "{": Token(TokenType.SYMBOL, "{"),
    "}": Token(TokenType.SYMBOL, "}"),
    "(": Token(TokenType.SYMBOL, "("),
    ")": Token(TokenType.SYMBOL, ")"),
    "[": Token(TokenType.SYMBOL, "["),
    "]": Token(TokenType.SYMBOL, "]"),
    ".": Token(TokenType.SYMBOL, "."),
    ",": Token(TokenType.SYMBOL, ","),
    ";": Token(TokenType.SYMBOL, ";"),
    "+": Token(TokenType.SYMBOL, "+"),
    "-": Token(TokenType.SYMBOL, "-"),
    "*": Token(TokenType.SYMBOL, "*"),
    "/": Token(TokenType.SYMBOL, "/"),
    "&": Token(TokenType.SYMBOL, "&"),
    "|": Token(TokenType.SYMBOL, "|"),
    "~": Token(TokenType.SYMBOL, "~"),
    "<": Token(TokenType.SYMBOL, "<"),
    ">": Token(TokenType.SYMBOL, ">"),
    "=": Token(TokenType.SYMBOL, "="),
    ">=": Token(TokenType.SYMBOL, ">="),
    "<=": Token(TokenType.SYMBOL, "<="),
    "==": Token(TokenType.SYMBOL, "=="),
    "!=": Token(TokenType.SYMBOL, "!="),

    ";": Token(TokenType.SYMBOL, ";"),
}


class Lexer:
    current_char: str

    filename: str
    _alllines: list  # 所有行
    _linecount: int  # 行数
    _line_index: int  # 最近一行
    _char_index: int  # 字符索引
    _indexpath: (int, int)  # 字符索引

    def __init__(self, filename: str):
        self.filename = filename
        with open(filename, 'r') as f:
            self._alllines = f.readlines()
            self._linecount = len(self._alllines)

        self._line_index = 0
        self._char_index = 0
        self._indexpath = (0, 0)
        self.current_char = self._alllines[self._line_index][self._char_index]

        self._setupkeywords()
        self._setupsymbols()

    def _get_next_char(self):
        current_line = self._alllines[self._line_index]
        if self._char_index >= len(current_line):
            current_line = self._get_next_line()
            self._char_index = -1
        if not current_line:
            return None
        self._char_index += 1
        if self._char_index >= len(current_line):
            return None
        self.current_char = current_line[self._char_index]

    def _get_next_line(self):
        self._char_index = 0
        self._line_index += 1
        if self._line_index >= self._linecount:
            return None
        print("line: " + str(self._line_readable()) + "; content: " + self._alllines[self._line_index])
        return self._alllines[self._line_index]

    def error(self, content: str = ""):
        content: str = "Invalid character" + "line: " + \
            str(self._line_index) + "char" + str(self._char_index) + content
        raise Exception(content)

    def _setupkeywords(self):
        self._keywords = DEFAULT_KEY_WORDS

    def _setupsymbols(self):
        self._symbols = DEFAULT_SYMBOL_TABLE

    def _advance(self):
        self._get_next_char()

    def _peek(self, n: int = 1):
        return self._alllines[self._line_index][self._char_index + 1]

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
            if self.current_char == "*" and self._peek() == "/":
                break
            self._advance()

    def _identifier(self):
        identifier: str = ""
        while self.current_char is not None \
            and (self.current_char.isalpha()
                 or self.current_char.isdigit()
                 or self.current_char == '_'):
            identifier += self.current_char
            self._advance()
        idf = self._keywords.get(identifier) or Token(TokenType.ID, identifier)
        idf.row = self._line_readable()
        return idf

    def _num(self):
        num: str = ""
        while self.current_char is not None and \
                (self.current_char.isdigit() or self.current_char == "."):
            num += self.current_char
            self._advance()
        assert num.isnumeric()
        return Token(TokenType.INT, num, self._line_readable())

    def _logistic_symbol(self):
        symbol: str = ""
        while self.current_char is not None \
                and self.current_char in VALID_SINGLE_SYMBOL:
            symbol += self.current_char
            self._advance()
        token = self._symbols.get(symbol)
        if not token:
            self.error("symbol error")
        token.row = self._line_readable()
        return token

    def _string(self):
        string: str = ""
        self._advance()
        while self.current_char is not None:
            char: str = self.current_char
            if char != '"':
                string += char
                self._advance()
            else:
                break
        self._advance()
        return Token(TokenType.STRING, string, self._line_readable())

    def _char(self):
        char: str = ""
        self._advance()
        if char != '\\' or char != '\'':
            char += self.current_char
            self._advance()
        else:
            self.error()
        return Token(TokenType.CHAR, char, self._line_readable())

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            char: str = self.current_char
            # 空格
            if char.isspace():
                self._skip_whitespace()
                continue

            if char.isalpha():  # 字符
                return self._identifier()

            if char.isdigit():  # 数字
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

            return Token(TokenType.ENDOFFILE, None, self._line_index)

        return Token(TokenType.ERROR, None, self._line_index)

    def _line_readable(self):
        return self._line_index + 1
