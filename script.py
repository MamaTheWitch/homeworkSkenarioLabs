import pytesseract as pt
from PIL import Image
import os
import re
import csv

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

path = r"C:\Users\sales\OneDrive\Desktop\Data_homework\Task_2"

fileLog = []
readyData = []

with os.scandir(path) as it:
    for entry in it:
        if entry.name.endswith(".png") or entry.name.endswith(".jpeg") and entry.is_file():
            fileLog.append(entry.path)


for file in fileLog:
    img_object = Image.open(file)
    img_text = pt.image_to_string(img_object)
    all_text = img_text.lower()
    split_text = all_text.split("\n")
    numberLog = []
    extract = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
    
    dictionary_of_a_file = dict()
    head, tail = os.path.split(file)
    filename = tail
    dictionary_of_a_file['file'] = filename
    
    def getNumbers():
        line = item.strip()
        dictionary_of_a_file['string'] = line
        if re.search(extract, line) is not None:
            for area in re.finditer(extract, line):
                numberLog.append(float(area[0]))
    
    if "total" in str(split_text):
        for item in split_text:
            if "total" in item:
                getNumbers()
    elif "appr" in str(split_text):
        for item in split_text:
            if "appr" in item:
                getNumbers()
    else:
        print ("Not found!")
    
    dictionary_of_a_file['sqFeet'] = max(numberLog)
    dictionary_of_a_file['sqMetres'] = min(numberLog)
    readyData.append(dictionary_of_a_file)
   
print(readyData)

# csv header
fieldnames = ['file', 'string', 'sqFeet', 'sqMetres']

# csv data
rows = readyData

with open('output.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

