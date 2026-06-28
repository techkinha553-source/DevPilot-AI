import json
from pathlib import Path

DATA_FILE = Path("data/users.json")

if not DATA_FILE.exists():
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text("{}")

with open(DATA_FILE, "r") as f:
    users = json.load(f)

user_stats = {}

def save_users():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)