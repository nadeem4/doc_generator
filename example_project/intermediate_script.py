import json

class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_json(self):
        try:
            return json.dumps({'name': self.name, 'age': self.age})
        except TypeError as e:
            print(f"Error converting to JSON: {e}")
            return None

def load_people(file_path):
    try:
        with open(file_path, 'r') as file:
            people_data = json.load(file)
            return [Person(**data) for data in people_data]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading people from {file_path}: {e}")
        return []

if __name__ == '__main__':
    alice = Person('Alice', 30)
    print(alice.to_json())

    people = load_people('people.json')
    for person in people:
        print(f"{person.name} is {person.age} years old.")