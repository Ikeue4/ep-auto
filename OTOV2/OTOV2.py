import pytesseract
from PIL import ImageGrab
import pyautogui
import time
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from fuzzywuzzy import fuzz
import threading

x1 = 0
y1 = 0
x2 = 0
y2 = 0
clicks = 0

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', end='\r'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}'),
    sys.stdout.flush()
    if iteration == total:
        print()

# Function to handle mouse click event
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

def clear_terminal():
    os.system("cls")
    
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
    
def screenshot_with_new(x1, y1, x2, y2):
    time.sleep(0.5)
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save("screenshot.png")
    
def train_data_out_other():
    language = []
    file = input("language list file name(spanish file) = ")
    recognized_text = pytesseract.image_to_string('screenshot.png')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open(file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
    f.close()
    
def train_data_out_english():
    file = input("language list file name(english file) = ")
    language = []
    recognized_text = pytesseract.image_to_string('screenshot.png')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open(file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
    f.close()


def train():
    global language_list
    file = input("language list file(spanish file) = ")
    f = open(file + '.txt', 'r')
    spanish = []
    for l in f:
        if ";" in l:
            parts = l.split(";", 1)
            l = parts[0]
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        spanish.append(l)
    f.close()
    
    file = input("language list file(english file) = ")
    f = open(file + '.txt', 'r')
    english = []
    for l in f:
        if ";" in l:
            parts = l.split(";", 1)
            l = parts[0]
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        spanish.append(l)
            
        english.append(l)
    f.close()
    
    print(english)
    try:
        upto = 1
        for i in spanish:
            language_list.append([spanish[upto], english[upto]])
            
            upto += 1
    except:
        print("end of list")
        
    for i in language_list:
        print(i)

def t1():
    total_iterations = 10
    for i in range(total_iterations + 1):
        time.sleep(0.01)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)

def t2():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
thread1 = threading.Thread(target=t1)
thread2 = threading.Thread(target=t2)

thread1.start()
thread2.start()

thread1.join()
thread1.join()
    
    
while True:
    print("1. Train\n2. Test\n3. Load")
    main_menu_input = input()
    clear_terminal()
    
    if main_menu_input == "1":
        clicks = 0
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        screenshot_position()
        print(x1, y1)
        print(x2, y2)
        screenshot_with_new(x1, y1, x2, y2)
        train_data_out_other()
        clicks = 0
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        screenshot_position()
        print(x1, y1)
        print(x2, y2)
        screenshot_with_new(x1, y1, x2, y2)
        train_data_out_english()
        language_list = []
        
    elif main_menu_input == "2":
        language_list = []
        train()
        time.sleep(2)
        for i in range(200):
            to_type = ''
            #time.sleep(0.05)
            # Get the coordinates of the region you want to capture
            # Replace these coordinates with the top-left and bottom-right coordinates of your desired region
            x1, y1 = 300, 720  # Top-left corner
            x2, y2 = 2500, 1000  # Bottom-right corner

            # Get the screen size
            screen_width, screen_height = pyautogui.size()

            # Ensure coordinates are within the screen boundaries
            x1 = max(0, min(x1, screen_width - 1))
            y1 = max(0, min(y1, screen_height - 1))
            x2 = max(0, min(x2, screen_width - 1))
            y2 = max(0, min(y2, screen_height - 1))

            # Capture the screenshot of the specified region
            screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

            # Save the screenshot to a file (optional)
            screenshot.save("screenshot.png")

            # Step 3: Capture the screenshot
            screenshot = 'screenshot.png'#ImageGrab.grab()


            # Step 4: Preprocess the screenshot (optional)

            # Step 5: Perform text recognition
            recognized_text = pytesseract.image_to_string(screenshot)

            # Print the recognized text
            print(recognized_text)
            recognized_text = recognized_text.rstrip()
            
            if "," in recognized_text:
                parts = recognized_text.split(",", 1)
                result = parts[0]
                
            else:
                result = recognized_text
                
            if recognized_text == 'ice cream, ice-cream':
                sys.exit

            for i in language_list:
                if fuzz.partial_ratio(i[1], result.lower()) >= 97:
                    print("recognized text")
                    print(i[0])
                    to_type=i[0]
                    
            pyautogui.moveTo(1650, 1400, duration=0.01)

            pyautogui.click()

            pyautogui.typewrite(to_type, interval=0.01)
                    
            if to_type == '':
                pyautogui.typewrite('?', interval=0.01)
                pyautogui.press('enter')

            # Simulate pressing the "Enter" key
            pyautogui.press('enter')
            