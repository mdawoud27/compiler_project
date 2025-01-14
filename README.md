# Compiler Project - Syntax Checker

## Project Overview

This project implements a simple **compiler/interpreter** with a graphical user interface for a basic programming language. The project demonstrates fundamental concepts of compiler design including _lexical analysis_, _syntax analysis_, and _error handling_.

## Features

### 1. Language Support

- Variable assignments
- Numeric literals (integers and floating-point numbers)
- String literals (both single and double quotes)
- Arithmetic operations (+, -, \*, /)
- If-else statements
- Comments (single-line comments with //)
- Nested expressions with proper operator precedence

### 2. Grammar Specification

```bash
Program    -> StmtList
StmtList   -> Stmt StmtList | ε
Stmt       -> AssignStmt | IfStmt
AssignStmt -> id = Expr ;
IfStmt     -> if (Expr) { StmtList } else { StmtList }
Expr       -> Term ((+ | -) Term)*
Term       -> Factor ((* | /) Factor)*
Factor     -> num | id | (Expr)
```

_For more information or explanation [check this](./grammar_rules.md)._

## Technical Implementation

The project is organized into several modules, each handling a specific aspect of the compiler:

### 1. Lexical Analysis (`lexer.py`)

- Converts source code into tokens
- Handles various token types:
  - Numbers (integers and floating-point)
  - Strings (single and double quoted)
  - Identifiers
  - Operators
  - Comments
  - Keywords

### 2. Syntax Analysis (`parser.py`)

- Implements recursive descent parsing
- Comprehensive error reporting
- Handles nested expressions and statements
- Implements operator precedence

### 3. Token Management (`token_types.py`)

- Defines token types and token class
- Manages token creation and properties

### 4. Syntax Highlighting (`syntax_highlighter.py`)

- Real-time syntax highlighting
- Color coding for different language elements
- Support for comments, strings, numbers, and keywords

### 5. GUI Implementation (`gui.py`)

- User-friendly interface
- Code editor with line numbers
- Real-time syntax highlighting
- Error display and feedback
- File operations (save/load)

## [Example Code](./example.txt)

```python
// This is a test program demonstrating all features
// Numbers, strings, and expressions

// 1. Basic assignments with different types
num1 = 42;        // Integer
num2 = 3.14159;   // Float
str1 = "Hello";   // Double quoted string
str2 = 'World';   // Single quoted string

// 2. Arithmetic expressions
result = num1 + num2 * 2;
x = (10 + 5) * 2;

// 3. Nested if statements
if (x) {
    y = y + 1;    // Increment
    z = x * (y + 2.5);  // Float arithmetic
} else {
    y = y - 1;    // Decrement
    z = x / 2;    // Division
}
```

## Error Handling

- Detailed error messages with line and column numbers
- Syntax error detection
- Type checking for operations
- Proper error recovery
- Visual feedback in the GUI

## Project Structure

The project is organized into the following files:

- `main.py`: Entry point of the application
- `token_types.py`: Token definitions and management
- `lexer.py`: Lexical analysis implementation
- `parser.py`: Syntax analysis implementation
- `syntax_highlighter.py`: Code highlighting functionality
- `gui.py`: GUI implementation

## Future Improvements

1. Symbol table implementation
2. Type checking system
3. Function definitions and calls
4. Loop constructs (while, for)
5. More data types
6. Code execution/interpretation
7. Enhanced error recovery
8. Code optimization
9. Intermediate code generation

## Running the Project

```bash
python3 main.py
```
