from flask import Flask
import tweettest
import os
from flask import render_template  
app = Flask(__name__)


@app.route("/")
def run():
    imageurls,filenames = tweettest.get_all_tweets_imageurls("@NintendoAmerica",100)
    tweettest.download_image(imageurls,filenames)
    os.system('rm -rf static/output.mp4')
    tweettest.convert_image_video(filenames,'static/output.mp4')
    #change this environment variable to yours
    tweettest.vision_analysor(imageurls,filenames,'ec500assignment1-e6358f3d9bbd.json')
    return render_template('index.html',imageurls = imageurls)