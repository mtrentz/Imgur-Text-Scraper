import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path
from shutil import copyfile


def create_folder(path):
    Path(os.path.join(path)).mkdir(parents=True, exist_ok=True)

HERE = os.path.dirname(sys.argv[0])
FILES_PATH = os.path.join(HERE, '..', '..', 'files')
IMAGES_PATH = os.path.join(HERE, '..', '..', 'imgs')

### Create the parent folder where the detected images will be
create_folder(os.path.join(FILES_PATH, 'detections'))

conn = sqlite3.connect(os.path.join(FILES_PATH, 'detected_text.db'))
c = conn.cursor()

df = pd.read_sql("SELECT * FROM texts", con=conn)

regex_detection_list = {
    'email': [
        r'email',
        r'mail',
        r'[^@\s]+@[^@\s\.]+\.[^@\.\s]+',
    ],
    'password': [
        r'password',
    ],
    'crypto': [
        r'bitcoin',
        r'bit',
        r'crypto',
        r'binance',
        # Bitcoin wallet regex
        r'(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}',
        # Eth wallet regex
        r'0x[a-fA-F0-9]{30,40}'
    ],
    'phone': [
        # US phone
        r'\([0-9]{3}\)[0-9]{3}-[0-9]{4}',
        # Brazil phone
        r'\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*',
        # India phone
        r'\+?\d[\d -]{8,12}\d',
    ]
}


for detection, regexes in regex_detection_list.items():
    print(f'Detecting images about: {detection}')
    # Create a folder for that category of detections (ex: emails, crypto stuff, etc..)
    detection_path = os.path.join(FILES_PATH, 'detections', detection)
    create_folder(detection_path)
    for regex in regexes:
        # Filter the database for the texts
        filtered = df.loc[df['text'].str.contains(regex, case=False)]

        for index, row in filtered.iterrows():
            text = row['text']
            img_filename = row['img_id'] + '.' + row['extension']

            img_source_path = os.path.join(IMAGES_PATH, img_filename)
            img_destination_path = os.path.join(detection_path, img_filename)

            # Check if the source exists so it can copy over
            if os.path.exists(img_source_path):
                # If exists, then check if it wasn't already copied to destination folder.
                if not os.path.exists(img_destination_path):
                    copyfile(img_source_path, img_destination_path)
