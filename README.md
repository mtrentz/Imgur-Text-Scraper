# Imgur-Text Scraper

Look for random valid imgur url, download the image and detect all texts in it by running an OCR.

Also tries to find important info by running some regex patterns on all text detected. You can create regex to look for emails, phone-numbers, and even some possible crypto stuff posted. If something is found, it will save the image on separate folder for further analysis.

Saves the result on a SQLite3 database on /files/detected_text.db

## Running it
This app uses both Golang and Python, so it's more practical to run it with Docker.

The docker app will spin out many goroutines that will look for valid imgur urls, which might take a while.

The python app will wait for new images to be downloaded and run OCR on it.

### Running with docker
Run it with docker-compose
```
docker-compose build
docker-compose up
```

### Running without docker
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

Images that are classified with important texts are saved on /files/detections.

## Warning
Since the urls are randomly generated, there **WILL** be a good amount of NSFW images.
'
Running the program with a large amount of workers is a very good way of getting your IP blocked by imgur.
So don't make too many requests per second for an extended amount of time.
