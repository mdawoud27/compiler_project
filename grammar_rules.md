# Grammar Rules

1. `Program -> StmtList`

   - A program consists of a list of statements (StmtList)

2. `StmtList -> Stmt StmtList | ε`

   - A statement list can be either:
     - A statement followed by another statement list
     - Empty (ε represents empty/nothing)
   - This allows for zero or more statements

3. `Stmt -> AssignStmt | IfStmt`

   - A statement can be either:
     - An assignment statement
     - An if statement

4. `AssignStmt -> id = Expr ;`

   - An assignment statement consists of:
     - An identifier (variable name)
     - Equals sign
     - An expression
     - Semicolon
   - Example: `x = 5`;

5. `IfStmt -> if (Expr) { StmtList } else { StmtList }`

   - An if statement consists of:
     - The keyword "if"
     - A condition (expression) in parentheses
     - A block of statements in curly braces
     - The keyword "else"
     - Another block of statements
   - Example: `if (x) { y = 1; } else { y = 2; }`

6. `Expr -> Term ((+ | -) Term)\*`

   - An expression is:
     - A term
     - Optionally followed by + or - and another term, repeated any number of times
   - Example: `a + b - c`

7. `Term -> Factor ((* | /) Factor)*`

   - A term is:
     - A factor
     - Optionally followed by \* or / and another factor, repeated any number of times
   - Example: `a _ b / c`

8. `Factor -> num | id | (Expr)`

   - A factor can be:
     - A number
     - An identifier (variable)
     - An expression in parentheses
       Examples: `42`, `x`, `(a + b)`

This grammar defines a simple programming language that supports:

- Variable assignments
- If-else statements
- Basic arithmetic expressions
- Nested expressions with parentheses
- Proper operator precedence (\* and / before + and -)
