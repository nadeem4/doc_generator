from abc import ABC, abstractmethod
from datetime import datetime


class ComplexClass(ABC):
    """A class that represents a Person object with a name, age, and creation time."""

    class_variable = "I am a class variable"

    def __init__(self, name: str, age: int):
        """Initialize a Person object with a name, age, and creation time.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.

        Returns:
            None

        Raises:
            None
        """
        self._name = name
        self._age = age
        self._creation_time = datetime.now()

    def display_info(self):
        """Display information about the object.

        Prints the name and age attributes of the object.

        Args:
            self: The object instance.

        Returns:
            None

        Raises:
            No exceptions are raised.
        """
        print(f"Name: {self._name}, Age: {self._age}")

    @property
    def name(self):
        """Return the name attribute of the object.

        Returns:
            str: The name attribute of the object.

        Raises:
            None.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name attribute of an object.

        Args:
            value (str): The value to set as the name attribute.

        Raises:
            ValueError: If the provided value is not a string.
        """
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError("Name must be a string")

    @name.deleter
    def name(self):
        """Delete the value of the '_name' attribute.

        Raises:
            AttributeError: If the '_name' attribute does not exist.
        """
        del self._name

    @classmethod
    def class_method_example(cls):
        """Print a message indicating that this is a class method and display the value
        of a class variable.

        Args:
            cls (Class): An instance of the class containing the class variable to be displayed.

        Returns:
            None

        Raises:
            No exceptions are raised.
        """
        print(f"This is a class method. Class variable value: {cls.class_variable}")

    @staticmethod
    def static_method_example(param1: int, param2: int) -> int:
        """Perform addition of two integers.

        Args:
            param1 (int): The first integer parameter.
            param2 (int): The second integer parameter.

        Returns:
            int: The sum of param1 and param2.

        Raises:
            None.
        """
        return param1 + param2

    @abstractmethod
    def abstract_method(self):
        """Define an abstract method that must be implemented by subclasses.

        This method serves as a placeholder and should be overridden in subclasses to provide specific functionality.

        Raises:
            NotImplementedError: Always raised as this method is meant to be abstract and should not be called directly.
        """
        pass

    def __str__(self):
        """Return a string representation of the ComplexClass object.

        Returns:
            str: A string containing the name and age of the ComplexClass object.

        Raises:
            None
        """
        return f"ComplexClass(Name: {self._name}, Age: {self._age})"

    def __repr__(self):
        """Return a string representation of the ComplexClass object.

        Returns:
            str: A string representation of the object with its name and age.

        Raises:
            None
        """
        return f"ComplexClass(name={self._name!r}, age={self._age!r})"

    def __len__(self):
        """Return the length of the name attribute.

        Returns:
            int: The length of the name attribute.

        Raises:
            None
        """
        return len(self._name)

    def __call__(self):
        """Print information about an instance of ComplexClass when called.

        Prints the name and age of the instance of ComplexClass.

        Raises:
            No exceptions are raised.

        Returns:
            None.
        """
        print(
            f"Instance of ComplexClass called: {self._name} is {self._age} years old."
        )

    def generate_numbers(self, limit: int):
        """Generate numbers up to a specified limit.

        Args:
            limit (int): The upper limit up to which numbers will be generated.

        Yields:
            int: The next number in the sequence starting from 1 up to the specified limit.

        Raises:
            None.
        """
        for i in range(1, limit + 1):
            yield i

    def __enter__(self):
        """Context manager entry method.

        Returns:
            object: The context manager object itself.

        Raises:
            No exceptions are raised.
        """
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager.

        Args:
            self: The context manager instance.
            exc_type (type): The type of the exception raised, if any.
            exc_val (Exception): The exception instance raised, if any.
            exc_tb (traceback): The traceback object associated with the exception, if any.

        Returns:
            bool: True if the context manager exits successfully.

        Raises:
            No specific exceptions are raised within this method.
        """
        print("Exiting the context")
        if exc_type:
            print(f"Error: {exc_type}, {exc_val}")
        return True

    def overloaded_method(self, x=None, *args, **kwargs):
        """Perform an example operation.

        Args:
            self: The instance of the class.
            x (any, optional): The value to be processed. Defaults to None.
            *args (tuple): Additional positional arguments.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            str: A formatted string containing the provided value, additional positional arguments, and keyword arguments.

        Raises:
            No specific exceptions are raised.
        """
        if x is None:
            return "No value provided"
        return f"Value: {x}, Additional args: {args}, Kwargs: {kwargs}"

    def factorial(self, n: int) -> int:
        """Calculate the factorial of a given integer.

        Args:
            n (int): The integer for which the factorial is to be calculated.

        Returns:
            int: The factorial of the input integer.

        Raises:
            RecursionError: If the input integer is negative.
        """
        if n == 0:
            return 1
        else:
            return n * self.factorial(n - 1)


class SubComplexClass(ComplexClass):
    """```
    A class that represents a subcomplex entity.
    ```"""

    def abstract_method(self):
        """Print a message indicating that the abstract method is implemented in a
        subclass.

        This method serves as a placeholder for an abstract method that should be implemented in a subclass.

        Raises:
            NotImplementedError: This method is meant to be overridden in a subclass.
        """
        print("Abstract method implemented in SubComplexClass")


if __name__ == "__main__":
    complex_obj = SubComplexClass("John Doe", 30)
    complex_obj.display_info()
    print(complex_obj.name)
    complex_obj.name = "Jane Doe"
    print(complex_obj.name)
    SubComplexClass.class_method_example()
    result = SubComplexClass.static_method_example(5, 10)
    print(f"Static method result: {result}")
    print(str(complex_obj))
    print(repr(complex_obj))
    with complex_obj:
        print("Inside context block")
    print(complex_obj.overloaded_method(10, 20, 30, key="value"))
    print(f"Factorial of 5: {complex_obj.factorial(5)}")
    complex_obj()
    for num in complex_obj.generate_numbers(5):
        print(f"Generated number: {num}")
