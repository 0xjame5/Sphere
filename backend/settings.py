from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

API_KEY_FILE = path.join(path.dirname(BASE_DIR), "apis.json")

DB_PATH = path.join(path.dirname(BASE_DIR), "db")
