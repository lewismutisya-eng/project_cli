import json
import os

def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except:
        return []

def save_data(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
