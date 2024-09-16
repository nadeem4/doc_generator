
# Python Code Parser

## Overview

This Python Code Parser is designed to analyze Python code and extract useful metadata from it. The parser can retrieve information about functions, methods, classes, imports, constants, and parameter details. It also provides default values for parameters, whether explicitly defined in the code or inferred based on the parameter types (e.g., `int`, `str`, `Optional`, etc.).

### Key Features:
- **Imports Detection**: Captures both standard imports (e.g., `import os`) and from-imports (e.g., `from typing import List`).
- **Functions and Methods Parsing**: Extracts information such as parameter names, types, and default values (including inferred defaults if missing).
- **Classes and Methods Parsing**: Captures class definitions, including methods and constants within the class scope.
- **Constants Detection**: Identifies constants (uppercase variables) within functions, methods, and class bodies.
- **Exception Handling Detection**: Extracts exception handling information (`try-except` blocks) and raised exceptions within functions and methods.
- **Automatic Default Parameter Assignment**: If a required parameter does not have a default value, the parser will assign a sensible default based on the type annotation.
- **Type Annotation Support**: Extracts and returns the parameter types and return types (if available).

## Features

### 1. Imports Detection
- **Standard Imports**: Extracts imports of the form `import X` or `import X as Y`.
- **From Imports**: Captures imports of the form `from X import Y`.

### 2. Function and Method Parsing
- **Parameter Names and Types**: Captures the names and types of parameters, using Python type hints if available.
- **Default Values**: Retrieves default values for parameters and automatically assigns a default if not explicitly defined, based on the parameter type.
- **Return Types**: Extracts the return type of the function or method, if specified.
- **Docstrings**: Retrieves function/method docstrings, if present.
- **Exceptions**: Detects raised exceptions and handled exceptions within `try-except` blocks.

### 3. Class Parsing
- **Class Names**: Captures the class name and associated docstring.
- **Methods**: Captures all methods in a class and processes them similarly to standalone functions.
- **Constants**: Detects constants (uppercase variables) defined at the class level or within methods.

### 4. Constants Detection
- Identifies constants within the scope of functions, methods, and classes. Constants are defined as variables with names in uppercase.

## How It Works

The parser uses Python's `ast` module to traverse and analyze the Abstract Syntax Tree (AST) of the Python code. Each part of the code (functions, classes, imports, etc.) is parsed by specialized methods to extract relevant information.

The extracted data is returned in a structured format, which includes:
- Function/method names
- Parameter names, types, and default values
- Class names and associated methods
- Constants and their values
- Imports and their aliases
- Exceptions raised and handled

## Example Usage

Here's a simple example to demonstrate how the parser works:

### Input Code (Example)

```python
from typing import List, Optional

class SampleClass:
    CONSTANT_VALUE = 42

    def __init__(self, x: int, y: int = 5):
        self.x = x
        self.y = y

    def divide(self, z: float = 1.0) -> float:
        try:
            return self.x / z
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")

def sample_function(a: int, b: int = 0) -> int:
    return a + b

def function_without_defaults(x: int, y: Optional[str]) -> None:
    pass
```

### Output (Parsed Information)

```python
{
    'functions': [
        {
            'name': 'sample_function',
            'parameters': [
                {'name': 'a', 'type': 'int', 'default': 'None'},
                {'name': 'b', 'type': 'int', 'default': '0'}
            ],
            'return_type': 'int',
            'docstring': None,
            'raises': [],
            'constants': []
        },
        {
            'name': 'function_without_defaults',
            'parameters': [
                {'name': 'x', 'type': 'int', 'default': 'None'},
                {'name': 'y', 'type': 'Optional[str]', 'default': 'None'}
            ],
            'return_type': 'None',
            'docstring': None,
            'raises': [],
            'constants': []
        }
    ],
    'classes': [
        {
            'name': 'SampleClass',
            'docstring': None,
            'methods': [
                {
                    'name': '__init__',
                    'parameters': [
                        {'name': 'self', 'type': None, 'default': 'None'},
                        {'name': 'x', 'type': 'int', 'default': 'None'},
                        {'name': 'y', 'type': 'int', 'default': '5'}
                    ],
                    'return_type': None,
                    'docstring': None,
                    'raises': [],
                    'constants': []
                },
                {
                    'name': 'divide',
                    'parameters': [
                        {'name': 'self', 'type': None, 'default': 'None'},
                        {'name': 'z', 'type': 'float', 'default': '1.0'}
                    ],
                    'return_type': 'float',
                    'docstring': None,
                    'raises': [
                        'Catches: ZeroDivisionError',
                        'Raises: ValueError("Cannot divide by zero")'
                    ],
                    'constants': []
                }
            ],
            'constants': ['CONSTANT_VALUE: 42']
        }
    ],
    'imports': [
        {'module': 'typing.List', 'alias': 'List'},
        {'module': 'typing.Optional', 'alias': 'Optional'}
    ]
}
```

## Installation

To run the parser, you need to have Python 3.9+ installed on your machine. This ensures compatibility with the `ast.unparse()` method, which is used to convert parsed AST nodes back into readable code.

1. Clone this repository:
    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:
    ```bash
    cd python-code-parser
    ```

3. Run the parser on your Python code:
    ```bash
    python parser.py
    ```

## Usage

You can use the `parse_python_code()` function to parse a Python file or a code snippet. Here's an example of how to use the parser:

```python
# Sample Python code to parse
code = 