from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/clarifai/upload_image")
def upload_image():
	pass

"""
WHAT DO WE NEED THE API TO DO?
WE NEED IT TO...:

Verify if a face exists and return the ID of the user

If not, we want to make the user upload to api and train the clarifai data
"""

if __name__ == "__main__":
    app.run(debug=True)