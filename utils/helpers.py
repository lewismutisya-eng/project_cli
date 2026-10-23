import json


def load_data(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: {filepath} has bad data, starting with an empty list.")
        return []


def save_data(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
