import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def surround_strips(text, regex, size, case):
    """ Printa todos locais onde a match de regex aparece, como tambem o texto em volta """
    if case:
        matches = re.finditer(regex, text)
    else:
        matches = re.finditer(regex, text, re.IGNORECASE)
    strips = []
    for found in matches:
        match_start = found.start()
        match_end = found.end()
        str_len = len(text)

        # Se for < 0 vai dar erro, entao começo a printar do inicio
        if (match_start - size) >= 0:
            print_start = match_start - size
        else:
            print_start = 0

        if (match_end + size) <= str_len:
            print_end = match_end + size
        else:
            print_end = str_len

        strip_str = text[print_start:match_start] + bcolors.OKGREEN + text[match_start:match_end] + bcolors.ENDC + text[match_end:print_end]
        strips.append(strip_str)

    return strips


def print_strips(text, regex, surround_len, case):
    # TODO: add case here
    # Aqui eu vou pegar o texto e separar em 'strips' de texto perto de onde deu o match na string
    row_strips = surround_strips(text, regex, surround_len, case)

    strips_str = ''
    for s in row_strips:
        strips_str += f'{bcolors.OKBLUE}#{bcolors.ENDC}'*30
        strips_str += '\n'*2
        strips_str += s
        strips_str += '\n'*2
    strips_str += f'{bcolors.OKBLUE}#{bcolors.ENDC}'*30

    print(strips_str)


def filter_df(df, regex, case):
    filtered_df = df.loc[df['text'].str.contains(regex, case=case)]
    return filtered_df


def create_folder(path):
    Path(os.path.join(path)).mkdir(parents=True, exist_ok=True)


HERE = os.path.dirname(sys.argv[0])
FILES_PATH = os.path.join(HERE, '..', '..', 'files')

conn = sqlite3.connect(os.path.join(FILES_PATH, 'detected_text.db'))
c = conn.cursor()

df = pd.read_sql("SELECT * FROM texts", con=conn)

### QUERY PARAMS
# regex = '[^@\s]+@[^@\s\.]+\.[^@\.\s]+'
regex = r'[^@\s]+@[^@\s\.]+\.[^@\.\s]+'
case = False
####

filtered = filter_df(df, regex=regex, case=case)

for index, row in filtered.iterrows():
    text = row['text']
    img_filename = row['img_id'] + '.' + row['extension']
    print('\n', '#'*30,)
    print(f'vvv Text of {img_filename} vvv')
    print('#'*30, '\n')
    print_strips(text=text, regex=regex, surround_len=10, case=case)

conn.close()
