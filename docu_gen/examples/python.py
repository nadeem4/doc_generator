CLASS_EXAMPLE = '''
                    class ExampleClass:
                        """
                        A class that represents an example.
                        """
                    '''
FUNCTION_EXAMPLE = '''
        def example_function(param1, param2):
            """
            Perform an example operation.

            Args:
                param1 (int): The first parameter.
                param2 (int): The second parameter.

            Returns:
                int: The result of the operation.

            Raises:
                ValueError: If invalid parameters are provided.
            """
            if param1 < 0 or param2 < 0:
                raise ValueError("Parameters must be non-negative.")
            return param1 + param2
        '''
