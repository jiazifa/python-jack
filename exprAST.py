from lexer import Token, TokenType


class ExprAST:

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        raise Exception


class EmptyExprAST(ExprAST):

    def __init__(self):
        pass

    def __str__(self):
        return "EmptyExprAST()"


class UnaryOpAST(ExprAST):
    """ 一元运算符 """
    op: Token = None

    def __init__(self, token: Token, expr: ExprAST):
        assert token.kind == TokenType.SYMBOL
        self.token = token
        self.expr = expr

    def __str__(self):
        """String representation of the class instance.
        Examples:
            UnaryOpAST("-", 4)
        """
        return 'UnaryOpAST({token}, {value})'.format(
            token=self.token,
            value=self.expr
        )


class BinaryExprAST(ExprAST):
    op: Token = None

    lhs: ExprAST = EmptyExprAST()
    rhs: ExprAST = EmptyExprAST()

    def __init__(self, op: Token, lhs: ExprAST, rhs: ExprAST):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "BinaryExprAST({lhs}, {op}, {rhs})".format(
            lhs=self.lhs,
            op=self.op,
            rhs=self.rhs
        )

class AssignExprAST(ExprAST):
    op: Token = None
    lhs: ExprAST = EmptyExprAST()
    rhs: ExprAST = EmptyExprAST()

    def __init__(self, op: Token, lhs: ExprAST, rhs: ExprAST):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "AssignExprAST({lhs}, {op}, {rhs})".format(
            lhs=self.lhs,
            op=self.op,
            rhs=self.rhs
        )

class INTExprAST(ExprAST):
    value: int = 0

    def __init__(self, token: Token):
        assert token.kind == TokenType.INT
        value = token.value
        self.value = int(value)

    def __str__(self):
        """String representation of the class instance.
        Examples:
            INTAST(4)
        """
        return 'INTAST({value})'.format(
            value=self.value
        )


class FloatExprAST(ExprAST):
    value: float = 0.0

    def __init__(self, token: Token):
        assert token.kind == TokenType.INT
        value = token.value
        self.value = float(value)

    def __str__(self):
        """String representation of the class instance.
        Examples:
            FloatAST(4)
        """
        return 'FloatAST({value})'.format(
            value=self.value
        )


class VariableExprAST(ExprAST):
    scope: str = None
    name: str = None
    kind: str = None
    value: Token = None

    def __init__(self, scope: str, kind: str, name: Token, value: Token):
        assert name.kind == TokenType.ID
        self.scope = scope
        self.name = name.value
        self.kind = kind
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            VariableAST(4)
        """
        return 'VariableAST({scope}, {kind}, {name}, {value})'.format(
            scope=self.scope,
            kind=self.kind,
            name=self.name,
            value=self.value
        )


class FunctionExprAST(ExprAST):
    name: str = None
    return_type: Token
    _variables: list = []
    statements: list = []

    def __init__(self, name: str, return_type: Token, variables: list, statements: list):
        self.name = name
        self.return_type = return_type
        self._variables = variables
        self.statements = statements

    def __str__(self):
        return "FunctionExprAST({name}, {return_type}, {variables}, {statements})".format(
            name=self.name,
            return_type=self.return_type,
            variables=self._variables,
            statements=self.statements
        )


class ClassExprAST(ExprAST):
    name: str = None
    _variables: list = []
    _functions: list = []

    def __init__(self, name: Token, variables: list, functions: list):
        self.name = name.value
        assert name.kind == TokenType.ID
        self._variables = variables
        self._functions = functions

    def __str__(self):
        return "ClassExprAST({name}, {variables}, {functions})".format(
            name=self.name, 
            variables=self._variables,
            functions=self._functions
            )

class CallExprAST(ExprAST):
    target: str = None
    args: list = []
    kwargs: dict = {}

    def __init__(self, target: str, args: list, kwargs: dict):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return "CallExprAST({target}, {args}, {kwargs})".format(
            target=self.target, 
            args=self.args,
            kwargs=self.kwargs
            )

class ReturnExprAST(ExprAST):
    value: ExprAST
    def __init__(self, value: ExprAST):
         self.value = value
        
    def __str__(self):
        return "ReturnExprAST({value})".format(
            value=self.value
            )
