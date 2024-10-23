import os
import sys


# Base handler class
class APIKeyHandler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self):
        raise NotImplementedError("Must implement handle method.")
