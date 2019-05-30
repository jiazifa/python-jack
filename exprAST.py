from lexer import Token, TokenType


class ExprAST:

    def __repr__(self):
        return self.__str__()


class EmptyExprAST(ExprAST):

    def __init__(self):
        pass


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
    value: str = None

    def __init__(self, token: Token):
        assert token.kind == TokenType.ID
        self.value = token.value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            VariableAST(4)
        """
        return 'VariableAST({value})'.format(
            value=self.value
        )
