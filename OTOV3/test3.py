import pytesseract
from PIL import ImageGrab
import pyautogui
import time
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import Levenshtein
import threading
import configparser
import cv2
import numpy as np
import psutil
import pyperclip
import queue

stop = False
tessdata_path = os.path.join(os.path.dirname(__file__), 'tessdata')
os.environ['TESSDATA_PREFIX'] = tessdata_path

config = configparser.ConfigParser()
config.read('config.ini')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_template_scores(scores,output_queue):
    changed = True
    global stop
    
    template_x_1 = config.get('screenshot_score', 'sx1')
    template_x_2 = config.get('screenshot_score', 'sx2')
    template_y_1 = config.get('screenshot_score', 'sy1')
    template_y_2 = config.get('screenshot_score', 'sy2')
        
    screenshot = pyautogui.screenshot(region=(float(template_x_1), float(template_y_1), float(template_x_2) - float(template_x_1), float(template_y_2) - float(template_y_1)))
    screenshot.save("screenshot_score.png")
    
    recognized_text = pytesseract.image_to_string(screenshot, lang='eng')
    recognized_text = recognized_text.rstrip()
    
    length = len(scores) - 1
    if length > 10:
        if recognized_text == scores[length - 8]:
            changed = False
    if changed == False:
        stop = True

    output_queue.put(recognized_text)
    
    
scores = []
output_queue = queue.Queue()

for i in range(20):
    thread5 = threading.Thread(target=process_template_scores, args=(scores,output_queue))
    thread5.start()
    thread5.join()
    scores.append(output_queue.get())
    print(scores)
    if stop == True:
        sys.exit('stop test')
    
