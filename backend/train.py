from glob import glob
import json
from os import path

import cognitive_face as CF

from settings import API_KEY_FILE, TRAIN_PATH

TRAIN_DATA_DIRS = glob(TRAIN_PATH + "/*.zip")[0]


with open(API_KEY_FILE) as api_key:

    KEY = json.load(api_key)["key1"]
    CF.Key.set(KEY)

    img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    # result = CF.face_list.get("")
    CF.face_list.add_face(img_url, "id01")

    print(CF.face_list.get("id01"))
