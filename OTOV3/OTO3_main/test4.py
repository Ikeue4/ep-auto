import pytesseract
from datetime import datetime
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
from OTO import OTO_learning

config = configparser.ConfigParser()
config.read('config.ini')

def onclick(event):
    global x1, y1, x2, y2, clicks
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        print(f"Clicked position: x={x:.2f}, y={y:.2f}")
        if clicks == 0:
            x1 = x
            y1 = y
        elif clicks == 1:
            x2 = x
            y2 = y
        else:
            print("error")
        clicks += 1
        
def screenshot_position():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    
    img_path = 'screenshot.png'
    img = mpimg.imread(img_path)
    
    screen_width, screen_height = pyautogui.size()
    plt.figure(figsize=(16,9))  # Adjust the figure size as needed
    plt.imshow(img)
    
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    
    plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    
    # Adjust the axis limits for bottom-right to bottom-left
    plt.show()


def generate_image():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot_scan.png")
    
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

tessdata_path = os.path.join(os.path.dirname(__file__), 'tessdata')
os.environ['TESSDATA_PREFIX'] = tessdata_path

def find_words_screen(target_words):
# Perform OCR on the screenshot
    extracted_data = pytesseract.image_to_data('screenshot_scan.png', output_type=pytesseract.Output.DICT)

    target_words = ['Spanish']
    word_positions = ''

    for i, word in enumerate(extracted_data['text']):
        if word in target_words:
            x = extracted_data['left'][i]
            y = extracted_data['top'][i]
            width = extracted_data['width'][i]
            height = extracted_data['height'][i]
            word_positions = ((word, x, y, width, height))

    return word_positions
    
word_positions = find_words_screen('Spanish')
print(word_positions)

pyautogui.moveTo(word_positions[1], word_positions[2])
pyautogui.click()
