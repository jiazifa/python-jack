from lexer import Token, TokenType

_error_count: int = 0


def error_count() -> int:
    return _error_count


def syntax_error(filename: str, expected: str, token: Token):
    print("Error in class" + filename + "in line:"
          + str(token.row) + "expect a " + expected
          + ", but got a " + str(token.value) + "\n")


def class_diff_filename(filename: str):
    """ 类名与文件名不一致 """
    error_count += 1
    content = "Error in file " + filename + ".jack: " + \
        "classname should be same as filename" + "\n"
    print(content)
