class ThingDoer:
    """A class that initializes object attributes with given values and sets a default
    value for another attribute."""

    def __init__(self, x: int, y: int):
        """Initialize the object with given values for attributes a and b, and set
        attribute c to 0.

        Args:
            x (int): The value to assign to attribute a.
            y (int): The value to assign to attribute b.

        Returns:
            None

        Raises:
            None
        """
        self.a = x
        self.b = y
        self.c = 0

    def action1(self):
        """Perform action 1 by adding two attributes.

        Returns:
            int: The sum of attribute 'a' and attribute 'b'.

        Raises:
            TypeError: If 'a' or 'b' are not integers.
        """
        return self.a + self.b

    def action2(self):
        """Subtracts the value of attribute 'b' from attribute 'a'.

        Returns:
            int: The result of the subtraction operation.

        Raises:
            TypeError: If 'a' or 'b' are not integers.
        """
        return self.a - self.b

    def perform(self):
        """Perform the multiplication operation on the attributes a and b of the object.

        Returns:
            int or float: The result of multiplying the attributes a and b.

        Raises:
            TypeError: If the attributes a or b are not numeric types.
        """
        return self.a * self.b

    def another_action(self):
        """Perform another action by dividing a by b if b is not zero.

        Returns:
            float or None: The result of the division if b is not zero, otherwise None.

        Raises:
            None.
        """
        if self.b != 0:
            return self.a / self.b
        else:
            return None

    def do_something(self):
        """Calculate the power of 'a' raised to the power of 'b' and assign it to 'c'.

        Raises:
            None

        Returns:
            None
        """
        self.c = self.a**self.b

    def what_am_i_doing(self):
        """Print the values of attributes a, b, and c.

        This function prints the values of attributes a, b, and c of the object calling the method.

        Args:
            self: The object instance.

        Returns:
            None

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
