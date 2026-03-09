import json
import os

DB_FILE = "database.json"


def load_db():

    if not os.path.exists(DB_FILE):
        return {"files": []}

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


def file_exists(url):

    db = load_db()

    return url in db["files"]


def register_file(url):

    db = load_db()

    if url not in db["files"]:
        db["files"].append(url)

    save_db(db)