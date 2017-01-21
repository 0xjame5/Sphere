from glob import glob
import json

from clarifai.rest import ClarifaiApp

from settings import API_KEY_FILE, TRAIN_PATH

TRAIN_DATA_DIRS = glob(TRAIN_PATH + "/*")
concepts = []

with open(API_KEY_FILE) as api_key:

    api_key = json.load(api_key)

    app = ClarifaiApp(api_key["id"], api_key["secret"])

    print app.models.delete_all()

    for concept in TRAIN_DATA_DIRS:

        concepts.append(concept.split('/')[-1])

        for pic in glob(concept + "/*"):

            app.inputs.create_image_from_filename(
                filename=pic,
                concepts=[concept.split('/')[-1]]
            )

    model = app.models.create(model_id="faces", concepts=concepts)
    model = model.train()
