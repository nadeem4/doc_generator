import math


def calculate_area(radius) -> int:
    return math.pi * radius**2


if __name__ == "__main__":
    r = 5
    area = calculate_area(r)
    print(f"The area of a circle with radius {r} is {area:.2f}")
