# Imgur-Text Scraper

Look for random valid imgur url, download the image and detect all texts in it by running an OCR.

Saves the result on a SQLite3 database on /files/detected_text.db

## Running it
This app uses both Golang and Python, so it's more practical to run it with Docker.

The docker app will spin out many goroutines that will look for valid imgur urls, which might take a while.

The python app will wait for new images to be downloaded and run OCR on it.

## Running with docker
Run it with docker-compose
```
docker-compose build
docker-compose up
```

## Running without docker
You'll need both Golang and Python installed.

For Golang there are no extra dependencies.

For the python app you'll need everything listed in /analyser/requirements.txt
```
numpy==1.21.2
opencv-python==4.5.3.56
Pillow==8.3.1
asgiref==3.4.1
click==8.0.1
fastapi==0.68.1
h11==0.12.0
pydantic==1.8.2
starlette==0.14.2
typing-extensions==3.10.0.2
uvicorn==0.15.0
```
as well as **Pytorch**, which depending on your plataform might bug out if you install it with pip.


## Files
All images are downloaded into /imgs.

The database is located in /files.

## Warning
Since the urls are randomly generated, there **WILL** be a good amount of NSFW images.

Running the program with a large amount of workers is a very good way of getting your IP blocked by imgur.
So don't make too many requests per second for an extended amount of time.
