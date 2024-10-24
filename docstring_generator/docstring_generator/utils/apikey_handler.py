import os
import sys


# Base handler class
class APIKeyHandler:
    """A class that serves as a base handler for API key management."""

    def __init__(self, successor=None):
        """Initialize a new instance of the class.

        Args:
            successor (object, optional): The successor object to be assigned. Defaults to None.

        Raises:
            None

        Returns:
            None
        """
        self._successor = successor

    def handle(self):
        """Raise NotImplementedError with a message indicating that the 'handle' method
        must be implemented.

        Raises:
            NotImplementedError: Indicates that the 'handle' method must be implemented.
        """
        raise NotImplementedError("Must implement handle method.")
