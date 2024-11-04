import json


class Person:
    """A class that represents a person with a name and age."""

    def __init__(self, name, age):
        """Initialize a Person object with a name and age.

        Args:
            name (str): The name of the person. It should be a non-empty string.
            age (int): The age of the person. It should be a non-negative integer.

        Raises:
            ValueError: If the age is negative or if the name is an empty string.

        Returns:
            None
        """
        self.name = name
        self.age = age

    def to_json(self):
        """Converts the object's attributes to a JSON string.

        This method serializes the attributes of the object, specifically the
        'name' and 'age' attributes, into a JSON formatted string.

        Returns:
            str: A JSON string representing the object attributes, including
            'name' and 'age'.

        Raises:
            TypeError: If there is an issue converting the object attributes
            to JSON, such as unsupported data types.
        """
        try:
            return json.dumps({"name": self.name, "age": self.age})
        except TypeError as e:
            print(f"Error converting to JSON: {e}")
            return None


def load_people(file_path):
    """Load people data from a JSON file and create Person objects.

    This function reads a JSON file specified by the `file_path` argument,
    decodes the JSON data, and creates a list of `Person` objects from the
    data contained in the file.

    Args:
        file_path (str): The path to the JSON file containing people data.

    Returns:
        list: A list of `Person` objects created from the data in the JSON file.

    Raises:
        IOError: If there is an issue with reading the file, such as the file
        not being found or lacking the necessary permissions.
        json.JSONDecodeError: If there is an issue with decoding the JSON
        data, such as invalid JSON format.
    """
    try:
        with open(file_path, "r") as file:
            people_data = json.load(file)
            return [Person(**data) for data in people_data]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading people from {file_path}: {e}")
        return []


if __name__ == "__main__":
    alice = Person("Alice", 30)
    print(alice.to_json())
    people = load_people("people.json")
    for person in people:
        print(f"{person.name} is {person.age} years old.")
