examples = [
    '''
    def add_numbers(a: int, b: int) -> int:
        """
        Adds two integers.

        Parameters:
        -------------
            a (int): First integer.
            b (int): Second integer.

        Returns:
        -------------
            int: Sum of a and b.

        Raises:
        -------------
            TypeError: If a or b is not an integer.
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Both a and b must be integers.")
        return a + b

    ''',
    '''
    def greet_user(name, greeting="Hello"):
        """
        Generates a greeting message.

        Parameters:
        ------------
            name (str): User's name.
            greeting (str, optional): Greeting phrase. Defaults to "Hello".

        Returns:
        ---------
            str: Personalized greeting.

        Raises:
        ----------
            ValueError: If name is empty.
        """
        if not name:
            raise ValueError("Name cannot be empty.")
        return f"{greeting}, {name}!"

    ''',
    '''
    def divide(dividend: float, divisor: float) -> float:
        """
        Divides two floats.

        Parameters:
        -------------
            dividend (float): Number to divide.
            divisor (float): Number to divide by.

        Returns:
        ------------
            float: Result of division.

        Raises:
        ------------
            ZeroDivisionError: If divisor is zero.
            TypeError: If inputs are not floats.
        """
        if not isinstance(dividend, float) or not isinstance(divisor, float):
            raise TypeError("Both dividend and divisor must be floats.")
        if divisor == 0.0:
            raise ZeroDivisionError("Divisor cannot be zero.")
        return dividend / divisor
    ''',
    '''
    def log_event(event_type: str, message: str, timestamp: str = None) -> None:
        """
        Logs an event to a file.

        Parameters:
        --------------
            event_type (str): Type of event (e.g., "INFO", "ERROR").
            message (str): Event message.
            timestamp (str, optional): ISO 8601 timestamp. Defaults to current time.

        Returns:
        --------------
            None

        Raises:
        ---------------
            ValueError: If event_type or message is empty.
            TypeError: If inputs are not strings.
            IOError: If log file cannot be written.
        """
        import datetime

        if not isinstance(event_type, str) or not isinstance(message, str):
            raise TypeError("Event type and message must be strings.")
        if not event_type.strip() or not message.strip():
            raise ValueError("Event type and message cannot be empty.")
        
        if timestamp is None:
            timestamp = datetime.datetime.utcnow().isoformat()
        elif not isinstance(timestamp, str):
            raise TypeError("Timestamp must be a string.")
        
        log_entry = f"{timestamp} - {event_type.upper()}: {message}\n"
        
        try:
            with open("event_log.txt", "a") as log_file:
                log_file.write(log_entry)
        except IOError as e:
            raise IOError(f"Failed to write to log file: {e}")
    ''',
    '''
    def concatenate_strings(*args, separator=" "):
        """
        Concatenates multiple strings.

        Parameters:
        --------------
            *args (str): Strings to concatenate.
            separator (str, optional): Separator between strings. Defaults to space.

        Returns:
        --------------
            str: Concatenated string.

        Raises:
        --------------
            TypeError: If inputs are not strings.
        """
        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("All arguments must be strings.")
        if not isinstance(separator, str):
            raise TypeError("Separator must be a string.")
        return separator.join(args)

    '''
]

def get_examples():
    return '\n\n'.join(examples)