import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

from settings import API_KEY_FILE, DB_PATH

with open(API_KEY_FILE) as api_key:
    api_key = json.load(api_key)

    visual_recognition = VisualRecognitionV3(
        '2016-05-20', api_key=api_key["api_key"])

    with open(join(DB_PATH, 'meh.zip'), 'rb') as cars, \
            open(join(DB_PATH, 'meh2.zip'), 'rb') as trucks:
        print(
            json.dumps(
                visual_recognition.create_classifier(
                    'Cars vs Trucks',
                    cars_positive_examples=cars,
                    negative_examples=trucks), indent=2))

    with open(join(DB_PATH, 'subject15.normal.jpg'), 'rb') as image_file:
        print(
            json.dumps(
                visual_recognition.classify(images_file=image_file),
                indent=2
            )
        )
