import easyocr
import sqlite3
import sys
import os

def detect_text(img_path):
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    result = reader.readtext(img_path)

    detected_text = ""

    # Get detected text separated by newline
    for res in result:
        text = res[1]
        detected_text += text + '\n'
    
    return detected_text