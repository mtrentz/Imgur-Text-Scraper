# Imgur-Text Scraper

Generate valid random imgur urls, download them and run a OCR on all texts.

Also tries to find important info by running some regex patterns on all text detected. You can create regex to look for emails, phone-numbers, and even some possible crypto stuff posted. If something is found, it will save the image on separate folder for further analysis.

Saves the result on a SQLite3 database on /files/detected_text.db

## Requirements
This app uses both Golang, for downloading, and Python for the OCR part. You'll need EasyOCR (Pytorch) and also FastAPI for the python app. But its advised to run it with Docker.

## Getting started
Running it with docker-compose:
```
docker-compose build
docker-compose up
```

## Configs
There are some configurations possible.

If you want to change the amount of goroutines that will look for valid URLs you can change it on /downloader/main.go main function.

The same goes for the number of images to download before stop looking for it and the amount of digits on the imgur image identifier.

If you want to add new regex classifications you can do it on /analyser/regexes.py.

In case you have a GPU with cuda available, it's possible to start the easyOCR reader with
```
reader = easyocr.Reader(['en'], gpu=True)
```

## Files
All images are downloaded into /imgs.
The database is located in /files.

## Warning
Since the urls are randomly generated, there **WILL** be a good amount of NSFW images.
'
Running the program with a large amount of workers is a very good way of getting your IP blocked by imgur.
So don't make too many requests per second for an extended amount of time.
