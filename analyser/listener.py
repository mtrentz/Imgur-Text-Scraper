from database import insert_text, create_db
from regexes import REGEX_DETECTION_LIST
from pydantic import BaseModel
from fastapi import FastAPI
from shutil import copyfile
from pathlib import Path
from PIL import Image
import numpy as np
import uvicorn
import easyocr
import sqlite3
import sys
import os
import re


class Message(BaseModel):
    msg: str


def create_folder(path):
    Path(os.path.join(path)).mkdir(parents=True, exist_ok=True)


def resized_img(img_path):
    with Image.open(img_path) as im:
        im = im.convert('RGB')
        max_size = 1000, 1000
        # Resizes image
        im.thumbnail(max_size, Image.ANTIALIAS)
        return im.copy()


def detect_text(img_path):
    img = np.asarray(resized_img(img_path))
    result = reader.readtext(img)
    detected_text = ""
    # Get detected text separated by newline
    for res in result:
        text = res[1]
        detected_text += text + '\n'
    return detected_text


def copy_img(img_source_path, img_destination_path):
    # Check if the source exists so it can copy over
    if os.path.exists(img_source_path):
        # If exists, then check if it wasn't already copied to destination folder.
        if not os.path.exists(img_destination_path):
            copyfile(img_source_path, img_destination_path)


def classify_text(img_name, img_text):
    # Runs some regexes to classify possible important texts in the image detected text.
    # All detections types and regexes are withing regexes.py

    # Keep track of all detections for that image:
    img_detections = []

    for detection, regexes in REGEX_DETECTION_LIST.items():
        # Create a folder for that category of detections (ex: emails, crypto stuff, etc..)
        detection_path = os.path.join(FILES_PATH, 'detections', detection)
        create_folder(detection_path)
        for regex in regexes:
            re_exp = re.compile(regex, re.IGNORECASE)
            if re_exp.search(img_text):
                img_source_path = os.path.join(IMAGES_PATH, img_name)
                img_destination_path = os.path.join(detection_path, img_name)
                # Create a copy of the image in the DETECTIONS folder.
                copy_img(img_source_path, img_destination_path)
                # Add detection to img_detection list
                img_detections.append(detection)
                # Breaks out of inner loop, because already found that image to be of certain DETECTION type
                break
    
    if len(img_detections) >= 1:
        print(f'>> Found image {img_name} to contain text about: {img_detections}')


app = FastAPI()

@app.get('/ready')
def api_ready():
    return {'Connected': 'API is online'}


@app.post('/')
async def imgur_scraper(msg: Message):
    # Get image name
    img_name = msg.msg

    HERE = os.path.dirname(sys.argv[0])

    # Image/File info
    img_identifier = img_name.split('.')[0]
    img_extension = img_name.split('.')[1]
    img_path = os.path.join(HERE, '..', 'imgs', img_name)

    # Conect do Database
    try:
        conn = sqlite3.connect(os.path.join(HERE, '..', 'files', 'detected_text.db'))
        c = conn.cursor()
    except Exception as e:
        print('Error coneccting to DB', e)
        return {'msg': 'Error coneccting to DB'}

    try:
        # Detects text, reader object started in main execution
        print(f'Detecting text on: {img_identifier}')
        text = detect_text(img_path)
        print(f'Detected text on: {img_identifier}')
    except Exception as e:
        print('Error recognizing image', e)
        return {'msg': 'Error recognizing image'}

    # Add text to DB
    insert_text(conn, c, img_identifier, img_extension, text)

    # Closes db connection
    conn.close()

    # Try to detect important info on text
    classify_text(img_name, text)

    return {'msg': 'OK'}


HERE = os.path.dirname(sys.argv[0])
# Confirms that the output folder exists
create_folder(os.path.join(HERE, '..', 'files'))
FILES_PATH = os.path.join(HERE, '..', 'files')
IMAGES_PATH = os.path.join(HERE, '..', 'imgs')
### Create the parent folder where the detected images will be
create_folder(os.path.join(FILES_PATH, 'detections'))

print('Starting database...')
create_db()
print('Starting OCR reader...')
reader = easyocr.Reader(['en'], gpu=False)


if __name__ == '__main__':
    print('Running server...')
    uvicorn.run(app, host="0.0.0.0", port=8001)

    # POST with cURL
    # curl -d '{"msg":"test_msg"}' -X POST localhost:8001
    # curl -d '{"msg":"El2dyRE.png"}' -X POST localhost:8001
