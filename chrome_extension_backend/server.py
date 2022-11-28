from flask import Flask, request, render_template
import json
import numpy as np
import pickle
from tensorflow import keras
import urllib
import cv2

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
    with open('image.png', 'wb') as f:
        f.write(response.file.read())
    
    # Load the image and convert it to grayscale
    img = cv2.imread('image.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Add some extra padding around the image
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_REPLICATE)

    # threshold the image (convert it to pure black and white)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)[1]

    # find the contours (continuous blobs of pixels) the image
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    letter_image_regions = []

    # Now we can loop through each of the contours and extract the letter
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # checking if any counter is too wide
        # if countour is too wide then there could be two letters joined together or are very close to each other
        if w / h > 1.25:
            # Split it in half into two letter regions
            half_width = int(w / 2)
            letter_image_regions.append((x, y, half_width, h))
            letter_image_regions.append((x + half_width, y, half_width, h))
        else:
            letter_image_regions.append((x, y, w, h))
            

    
    # Sort the detected letter images based on the x coordinate to make sure
    # we get them from left-to-right so that we match the right image with the right letter  
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])
    
    # Creating an empty list for storing predicted letters
    predictions = []
    
    # Save out each letter as a single image
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]
        
        try:
          letter_image = cv2.resize(letter_image, (30,30))
          
          # Turn the single image into a 4d list of images
          letter_image = np.expand_dims(letter_image, axis=2)
          letter_image = np.expand_dims(letter_image, axis=0)

          # making prediction
          pred = model.predict(letter_image)
          
          # Convert the one-hot-encoded prediction back to a normal letter
          letter = lb.inverse_transform(pred)[0]
          predictions.append(letter)
        
        except:
          pass
        
    # joining predicted captcha's text
    captcha_text = "".join(predictions)

	# Return data in json format
    return json.dumps({"captcha_text": captcha_text})


if __name__ == "__main__":
	app.run(port=5001)
