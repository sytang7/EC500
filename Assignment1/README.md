# MiniProgram1
## Aim
- Collect serveral image URLs from a certain twitter account by using Tweepy
- Download image from the URLS
- Convert all images to a video by using FFmpeg
- analyse all image and output labels by using Google Vision API

## Manual
1. pip install tweepy
2. pip install ffmpeg
3. authenticate to Google Cloud Vision API
4. Done!

## Code Review


This program run correctly. But still has some problem.


If the document has picture with png form, that wouldn’t be download.
This program change all of the picture to mp4 document, which make the speed slow.
If the twitter has no picture, this program no any feedback.
4.   Asynchronous, because you can count multiple images.

## Unittest
Test1 Fault test2.3 OK
Test1 for speed. Task 2 for download picture. Task 3 for label.txt

## Web for call function:
1.The HelloWorld document for this web and this use django. For run this document, install django and download the whole document.
2.In this document, use terminal to run: python manang.py runserver local5000
3. Get the website and open it with your chorm.
4. You can type in your twitter ID.
5. You will get the result at the HelloWorld document.
