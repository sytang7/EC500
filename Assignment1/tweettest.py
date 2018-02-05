#!/usr/bin/env python
# encoding: utf-8
import tweepy
import json
import urllib.request
import io
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import bigquery
import ffmpy
import os

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_all_tweets_image(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []    
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    alltweets.extend(new_tweets)  
    oldest = alltweets[-1].id - 1
    res = []
    filename = []
    while len(new_tweets) > 0:
        print(len(alltweets))
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        for status in new_tweets:
            if 'media' in status._json['entities']:
                res.append(status._json['entities']['media'][0]['media_url'])
                filename.append(status._json['id_str'])
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 100):
            break
        print("...%d tweets downloaded so far".format(len(alltweets)))
    return res, filename
 
def download_image(imageurl,filename):
    for url,name in zip(imageurl,filename):
        directory = "photo/" + name + '.jpg'
        urllib.request.urlretrieve(url, directory)


def vision_analysor(imageurl):
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = imageurl
    response = client.face_detection(image=image)
    faces = response.face_annotations

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

def convert_image_video(filename):
    file = open('photo/filenames.txt', 'w')
    for name in filename:
        inputfile = "photo/" + name + '.jpg'
        outputfile = "photo/" + name + '.mp4'
        cmd = "ffmpeg -loop 1 -i " + inputfile + " -c:a libfdk_aac -ar 44100 -ac 2 -vf \"scale='if(gt(a,16/9),1280,-1)\':\'if(gt(a,16/9),-1,720)\', pad=1280:720:(ow-iw)/2:(oh-ih)/2\" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 " + outputfile
        os.system(cmd)
        file.write("file \'" + name+'.mp4\'\n')    
    file.close()
    cmd = "ffmpeg -f concat -i photo/filenames.txt output.mp4"
    os.system(cmd)

       

if __name__ == '__main__':
    imageurls,filename = get_all_tweets_image("@NintendoAmerica")
    download_image(imageurls,filename)
    convert_image_video(filename)
    vision_analysor(imageurls)


