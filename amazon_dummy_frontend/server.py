from flask import Flask, render_template, send_file
import os
from random import randint

app = Flask(__name__)

@app.route('/')
def home():
    images = os.listdir(os.path.join(os.getcwd(), 'amazon_dummy_frontend', 'static', 'solved-captchas'))
    return render_template("Amazon.in.html", filename= images[randint(0, len(images)-1)])

if __name__ == "__main__":
	app.run(port=5000)
