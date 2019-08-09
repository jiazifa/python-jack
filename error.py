from lexer import Token, TokenType

_error_count: int = 0

def syntax_error(filename: str, expected: str, token: Token):
    global _error_count
    _error_count += 1
    print("Error in class" + filename + "in line:"
          + str(token.row) + "expect a " + expected
          + ", but got a " + str(token.value) + "\n")


def class_diff_filename(filename: str):
    """ 类名与文件名不一致 """
    global _error_count
    _error_count += 1
    content = "Error in file " + filename + ".jack: " + \
        "classname should be same as filename" + "\n"
    print(content)


def error_RedeclareVar(currentClass: str, row: int, varType: str, name: str):
    """ 
    变量重定义
    """
    global _error_count
    _error_count += 1
    content = "Error in class {currentClass} in line {row} : redeclaration of '{varType}  {name} '".format(
        currentClass=currentClass,
        row=row,
        varType=varType,
        name=name
    )
    print(content)

def error_redeclareFunction(currentClass: str, varType: str, name: str):
    """ 
    方法重定义
    """
    global _error_count
    _error_count += 1
    content = "Error in class {currentClass} : redeclaration of '{varType}  {name} '".format(
        currentClass=currentClass,
        varType=varType,
        name=name
    )
    print(content)