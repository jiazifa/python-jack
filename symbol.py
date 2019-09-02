from enum import Enum
from exprAST import *
from parser import *
from error import *


class SymbolKind(Enum):
    STATIC = 1,
    FIELD = 2,
    ARG = 3,
    VAR = 4,
    FUNCTION = 5,
    METHOD = 6,
    CONSTRUCTOR = 7,
    NONE = 8


class SymbolInfo:
    _token: Token
    _type: str  # int, float, char, string
    _kind: SymbolKind  # kind : static, field, var, argument
    index: int
    _args: list

    def __init__(self, token:Token, symbolType: str, kind: SymbolKind, index: int):
        self._token = token
        self._type = symbolType
        self._kind = kind
        self.index = index
        self._args = list()

    def __str__(self):
        return "SymbolInfo({symbolType}, {kind}, {index}, {args})".format(
            symbolType=self._type,
            kind=self._kind,
            index=self.index,
            args=self._args
        )


class SymbolTable:
    _parser: Parser = None
    _static_index: int
    _field_index: int
    _arg_index: int
    _var_index: int
    _error_num: int
    _classIndex: dict  # {str: int} 从类名到数组索引
    _classTable: list  # [{str: SymbolInfo}] 类符号表数组, 将一直保留着不会被销毁
    _subroutineTable: dict  # 函数符号表
    _currentClassNumber: int  # 遍历语法树的时候, 保存当前类符号表数组索引
    _currentClass: str  # 遍历语法树的时候, 保存当前类名称

    def __init__(self, parser: Parser):
        # 初始化时
        self._parser = parser
        self._currentClassNumber = 0
        self._static_index = 0
        self._field_index = 0
        self._arg_index = 0
        self._var_index = 0
        self._error_num = 0
        self._classTable = []
        self._classIndex = {}
        self._subroutineTable = {}
        self._currentClass = ""

    def insertClassTable(self, expr: ExprAST):
        """ 
        类符号表的插入操作
        """
        if isinstance(expr, ClassExprAST):
            # 处理类
            temp: dict = {}
            self._classTable.append(temp)
            expr: ClassExprAST = expr
            self._currentClass = expr.name
            index: int = len(self._classTable)
            self._classIndex[self._currentClass] = index
            self._static_index = self._field_index = 0
            for var in expr._variables:
                if isinstance(var, VariableExprAST):
                    var: VariableExprAST = var
                    info: SymbolInfo
                    if var.scope == "field":
                        info = SymbolInfo(var.token, var.kind, SymbolKind.FIELD,
                                          self._field_index)
                        self._field_index += 1
                    elif var.scope == "static":
                        info = SymbolInfo(var.token, var.kind, SymbolKind.STATIC,
                                          self._static_index)
                        self._static_index += 1
                    print(temp)
                    if var.name in temp:
                        error_RedeclareVar(
                            self._currentClass, var.value.row, var.scope, var.name)
                        return
                    temp[var.name] = info
            for func in expr._functions:
                func: FunctionExprAST = func
                info: SymbolInfo
                info = SymbolInfo(func.token, "function", SymbolKind.FUNCTION, len(self._subroutineTable))
                for arg in func._variables:
                    arg: VariableExprAST = arg
                    info._args.append(arg.kind)
                name = func.name
                if name in temp:
                    error_redeclareFunction(self._currentClass, "function", name)
                    return
                temp[name] = info
                pass

    def insertSubroutineTable(self, expr: ExprAST):
        """  
        函数符号表的插入操作
        """
        pass

    def findSubroutineTable(self, funcName: str) -> SymbolInfo:
        """  
        函数符号表的查找操作
        """
        pass

    def findClassTable(self, className: str, funcName: str) -> SymbolInfo:
        """  
        类符号表的查找操作
        """
        pass

    def findClassIndex(self, className: str) -> bool:
        """  
        判断className是不是合法的类名
        """
        return self._classIndex[className] != None

    def getFieldNumber(self, className: str) -> int:
        """  
        获得属性数量
        """
        assert self.findClassIndex(className) == True
        classNum: int = self._classIndex.get(className)
        nfield = 0
        pass


if __name__ == "__main__":
    filename = 'TestsJack/testSymbolClass.jack'
    parser = Parser([filename])
    ast: ClassExprAST = parser._parse_class()
    table: SymbolTable = SymbolTable(parser)
    table.insertClassTable(ast)
    print(table._classTable)
