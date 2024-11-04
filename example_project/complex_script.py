from abc import ABC, abstractmethod
from datetime import datetime


class ComplexClass(ABC):
    """A class that represents a complex entity with a name and age."""

    class_variable = "I am a class variable"

    def __init__(self, name: str, age: int):
        """Initialize a Person object with a name, age, and creation time.

        Args:
            name (str): The name of the person. Must be a non-empty string.
            age (int): The age of the person. Must be a non-negative integer.

        Returns:
            None

        Raises:
            ValueError: If the name is an empty string or if the age is negative.
        """
        self._name = name
        self._age = age
        self._creation_time = datetime.now()

    def display_info(self):
        """Display information about the object.

        This method prints the name and age attributes of the object instance.

        Args:
            self: The object instance from which the name and age attributes are accessed.

        Returns:
            None: This method does not return any value.

        Raises:
            No exceptions are raised.
        """
        print(f"Name: {self._name}, Age: {self._age}")

    @property
    def name(self):
        """Return the name attribute of the object.

        This method retrieves the value of the name attribute, which is expected to be a string.

        Returns:
            str: The name attribute of the object.

        Raises:
            None: This method does not raise any exceptions.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name attribute of an object.

        This method assigns the provided value to the name attribute of the object. It ensures that the value is a string before setting it.

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

        This method removes the '_name' attribute from the instance. If the attribute does not exist, an exception will be raised.

        Raises:
            AttributeError: If the '_name' attribute does not exist on the instance.
        """
        del self._name

    @classmethod
    def class_method_example(cls):
        """Print a message indicating that this is a class method and display the value
        of a class variable.

        Args:
            cls (type): The class type that contains the class variable to be displayed.

        Returns:
            None

        Raises:
            No exceptions are raised.
        """
        print(f"This is a class method. Class variable value: {cls.class_variable}")

    @staticmethod
    def static_method_example(param1: int, param2: int) -> int:
        """Perform addition of two integers.

        This method takes two integer parameters and returns their sum. It is a static method that does not depend on any instance variables.

        Args:
            param1 (int): The first integer parameter.
            param2 (int): The second integer parameter.

        Returns:
            int: The sum of param1 and param2.

        Raises:
            None: This method does not raise any exceptions.
        """
        return param1 + param2

    @abstractmethod
    def abstract_method(self):
        """Define an abstract method that must be implemented by subclasses.

        This method serves as a placeholder and should be overridden in subclasses to provide specific functionality. It is intended to enforce a contract for subclasses, ensuring that they implement their own version of this method.

        Raises:
            NotImplementedError: Always raised as this method is meant to be abstract and should not be called directly. This exception indicates that the method must be implemented in a subclass.
        """
        pass

    def __str__(self):
        """Return a string representation of the ComplexClass object.

        This method provides a formatted string that includes the name and age attributes of the ComplexClass instance, allowing for easy identification and debugging of the object.

        Returns:
            str: A string containing the name and age of the ComplexClass object in the format "ComplexClass(Name: {name}, Age: {age})".

        Raises:
            None
        """
        return f"ComplexClass(Name: {self._name}, Age: {self._age})"

    def __repr__(self):
        """Return a string representation of the ComplexClass object.

        This method provides a formatted string that includes the name and age attributes of the ComplexClass instance, which can be useful for debugging and logging purposes.

        Returns:
            str: A string representation of the object, formatted as
            "ComplexClass(name=<name>, age=<age>)".

        Raises:
            None
        """
        return f"ComplexClass(name={self._name!r}, age={self._age!r})"

    def __len__(self):
        """Return the length of the name attribute.

        This method calculates and returns the number of characters in the
        name attribute of the instance.

        Returns:
            int: The length of the name attribute.

        Raises:
            None: This method does not raise any exceptions.
        """
        return len(self._name)

    def __call__(self):
        """Print information about an instance of ComplexClass when called.

        This method outputs the name and age of the instance of ComplexClass to the console.

        Returns:
            None: This method does not return any value.

        Raises:
            No exceptions are raised.
        """
        print(
            f"Instance of ComplexClass called: { self._name} is {self._age} years old."
        )

    def generate_numbers(self, limit: int):
        """Generate numbers up to a specified limit.

        This generator function yields consecutive integers starting from 1 up to the specified limit.

        Args:
            limit (int): The upper limit up to which numbers will be generated.
                         Must be a positive integer.

        Yields:
            int: The next number in the sequence starting from 1 up to the specified limit.

        Raises:
            ValueError: If the limit is less than 1.
        """
        for i in range(1, limit + 1):
            yield i

    def __enter__(self):
        """Enter the context for the context manager.

        This method is called when the execution flow enters the context of the
        context manager. It typically sets up any necessary resources or state
        required for the context.

        Returns:
            object: The context manager object itself, allowing for further
            operations within the context.

        Raises:
            No exceptions are raised.
        """
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager.

        This method is called when exiting a context managed by the context manager. It handles any exceptions that may have been raised within the context and performs necessary cleanup.

        Args:
            self: The context manager instance.
            exc_type (type): The type of the exception raised, if any. This will be `None` if no exception was raised.
            exc_val (Exception): The exception instance raised, if any. This will be `None` if no exception was raised.
            exc_tb (traceback): The traceback object associated with the exception, if any. This will be `None` if no exception was raised.

        Returns:
            bool: True if the context manager exits successfully, indicating that any necessary cleanup has been performed.

        Raises:
            No specific exceptions are raised within this method.
        """
        print("Exiting the context")
        if exc_type:
            print(f"Error: {exc_type}, {exc_val}")
        return True

    def overloaded_method(self, x=None, *args, **kwargs):
        """Perform an example operation that processes a value along with additional
        arguments.

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
                      Must be a non-negative integer.

        Returns:
            int: The factorial of the input integer. The factorial of 0 is defined as 1.

        Raises:
            RecursionError: If the input integer is negative, as factorial is not defined for negative integers.
        """
        if n == 0:
            return 1
        else:
            return n * self.factorial(n - 1)


class SubComplexClass(ComplexClass):
    """A class that represents a sub-complex structure or entity."""

    def abstract_method(self):
        """Print a message indicating that the abstract method is implemented in a
        subclass.

        This method serves as a placeholder for an abstract method that should be
        implemented in a subclass. It is intended to be overridden by subclasses
        to provide specific functionality.

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
