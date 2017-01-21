from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

API_KEY_FILE = path.join(path.dirname(BASE_DIR), "clarifai_api.json")

DB_PATH = path.join(path.dirname(BASE_DIR), "data")

DATA_PATH = path.join(path.dirname(BASE_DIR), "data")

TRAIN_PATH = path.join(DATA_PATH, "train")
TEST_PATH = path.join(DATA_PATH, "test")
