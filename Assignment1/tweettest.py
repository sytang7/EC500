#!/usr/bin/env python
# encoding: utf-8
import tweepy
import json
import urllib.request
import io
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import bigquery
import os



def get_all_tweets_imageurls(screen_name = "@NintendoAmerica", Num = 100):    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)



    alltweets = []    
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    alltweets.extend(new_tweets)  
    oldest = alltweets[-1].id - 1
    imageurls = []
    filenames = []
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        for status in new_tweets:
            if 'media' in status._json['entities']:
                imageurls.append(status._json['entities']['media'][0]['media_url'])
                filenames.append(status._json['id_str'])
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > Num):
            print("Got {} images from {} so far".format(len(imageurls),screen_name))
            break
        
    return imageurls, filenames
 
def download_image(imageurls,filenames):
    if os.path.exists("photo/"):
        os.system('rm -rf photo/*')
    else:
        os.system('mkdir photo')
    for url,name in zip(imageurls, filenames):
        directory = "photo/" + name + '.jpg'
        urllib.request.urlretrieve(url, directory)
    print("Finish Downloading!")
    print("------------------------------------")


def vision_analysor(imageurls,filenames):
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    file = open('results.txt', 'w')
    for url,name in zip(imageurls,filenames):
        image.source.image_uri = url
        response = client.label_detection(image=image)
        labels = response.label_annotations
        file.write('Labels for {}:\n'.format(name))
        for label in labels:
            file.write(label.description + "\n")
        file.write('-----------------------------------------\n')

def convert_image_video(filenames, outputname = 'output.mp4'):
    file = open('photo/filenames.txt', 'w')
    for name in filenames:
        inputfile = "photo/" + name + '.jpg'
        outputfile = "photo/" + name + '.mp4'
        cmd = "ffmpeg -loop 1 -i " + inputfile + " -c:a libfdk_aac -ar 44100 -ac 2 -vf \"scale='if(gt(a,16/9),1280,-1)\':\'if(gt(a,16/9),-1,720)\', pad=1280:720:(ow-iw)/2:(oh-ih)/2\" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 " + outputfile
        os.system(cmd)
        file.write("file \'" + name +'.mp4\'\n')    
    file.close()

    cmd = "ffmpeg -f concat -i photo/filenames.txt " + outputname
    os.system(cmd)       

if __name__ == '__main__':
    imageurls,filenames = get_all_tweets_imageurls("@NintendoAmerica",100)
    download_image(imageurls,filenames)
    convert_image_video(filenames,'output.mp4')
    vision_analysor(imageurls,filenames)
    print("All done!")

