import json
import os

def load_users(file_path='users.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_users(users, file_path='users.json'):
    with open(file_path, 'w') as f:
        json.dump(users, f)

def load_predictions(file_path='predictions.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_predictions(predictions, file_path='predictions.json'):
    with open(file_path, 'w') as f:
        json.dump(predictions, f)