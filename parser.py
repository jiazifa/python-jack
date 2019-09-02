from enum import Enum
from lexer import Token, TokenType, Lexer
from error import syntax_error, class_diff_filename
from exprAST import *

class Parser:
    _filenames: list
    _current_filename: str
    _syntax_tree: ExprAST
    _lexer: Lexer
    _has_return: bool
    _current_token: Token
    _token_queue: list

    def __init__(self, filenames: list):
        self._filenames = filenames
        self._syntax_tree = None

        self._current_filename = None
        self._has_return = False
        self._token_queue = list()
        self._lexer = Lexer(filenames[0])
        self._current_filename = self._lexer.filename
        self._get_token()

    def _borrow(self) -> Token:
        """ 向前看一个 Token，将当前的 Token 推入队列中 """
        self._token_queue.append(self._current_token)
        self._current_token = self._lexer.get_next_token()
        return self._current_token

    def _repay(self):
        """ 归还前看的 Token，同时设置当前 Token """
        token = self._current_token
        self._current_token = self._token_queue.pop(-1)
        self._token_queue.insert(0, token)

    def _get_token(self):
        """ 统一管理 Token 的获取，如果存在前看，则优先处理 """
        if not self._token_queue:
            token = self._lexer.get_next_token()
            self._current_token = token
        else:
            token = self._token_queue.pop(0)
            self._current_token = token

    def _eat(self, t: TokenType, contains: list = []):
        # print("on eat " + str(t) + " cpmpare with current " + str(self._current_token))
        assert self._current_token.kind == t
        if len(contains) > 0:
            if self._current_token.value not in contains:
                syntax_error(self._current_filename, "one of {content}".format(
                    content=contains), self._current_token)
        self._get_token()

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
        functions = self._parse_function_list()

        classExpr = ClassExprAST(name, variables, functions)
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
                self._eat(TokenType.SYMBOL, ["="])
                value = self._current_token
                self._eat(value.kind)
            self._eat(TokenType.SYMBOL, [";"])
            return VariableExprAST(scope, kind.value, name, value)
        else:
            syntax_error(self._current_filename,
                         "identifier", self._current_token)

    def _parse_function_list(self):
        valid = ["function"]
        functions = []
        while self._current_token.value in valid:
            function = self._parse_function()
            functions.append(function)
        return functions

    def _parse_function(self) -> FunctionExprAST:
        valid = ["function"]
        self._eat(TokenType.KEY_WORDS, valid)
        return_type = self._current_token
        self._eat(TokenType.KEY_WORDS, [return_type.value])
        name = self._current_token
        self._eat(TokenType.ID, [name.value])
        variables = self._parse_function_var_decs()
        statements = self._parse_function_statements()
        return FunctionExprAST(name, name.value, return_type, variables, statements)

    def _parse_function_var_decs(self) -> list:
        variables = []
        self._eat(TokenType.SYMBOL, ["("])
        # variables
        while self._current_token.kind == TokenType.KEY_WORDS:
            variable = self._parse_function_var_dec()
            variables.append(variable)
        self._eat(TokenType.SYMBOL, [")"])
        return variables

    def _parse_function_var_dec(self) -> VariableExprAST:
        var_type = self._current_token
        self._eat(TokenType.KEY_WORDS, [var_type.value])
        var = self._current_token
        self._eat(TokenType.ID, [var.value])
        value = None
        if self._current_token.kind == TokenType.SYMBOL and self._current_token.value == "=":
            self._eat(TokenType.SYMBOL, ["="])
            value = self._current_token
        return VariableExprAST("", var_type.value, var, value)

    def _parse_function_statements(self) -> list:
        statements = []
        self._eat(TokenType.SYMBOL, ["{"])
        while self._current_token.value is not "}":
            statement = self._parse_statement()
            statements.append(statement)
        self._eat(TokenType.SYMBOL, ["}"])
        return statements

    def _parse_statement(self) -> ExprAST:
        """
        statement -> assign_statement
               | if_statement
               | while_statement
               | return_statement
               | call_statement ;
        """
        token = self._current_token
        statement = EmptyExprAST()
        if token.kind == TokenType.ID:
            borrowed = self._borrow()
            if borrowed.value == "=":
                # assign_statement
                self._repay()
                statement = self._parse_assignment_statement()
            elif borrowed.value in ["(", "."]:
                # call_statement
                self._repay()
                statement = self._parse_call_statement()
        elif token.kind == TokenType.KEY_WORDS and token.value == "return":
            statement = self._parse_return_statement()
        elif token.kind == TokenType.KEY_WORDS and token.value == "if":
            # if_statement
            statement = self._parse_if_statement()
        elif token.kind == TokenType.KEY_WORDS and token.value == "while":
            # while_statement
            statement = self._parse_while_statement()
        self._eat(TokenType.SYMBOL, [";"])
        return statement

    def _parse_return_statement(self) -> ReturnExprAST:
        self._eat(TokenType.KEY_WORDS, ["return"])
        if self._current_token.kind == TokenType.SYMBOL and self._current_token.value == ";":
            return ReturnExprAST(self._current_token, EmptyExprAST())
        else:
            return ReturnExprAST(self._current_token, self.expression())

    def _parse_if_statement(self) -> ExprAST:
        
        pass

    def _parse_while_statement(self) -> ExprAST:
        pass

    def _parse_assignment_statement(self) -> AssignExprAST:
        """
        assign_statement -> leftValue = expression ; 
        """
        token = self._current_token
        statement = EmptyExprAST()
        left = token
        self._eat(token.kind, [token.value])
        op = self._current_token
        self._eat(op.kind, [op.value])
        right = self.expression()
        statement = AssignExprAST(op, left, right)
        return statement

    def _parse_call_statement(self) -> CallExprAST:
        token = self._current_token
        name = token.value
        args = []
        kwargs = {}
        self._eat(token.kind)
        if self._current_token.kind == TokenType.SYMBOL and self._current_token.value == ".":
            self._eat(TokenType.SYMBOL, ["."])
        elif self._current_token.kind == TokenType.SYMBOL and self._current_token.value == "(":
            self._eat(TokenType.SYMBOL, ["("])
            while self._current_token.value is not ")" and self._current_token.kind is not TokenType.SYMBOL:
                args.append(self.expression())
        # logic
        self._eat(TokenType.SYMBOL, [")"])
        return CallExprAST(token, name, args, kwargs)

    def expression(self) -> ExprAST:
        """
        expression : term ((PLUS | MINUS) term)*
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
                node = self.expression()
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
        elif token.kind == TokenType.ID:
            self._eat(token.kind)
            return VariableExprAST(None, None, token, None)
        return EmptyExprAST()


if __name__ == "__main__":
    filename = 'TestsJack/testParseClass.jack'
    parse = Parser([filename])
    binary: ExprAST = parse._parse_class()
    print(binary)
