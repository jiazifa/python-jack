# python-jack
jack  in python


## 状态转移图

```
program -> classlist
    classlist -> classlist class
               | class
    class -> class ID { classVarDecList subroutineDecList }
    classVarDecList -> classVarDecList classVarDec
             	     |
    classVarDec -> static type varNameList ;
                 | field type varNameList ;
    varNameList -> varNameList , ID
                 | ID
    type -> int
          | float
          | char
          | boolean
          | void
          | ID
    subroutineDecList -> subroutineDecList subroutineDec
                       | 
    subroutineDec -> constructor type ID ( params ) subroutineBody
                   | function type ID ( params ) subroutineBody
                   | method type ID (params ) subroutineBody
    params -> paramList
            | 
    paramList -> paramList , param
               | param
    param -> type ID
    subroutineBody -> { varDecList statements }
    varDecList -> varDecList varDec
                | 
    varDec -> type varNameList ;
    statements -> statements statement
                | 
    statement -> assign_statement
               | if_statement
               | while_statement
               | return_statement
               | call_statement ;
    assign_statement -> leftValue = expression ; 
    leftValue -> ID
               | ID [ expression ]
    if_statement -> if ( expression ) statement
                  | if ( expression ) statement else statement
    while_statement -> while ( expression ) { statement }
    return_statement -> return ; 
                      | return expression ;
    call_statement -> ID ( expressions ) 
                    | ID . ID ( expressions )
    expressions -> expression_list
                 | 
    expression_list -> expression_list , expression
                     | expression
    expression -> expression & boolExpression
                | expression | boolExpression
                | boolExpression
    boolExpression -> additive_expression relational_operator additive_expression
                    | additive_expression
    relational_operator -> <= 
                         | >=
                         | ==
                         | <
                         | >
                         | !=
    additive_expression -> additive_expression + term
                         | additive_expression – term
                         | term    
    term -> term * factor
          | term / factor
          | factor
    factor -> - positive_factor
            | positive_factor
    positive_factor -> ~ not_factor
                     | not_factor
    not_factor -> INT_CONST
                | CHAR_CONST
                | STRING_CONST
                | keywordConstant
                | ID
                | ID [ expression ]
                | call_expression
                | ( expression )
    keywordConstant -> true
                     | false
                     | null
                     | this
    call_expression -> ID ( expression )
                     | ID . ID ( expression )

```