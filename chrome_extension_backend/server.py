from flask import Flask, request, render_template
import json
import numpy as np
import pickle
from tensorflow import keras
import urllib


model = keras.models.load_model("captcha_extractor_model.hdf5")

with open("captcha_labels.pickle", "rb") as f:
    lb = pickle.load(f)

# Setup flask server
app = Flask(__name__)

# Setup url route which will calculate
# total sum of array.
@app.route('/solvecaptcha', methods = ['POST'])
def solve_char():
    data = request.get_json()

    response = urllib.request.urlopen(data['image'])
    with open('image.jpg', 'wb') as f:
        f.write(response.file.read())
    
    # letter_image = np.array(data['image'])
    # pred = model.predict(letter_image)

    # letter = lb.inverse_transform(pred)[0]
    # return json.dumps({"captcha_text": letter_image})

	# Return data in json format

if __name__ == "__main__":
	app.run(port=5001)
