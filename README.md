# Imgur-Text Scraper

Generate valid random imgur urls, download them and run a OCR on all texts.

Saves the result on a SQLite3 database on /files/detected_text.db

## Requirements
This app uses both Golang, for downloading, and Python for the OCR part. You'll need EasyOCR (Pytorch) and also FastAPI for the python app. But its advised to run it with Docker.

## Getting started
Running it with docker-compose:
```
docker-compose build
docker-compose up
```

## Warning
Since the urls are randomly generated, there **WILL** be a good amount of NSFW images.

Running the program with a large amount of workers is a very good way of getting your IP blocked by imgur.
So don't make too many requests per second for an extended amount of time.
