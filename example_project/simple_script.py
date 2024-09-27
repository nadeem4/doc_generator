import math


def calculate_area(radius) -> int:
    """Calculate the area of a circle given its radius.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle calculated using the formula math.pi * radius ** 2.

    Raises:
        None.
    """
    return math.pi * radius**2


if __name__ == "__main__":
    r = 5
    area = calculate_area(r)
    print(f"The area of a circle with radius {r} is {area:.2f}")
