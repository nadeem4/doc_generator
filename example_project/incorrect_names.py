class ThingDoer:
    """A class that performs actions based on the provided input values."""

    def __init__(self, x: int, y: int):
        """Initialize the object with given values for attributes a and b, and set
        attribute c to 0.

        Args:
            x (int): The value to assign to attribute a.
            y (int): The value to assign to attribute b.

        Returns:
            None: This method does not return a value.

        Raises:
            None: This method does not raise any exceptions.
        """
        self.a = x
        self.b = y
        self.c = 0

    def action1(self):
        """Perform action 1 by adding two attributes.

        This method calculates the sum of the instance attributes 'a' and 'b'.
        It is expected that both attributes are integers.

        Returns:
            int: The sum of attribute 'a' and attribute 'b'.

        Raises:
            TypeError: If either 'a' or 'b' are not integers.
        """
        return self.a + self.b

    def action2(self):
        """Subtracts the value of attribute 'b' from attribute 'a'.

        This method performs a subtraction operation using the instance attributes 'a' and 'b'. It is expected that both attributes are integers.

        Returns:
            int: The result of the subtraction operation, calculated as 'a - b'.

        Raises:
            TypeError: If either 'a' or 'b' are not integers.
        """
        return self.a - self.b

    def perform(self):
        """Perform the multiplication operation on the attributes `a` and `b` of the
        object.

        This method multiplies the two attributes `a` and `b`, which are expected to be numeric types (either integers or floats). The result of the multiplication is returned.

        Returns:
            int or float: The result of multiplying the attributes `a` and `b`.

        Raises:
            TypeError: If the attributes `a` or `b` are not numeric types (e.g., if they are strings or None).
        """
        return self.a * self.b

    def another_action(self):
        """Perform another action by dividing `a` by `b` if `b` is not zero.

        Returns:
            float or None: The result of the division if `b` is not zero; otherwise, returns None.

        Raises:
            None: This function does not raise any exceptions.
        """
        if self.b != 0:
            return self.a / self.b
        else:
            return None

    def do_something(self):
        """Calculate the power of 'a' raised to the power of 'b' and assign the result
        to 'c'.

        This method computes the value of `self.a` raised to the power of `self.b` and stores the result in `self.c`. It is assumed that `self.a` and `self.b` are already defined as attributes of the class instance.

        Returns:
            None: This method does not return a value; it modifies the instance attribute `self.c`.

        Raises:
            TypeError: If `self.a` or `self.b` are not of a numerical type (e.g., int or float).
            ValueError: If `self.a` or `self.b` are complex numbers, as this operation is not defined for them.
        """
        self.c = self.a**self.b

    def what_am_i_doing(self):
        """Print the values of attributes a, b, and c.

        This method prints the values of the attributes `a`, `b`, and `c` of the object instance that calls the method.

        Args:
            self: The object instance from which the method is called. It is expected to have attributes `a`, `b`, and `c`.

        Returns:
            None: This method does not return any value.

        Raises:
            No exceptions are raised.
        """
        print(f"Values are: a={self.a}, b={self.b}, c={self.c}")


if __name__ == "__main__":
    obj = ThingDoer(10, 5)
    print(f"Action1 result (should add): {obj.action1()}")
    print(f"Action2 result (should subtract): {obj.action2()}")
    print(f"Perform result (should multiply): {obj.perform()}")
    print(f"Another action result (should divide): {obj.another_action()}")
    obj.do_something()
    obj.what_am_i_doing()
