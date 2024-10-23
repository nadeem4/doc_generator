# string with different formatting options


def single_line_string_with_200_char():
    """Return a string consisting of 200 repetitions of the character 'a'.

    Returns:
        str: A string with a length of 200 characters, all being the character 'a'.
    """
    return "a" * 200


def multiline_string():
    """Return a multiline string.

    Returns:
        str: A string with multiple lines.
    """
    return """This is a multiline string.
It has multiple lines."""


def multiline_string_with_indentation():
    """Return a multiline string with indentation.

    Returns:
        str: A multiline string with multiple lines and indentation.
    """
    return """This is a multiline string.
    It has multiple lines with indentation."""


def multiline_string_with_newline_escape():
    """Return a multiline string with newline escape characters.

    Returns:
        str: A multiline string with newline escape characters.
    """
    return "This is a multiline string.\nIt has multiple lines with newline escape."


def multiline_string_with_newline_escape_and_indentation():
    """Return a multiline string with newline escape and indentation.

    Returns:
        str: A multiline string with multiple lines separated by newline escape and indentation.
    """
    return "This is a multiline string.\n    It has multiple lines with newline escape and indentation."


def multiline_string_with_newline_escape_and_indentation_and_quotes():
    """```python Return a multiline string with newline escape, indentation, and quotes.

    Returns:
        str: A multiline string with the following characteristics:
            - Contains multiple lines.
            - Includes newline escape sequences.
            - Demonstrates indentation with spaces.
            - Contains single quotes ('') and double quotes ("").
    ```
    """
    return "This is a multiline string.\n    It has multiple lines with newline escape and indentation and quotes: 'single quotes' and \"double quotes\"."


def multiline_string_using_tuple():
    """Return a multiline string created using a tuple.

    Returns:
        str: A multiline string created by joining multiple lines using a tuple.
    """
    return "This is a multiline string.\n" "It has multiple lines using a tuple."
