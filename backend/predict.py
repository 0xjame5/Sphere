from glob import glob
import json

from clarifai.rest import ClarifaiApp

from settings import API_KEY_FILE, TEST_PATH

TEST_DATA_DIRS = glob(TEST_PATH + "/*")
concepts = []

with open(API_KEY_FILE) as api_key:

    api_key = json.load(api_key)

    app = ClarifaiApp(api_key["id"], api_key["secret"])

    # get the face model
    model = app.models.get("faces")

    for concept in TEST_DATA_DIRS:

        # predict with the model
        json_data = dict(model.predict_by_filename(concept))

        outputs = (json_data["outputs"][0]["data"]["concepts"])

        recognized_user = max(outputs, key=lambda x: x["value"])["id"]

        print(recognized_user)
