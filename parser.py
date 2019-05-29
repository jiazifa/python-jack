from enum import Enum
from lexer import Token, TokenType, Lexer

class NodeKind(Enum):
    NONE = 1,
    CLASS = 2,
    CLASS_VAR_DEC = 3,
    SUBROUTINE_DEC = 4,
    BASIC_DEC = 5,
    CLASS_TYPE = 6,
    NULL = 7,
    PARAM = 8,
    VAR_DEC = 9,
    ARRAY = 10,
    VAR = 11,
    IF_STATEMENT = 12,
    WHILE_STATEMENT = 13,
    CALL_EXPRESSION = 14,
    RETURN_STATEMENT = 15,
    CALL_STATEMENT = 16,
    BOOL_EXPRESSION = 17,
    FUNCTION_CALL = 18,
    CONSTRUCTOR_CALL = 19,
    COMPARE = 20,
    OPERATION = 21,
    BOOL = 22,
    ASSIGN = 23,
    SUBROUTINE_BODY = 24,
    BOOL_CONST = 25,
    NEGATIVE = 26,
    METHOD_CALL = 27,
    INT_CONST = 28,
    CHAR_CONST = 29,
    STRING_CONST = 30,
    KEY_WORD_CONST = 31,
    THIS = 32

class TreeNode:
    token: Token
    child: list # size = 5
    next_node: TreeNode
    kind: NodeKind
    
    def __init__(self):
        self.kind = NodeKind.NONE
        self.child = [None for _ in range(5)]
        self.token = Token(TokenType.NONE, "")
        self.next_node = TreeNode()


class Parser:
    _filenames: list
    _current_filename: str 
    _syntax_tree: TreeNode
    _lexer: Lexer
    _has_return: bool

    _buffer: list

    def __init__(self, filenames: list):
        self._filenames = filenames
        self._syntax_tree = None

        self._current_filename = None
        self._has_return = False

        self._buffer = []
        pass

    def load_token(self):
        """ 从缓冲区中取出一个token
        """
        if len(self._buffer) == 0:
            token = self._lexer.get_next_token()
            self._buffer.append(token)
        return self._buffer.pop(0)

    def store_token(self):
        """ 把上一次取出的token放入到缓冲区中
        """
        pass

    def get_full_name(self, name: str) -> str:
        fullname = str(self._current_filename) + "." + str(name)
        return fullname

    def get_caller_name(self, fullname: str) -> str:
        names = fullname.split(".")
        if len(names) > 0: names.pop(0)
        return "".join(names)

    def get_function_name(self, fullname: str) -> str:
        names = fullname.split(".")
        if len(names) > 0: names.pop(0)
        return "".join(names)

    def parse_variables(self):
        tree: TreeNode
        token = self.load_token()
        if token.kind != TokenType.ID:
            