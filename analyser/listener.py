from database import insert_text, create_db
from pydantic import BaseModel
from fastapi import FastAPI
from pathlib import Path
from PIL import Image
import numpy as np
import uvicorn
import easyocr
import sqlite3
import sys
import os


class Message(BaseModel):
    msg: str


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


HERE = os.path.dirname(sys.argv[0])
# Confirms that the output folder exists
Path(os.path.join(HERE, '..', 'files')).mkdir(parents=True, exist_ok=True)

print('Starting database...')
create_db()
print('Starting OCR reader...')
reader = easyocr.Reader(['en'], gpu=False)

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

    return {'msg': 'OK'}


if __name__ == '__main__':
    print('Running server...')
    uvicorn.run(app, host="0.0.0.0", port=8001)

    # POST with cURL
    # curl -d '{"msg":"test_msg"}' -X POST localhost:8001
    # curl -d '{"msg":"El2dyRE.png"}' -X POST localhost:8001
