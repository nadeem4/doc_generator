# string with different formatting options


def single_line_string_with_200_char():
    """Return a string consisting of 200 repetitions of the character 'a'.

    This function generates a string that is exactly 200 characters long, with each character being the lowercase letter 'a'.

    Returns:
        str: A string with a length of 200 characters, all being the character 'a'.
    """
    return "a" * 200


def multiline_string():
    """Return a multiline string.

    This function generates and returns a string that contains multiple lines of text.
    The string is formatted to include line breaks, making it suitable for scenarios
    where multiline text is required.

    Returns:
        str: A string with multiple lines.

    Example:
        >>> result = multiline_string()
        >>> print(result)
        This is a multiline string.
        It has multiple lines.
    """
    return """This is a multiline string.
It has multiple lines."""


def multiline_string_with_indentation():
    """Return a multiline string with indentation.

    This function generates a formatted multiline string that includes
    indented text across multiple lines.

    Returns:
        str: A multiline string containing text with indentation.

    Example:
        >>> result = multiline_string_with_indentation()
        >>> print(result)
        This is a multiline string.
            It has multiple lines with indentation.
    """
    return """This is a multiline string.
    It has multiple lines with indentation."""


def multiline_string_with_newline_escape():
    """Return a multiline string with newline escape characters.

    This function generates a string that contains multiple lines, where each line is separated by a newline escape character (`\n`). The string is formatted to demonstrate how newline characters can be used in Python strings.

    Returns:
        str: A multiline string with newline escape characters.

    Example:
        >>> result = multiline_string_with_newline_escape()
        >>> print(result)
        This is a multiline string.
        It has multiple lines with newline escape.
    """
    return "This is a multiline string.\nIt has multiple lines with newline escape."


def multiline_string_with_newline_escape_and_indentation():
    """Return a multiline string with newline escape and indentation.

    This function generates a formatted string that includes multiple lines,
    each separated by a newline escape character and indented for clarity.

    Returns:
        str: A multiline string with multiple lines separated by newline escape
        and indentation.

    Example:
        >>> result = multiline_string_with_newline_escape_and_indentation()
        >>> print(result)
        This is a multiline string.
            It has multiple lines with newline escape and indentation.
    """
    return "This is a multiline string.\n    It has multiple lines with newline escape and indentation."


def multiline_string_with_newline_escape_and_indentation_and_quotes():
    """Return a multiline string with newline escape, indentation, and quotes.

    This function generates a string that contains multiple lines, utilizes newline escape sequences for line breaks, demonstrates indentation using spaces, and includes both single and double quotes.

    Returns:
        str: A multiline string with the following characteristics:
            - Contains multiple lines.
            - Includes newline escape sequences.
            - Demonstrates indentation with spaces.
            - Contains single quotes ('') and double quotes ("").
    """
    return "This is a multiline string.\n    It has multiple lines with newline escape and indentation and quotes: 'single quotes' and \"double quotes\"."


def multiline_string_using_tuple():
    """Return a multiline string created using a tuple.

    This function constructs a multiline string by concatenating several lines
    together. The lines are defined as separate string literals and are joined
    together to form a single string.

    Returns:
        str: A multiline string created by joining multiple lines using a tuple.

    Example:
        >>> multiline_string_using_tuple()
        'This is a multiline string.\nIt has multiple lines using a tuple.'
    """
    return "This is a multiline string.\n" "It has multiple lines using a tuple."
