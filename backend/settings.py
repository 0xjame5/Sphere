from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

API_KEY_FILE = path.join(path.dirname(BASE_DIR), "microsoft_api.json")

DB_PATH = path.join(path.dirname(BASE_DIR), "db")

DATA_PATH = path.join(path.dirname(BASE_DIR), "data")

TRAIN_PATH = path.join(DATA_PATH, "train")
