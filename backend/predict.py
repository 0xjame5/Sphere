import json

from clarifai.rest import ClarifaiApp

from settings import API_KEY_FILE


def predict(input_photo):

    with open(API_KEY_FILE) as api_key:

        api_key = json.load(api_key)

        app = ClarifaiApp(api_key["id"], api_key["secret"])

        # get the face model
        model = app.models.get("faces")

        # predict with the model
        json_data = dict(model.predict_by_base64(input_photo))
        outputs = json_data["outputs"][0]["data"]["concepts"]

        return max(outputs, key=lambda x: x["value"])["id"]
