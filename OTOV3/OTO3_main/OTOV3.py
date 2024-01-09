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
from OTO import OTO_learning, OTORead, OTO
import requests
import socket
from translate import Translator
import concurrent.futures
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet

OTO.setup()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
ip = (s.getsockname()[0])
s.close()
key = 'ygauihdgwga123125sjhd213'

data = {
    'ip': ip,
    'key': key
}

#out = requests.post('https://auto-ep-server-1.poeple.repl.co/val', json=data)
#print(out.text)

#if out.text != '200':
    #raise SyntaxWarning
#time.sleep(1)

config = configparser.ConfigParser()
config.read('config.ini')
x1 = 0
y1 = 0
x2 = 0
y2 = 0
clicks = 0
spanish = []
english = []
stop = False
error = False

def get_system_load():
    cpu_load = psutil.cpu_percent()
    gpu_load = 0  # Add code here to get GPU load if available
    ram_load = psutil.virtual_memory().percent
    return cpu_load, gpu_load, ram_load

def display_system_load(cpu_load, gpu_load, ram_load):
    print(f"CPU Load: {cpu_load}%")
    print(f"GPU Load: {gpu_load}%")
    print(f"RAM Load: {ram_load}%")
    
def system_main():
    clear_terminal()
    cpu_load, gpu_load, ram_load = get_system_load()
    display_system_load(cpu_load, gpu_load, ram_load)

def generate_image():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot_scan.png")
    
def num3():
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_system_load():
        cpu_load = psutil.cpu_percent()
        gpu_load = 0  # Add code here to get GPU load if available
        ram_load = psutil.virtual_memory().percent
        return cpu_load, gpu_load, ram_load

    def display_system_load(cpu_load, gpu_load, ram_load):
        print(f"CPU Load: {cpu_load}%")
        print(f"GPU Load: {gpu_load}%")
        print(f"RAM Load: {ram_load}%")

    def main():
        while not stop_flag:
            clear_terminal()
            cpu_load, gpu_load, ram_load = get_system_load()
            display_system_load(cpu_load, gpu_load, ram_load)
            time.sleep(1)

    if __name__ == '__main__':
        main()
        
def check_likeness(word1, word2):
    synonyms_word1 = set()
    synonyms_word2 = set()

    for syn in wordnet.synsets(word1):
        for lemma in syn.lemmas():
            synonyms_word1.add(lemma.name())
            
    for syn in wordnet.synsets(word2):
        for lemma in syn.lemmas():
            synonyms_word2.add(lemma.name())

    if synonyms_word1 & synonyms_word2:
        return True
    else:
        return False

def translate(i):
    translator = Translator(to_lang="en", from_lang="es")
    translated_text = translator.translate(i[0])
    true_text = i[1]
    true_text_parts = true_text.split(",")
    true_text = true_text_parts[0].strip()
    similarity_ratio = fuzz.ratio(true_text, translated_text)
    return i[0], i[1], translated_text, similarity_ratio
        
def part_selection(start):
    for i in range(2):
        get1 = 'x' + str(start)
        get2 = 'x' + str(start + 1)
        get3 = 'y' + str(start)
        get4 = 'y' + str(start + 1)
        x1 = config.get('tasks', get1)
        x2 = config.get('tasks', get2)
        y1 = config.get('tasks', get3)
        y2 = config.get('tasks', get4)
        
        screenshot = pyautogui.screenshot(region=(float(x1), float(y1), float(x2) - float(x1), float(y2) - float(y1)))
        screenshot.save('option.png')
        
        output = pytesseract.image_to_string('option.png', lang = 'spa')
        lines = output.splitlines()
        non_empty_lines = filter(str.strip, lines)
        output = "\n".join(non_empty_lines)
        
        return output
        
        
    
def find_words_screen(target_word, filename):
# Perform OCR on the screenshot
    extracted_data = pytesseract.image_to_data(filename, output_type=pytesseract.Output.DICT)
    target_words = []
    target_words = target_word.split()
    for i in target_words:
        print(i)
    word_positions = ''
    

    for i, word in enumerate(extracted_data['text']):
        for j in target_words:
            if word in j:
                x = extracted_data['left'][i]
                y = extracted_data['top'][i]
                width = extracted_data['width'][i]
                height = extracted_data['height'][i]
                if word != '':
                    word_positions = ((word, x, y, width, height))
                break

    print(word_positions)
    return word_positions   

def process_template(template_file):
    global stop

    confidence_threshold = 18
    # Load the target image
    target = cv2.imread('screenshot_scan.png', 0)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Load the template image
    template = cv2.imread(template_file, 0)

    # Downscale the target and template images by a factor (e.g., 0.5 for half size)
    scale_factor = 1
    target = cv2.resize(target, None, fx=scale_factor, fy=scale_factor)
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)

    # Detect and compute keypoints and descriptors for the template and target images
    keypoints_template, descriptors_template = sift.detectAndCompute(template, None)
    keypoints_target, descriptors_target = sift.detectAndCompute(target, None)

    # Create a brute-force matcher
    bf = cv2.BFMatcher()

    # Match descriptors between the template and target images
    matches = bf.match(descriptors_template, descriptors_target)

    # Sort the matches by distance (lower distance means better match)
    matches = sorted(matches, key=lambda x: x.distance)

    # Select reliable matches using RANSAC
    src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_target[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Calculate the number of inliers
    num_inliers = np.sum(mask)

    # Calculate the percentage of inliers
    confidence = (num_inliers / len(matches)) * 100
    print(confidence)
    if confidence >= confidence_threshold:
        #print('success')
        # Draw bounding box around the template in the target image
        h, w = template.shape
        
        # Display the target image with the bounding box
        #cv2.imshow("Target Image with Bounding Box", target_with_box)
        cv2.waitKey(0)
        stop = True
        
def process_template_opp(template_file):
    global stop

    confidence_threshold = 50
    # Load the target image
    target = cv2.imread('screenshot_scan.png', 0)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Load the template image
    template = cv2.imread(template_file, 0)

    # Downscale the target and template images by a factor (e.g., 0.5 for half size)
    scale_factor = 1
    target = cv2.resize(target, None, fx=scale_factor, fy=scale_factor)
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)

    # Detect and compute keypoints and descriptors for the template and target images
    keypoints_template, descriptors_template = sift.detectAndCompute(template, None)
    keypoints_target, descriptors_target = sift.detectAndCompute(target, None)

    # Create a brute-force matcher
    bf = cv2.BFMatcher()

    # Match descriptors between the template and target images
    matches = bf.match(descriptors_template, descriptors_target)

    # Sort the matches by distance (lower distance means better match)
    matches = sorted(matches, key=lambda x: x.distance)

    # Select reliable matches using RANSAC
    src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_target[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Calculate the number of inliers
    num_inliers = np.sum(mask)

    # Calculate the percentage of inliers
    confidence = (num_inliers / len(matches)) * 100
    print(confidence)
    if confidence <= confidence_threshold:
        #print('success')
        # Draw bounding box around the template in the target image
        h, w = template.shape
        
        # Display the target image with the bounding box
        #cv2.imshow("Target Image with Bounding Box", target_with_box)
        cv2.waitKey(0)
        stop = True

def process_template_error(template_file):
    global error
    
    confidence_threshold = 18
    # Load the target image
    target = cv2.imread('screenshot_scan.png', 0)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Load the template image
    template = cv2.imread(template_file, 0)

    # Downscale the target and template images by a factor (e.g., 0.5 for half size)
    scale_factor = 1
    target = cv2.resize(target, None, fx=scale_factor, fy=scale_factor)
    template = cv2.resize(template, None, fx=scale_factor, fy=scale_factor)

    # Detect and compute keypoints and descriptors for the template and target images
    keypoints_template, descriptors_template = sift.detectAndCompute(template, None)
    keypoints_target, descriptors_target = sift.detectAndCompute(target, None)

    # Create a brute-force matcher
    bf = cv2.BFMatcher()

    # Match descriptors between the template and target images
    matches = bf.match(descriptors_template, descriptors_target)

    # Sort the matches by distance (lower distance means better match)
    matches = sorted(matches, key=lambda x: x.distance)

    # Select reliable matches using RANSAC
    src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_target[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Calculate the number of inliers
    num_inliers = np.sum(mask)

    # Calculate the percentage of inliers
    confidence = (num_inliers / len(matches)) * 100
    print(confidence)
    if confidence >= confidence_threshold:
        #print('success')
        # Draw bounding box around the template in the target image
        
        # Display the target image with the bounding box
        #cv2.imshow("Target Image with Bounding Box", target_with_box)
        cv2.waitKey(0)
        error = True


def find_closest_match(target_word, word_list):
    closest_match = None
    min_distance = float('inf')

    for word in word_list:
        distance = Levenshtein.distance(target_word, word)
        if distance < min_distance:
            min_distance = distance
            closest_match = word

    return closest_match

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
    recognized_text = pytesseract.image_to_string('screenshot.png', lang='spa')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open('trained_models_OTOV3/' + file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
        print(i)
    f.close()
    
def train_data_out_other_ai(name):
    language = []
    file = name + '_sp'
    recognized_text = pytesseract.image_to_string('screenshot.png', lang='spa')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open('trained_models_OTOV3/' + file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
        print(i)
    f.close()
    
def train_data_out_english_ai(name):
    file = name + '_en'
    language = []
    recognized_text = pytesseract.image_to_string('screenshot.png', lang='eng')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open('trained_models_OTOV3/' + file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
        print(i)
    f.close()
    
def train_data_out_english():
    file = input("language list file name(english file) = ")
    language = []
    recognized_text = pytesseract.image_to_string('screenshot.png', lang='eng')
    lines_list = [line for line in recognized_text.splitlines() if line.strip()]
    f = open('trained_models_OTOV3/' + file + '.txt', 'w')
    
    for i in lines_list:
        f.write("\n")
        f.write(i)
        print(i)
    f.close()


def train():
    global language_list
    global spanish
    global english
    file = input("language list file(spanish file) = ")
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    spanish = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        spanish.append(l)
    f.close()
    
    file = input("language list file(english file) = ")
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    english = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
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
        
def train_ai(name):
    global language_list
    global spanish
    global english
    file = name + '_sp'
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    spanish = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        spanish.append(l)
    f.close()
    
    file = name + '_en'
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    english = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
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
    if length > 30:
        if recognized_text == scores[length - 28]:
            changed = False
    if changed == False:
        stop = True

    output_queue.put(recognized_text)
    


def t1():
    clear_terminal()
    cpu_load, gpu_load, ram_load = get_system_load()
    display_system_load(cpu_load, gpu_load, ram_load)


def t2():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
def t3():
    tessdata_path = os.path.join(os.path.dirname(__file__), 'tessdata')
    print(tessdata_path)
    os.environ['TESSDATA_PREFIX'] = tessdata_path

    
thread1 = threading.Thread(target=t1)
thread2 = threading.Thread(target=t2)
thread3 = threading.Thread(target=t3)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()
    

while True:
    clear_terminal()
    print("1. Train\n2. Test\n3. Settings\n4. quit...")
    main_menu_input = input()
    clear_terminal()
    
    if main_menu_input == "1":
        auto_train = input('Auto-Train(Y/N): ')
        if auto_train.lower() == 'n':
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
        elif auto_train.lower() == 'y':
            x1 = config.get('screenshot_auto', 'ox1')
            x2 = config.get('screenshot_auto', 'ox2')
            y1 = config.get('screenshot_auto', 'oy1')
            y2 = config.get('screenshot_auto', 'oy2')
            screenshot_with_new(float(x1), float(y1), float(x2), float(y2))
            train_data_out_other()
            x1 = config.get('screenshot_auto', 'sx1')
            x2 = config.get('screenshot_auto', 'sx2')
            y1 = config.get('screenshot_auto', 'sy1')
            y2 = config.get('screenshot_auto', 'sy2')
            screenshot_with_new(float(x1), float(y1), float(x2), float(y2))
            
            train_data_out_english()
    elif main_menu_input == "2":
        clear_terminal()
        read_write = input('R for Read, W for Write: ')
        language_list = []
        train()
        time_delay = float(input('time delay(for dash, for normal do 0): '))
        stop = False
        errors = 0
        stop_flag = False
        scores = []
        times = int(input('how many times: '))
        #checking = input('would you like error checking(uses cpu resources!)(Y/N): ')
        thread1 = threading.Thread(target=num3)
        #thread1.start()
        output_queue = queue.Queue()
        times_done = 0
        for i in range(times):
            time.sleep(0.1)
            start_time_cpu = time.time()
            error = False
            
            generate_image()
            
            template_file1 = 'error_windows\Web capture_3-8-2023_183936_app.educationperfect.com.jpeg'
            template_file2 = 'error_windows\Web capture_3-8-2023_17436_app.educationperfect.com.jpeg'
            template_file3 = 'error_windows\Web capture_3-8-2023_1979_app.educationperfect.com.jpeg'
            template_file4 = 'error_windows\Web capture_5-11-2023_18542_app.educationperfect.com.jpeg'
            
            thread2 = threading.Thread(target=process_template, args=(template_file1,))
            thread3 = threading.Thread(target=process_template_error, args=(template_file2,))
            thread4 = threading.Thread(target=process_template, args=(template_file3,))
            thread5 = threading.Thread(target=process_template_scores, args=(scores,output_queue))
            thread6 = threading.Thread(target=process_template_opp, args=(template_file4,))
            
            thread2.start()
            thread3.start()
            thread4.start()
            thread5.start()
            thread6.start()
            
            thread2.join()
            thread3.join()
            thread4.join()
            thread5.join()
            thread6.join()
            
            scores.append(output_queue.get())
            
            if stop == True:
                break
            if error == True:
                errors += 1
            
            time.sleep(time_delay)
            to_type = ''
            
            if error == False:
                #time.sleep(0.05)
                # Get the coordinates of the region you want to capture
                # Replace these coordinates with the top-left and bottom-right coordinates of your desired region
                x1 = config.get('screenshot', 'x1')
                x2 = config.get('screenshot', 'x2')
                y1 = config.get('screenshot', 'y1')
                y2 = config.get('screenshot', 'y2')

                    # Get the screen size
                screen_width, screen_height = pyautogui.size()

                # Ensure coordinates are within the screen boundaries
                x1 = max(0, min(float(x1), screen_width - 1))
                y1 = max(0, min(float(y1), screen_height - 1))
                x2 = max(0, min(float(x2), screen_width - 1))
                y2 = max(0, min(float(y2), screen_height - 1))

                # Capture the screenshot of the specified region
                screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

                # Save the screenshot to a file (optional)
                screenshot.save("screenshot.png")

                    # Step 3: Capture the screenshot
                screenshot = 'screenshot.png'#ImageGrab.grab()
                
                if read_write.lower() == 'r':
                    recognized_text = pytesseract.image_to_string(screenshot, lang='spa')

                if read_write.lower() == 'w':
                    recognized_text = pytesseract.image_to_string(screenshot, lang='eng')

                # Print the recognized text
                #print(recognized_text)
                recognized_text = recognized_text.rstrip()
                    
                result = recognized_text
                
                if '|' in result:
                    result = result.replace('|', 'I')
                    
                if 'Translate from English to Spanish' in result:
                    result = result.replace('Translate from English to Spanish', "")
                    
                if 'Translate from Spanish to English' in result:
                    result = result.replace('Translate from Spanish to English', "")
                    
                if 'Translate from French to English' in result:
                    result = result.replace('Translate from French to English', "")
                    
                if 'Translate from English to French' in result:
                    result = result.replace('Translate from English to French', "")
                
                result = result.rstrip()
                        
                print(recognized_text)
                if read_write.lower() == 'r':
                    closest_word = find_closest_match(result, spanish)
                    print("Closest match for '{}' is '{}'.".format(result, closest_word))
                    print(spanish)
                    if closest_word == '?':
                        to_type = 'error'
                    else:
                        i = spanish.index(closest_word)
                        i -= 1
                        x = language_list[i]
                        #print(x[1])
                        to_type = x[1]
                        
                elif read_write.lower() == 'w':
                    closest_word = find_closest_match(result, english)
                    print("Closest match for '{}' is '{}'.".format(result, closest_word))
                    i = english.index(closest_word)
                    i -= 1
                    x = language_list[i]
                    #print(x[0])
                    to_type = x[0]

                            
                pyautogui.moveTo(float(config.get('cerse', 'x')),float(config.get('cerse', 'y')), duration=0.01)

                pyautogui.click()

                if 'ï¿½' in to_type:
                    to_type = to_type.replace('ï¿½', "í")
                        
                print('=================to type=================')
                print(to_type)

                pyperclip.copy(to_type)
                pyautogui.hotkey('ctrl', 'v')

                # Simulate pressing the "Enter" key
                pyautogui.press('enter')
            else:
                time.sleep(2)
                pyautogui.press('enter')
            times_done += 1
            length = len(scores) - 1
            end_time_cpu = time.time()
            execution_time_cpu = end_time_cpu - start_time_cpu
            print(f"CPU Execution Time: {execution_time_cpu:.4f} seconds")
            print("errors:", errors)
            print(str(times_done)+"/"+str(times))
            print("user score:", scores[length])
        stop_flag = True
        clear_terminal()
        
    elif main_menu_input == '3':
        clear_terminal()
        print('1. screenshot scan area calibration\n2. cerise scan area calibration\n3. auto train scan area calibration\n4. score checking calibration')
        settings_menu_input = input("")
        if settings_menu_input == "1":
            clear_terminal()
            x1 = config.get('screenshot', 'x1')
            x2 = config.get('screenshot', 'x2')
            y1 = config.get('screenshot', 'y1')
            y2 = config.get('screenshot', 'y2')
            print('From left corner:', x1, y1,"\nFrom right corner:", x2, y2)
            change = input("change values(Y/N): ")
            if change.lower() == 'y':
                print('tab to ep!!!!!')
                time.sleep(2)
                clicks = 0
                screenshot_position()
                config.set('screenshot', 'x1', str(x1))
                config.set('screenshot', 'x2', str(x2))
                config.set('screenshot', 'y1', str(y1))
                config.set('screenshot', 'y2', str(y2))
                print('you are changing your screen scan to:', x1, y1, x2, y2, "Y/N")
                conferm = input('')
                if conferm.lower() == 'y':
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
        elif settings_menu_input == "2":
            clear_terminal()
            x2 = config.get('cerse', 'x')
            y2 = config.get('cerse', 'y')
            change = input("do you want to change the cerse position? (Y/N): ")
            if change.lower() == 'y':
                print('tab to ep!!!!')
                time.sleep(2)
                clicks = 1
                screenshot_position()
                config.set('cerse', 'x', str(x2))
                config.set('cerse', 'y', str(y2))
                print('are you sure you want to change the cerse position? (Y/N): ')
                conferm = input()
                if conferm.lower() == 'y':
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
        elif settings_menu_input == '3':
            clear_terminal()
            change = input("change values(Y/N): ")
            print('tab to ep!!!!!(first is other language)')
            time.sleep(2)
            clicks = 0
            screenshot_position()
            config.set('screenshot_auto', 'ox1', str(x1))
            config.set('screenshot_auto', 'ox2', str(x2))
            config.set('screenshot_auto', 'oy1', str(y1))
            config.set('screenshot_auto', 'oy2', str(y2))
            print('conform first part')
            conferm = input('')
            if conferm.lower() == 'y':
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            clicks = 0
            time.sleep(0.5)
            screenshot_position()
            config.set('screenshot_auto', 'sx1', str(x1))
            config.set('screenshot_auto', 'sx2', str(x2))
            config.set('screenshot_auto', 'sy1', str(y1))
            config.set('screenshot_auto', 'sy2', str(y2))
            print('conform second part')
            conferm = input('')
            if conferm.lower() == 'y':
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        elif settings_menu_input == '4':
            clear_terminal()
            change = input("change values(Y/N): ")
            print('tab to ep!!!!!(first is other language)')
            time.sleep(2)
            clicks = 0
            screenshot_position()
            config.set('screenshot_score', 'sx1', str(x1))
            config.set('screenshot_score', 'sx2', str(x2))
            config.set('screenshot_score', 'sy1', str(y1))
            config.set('screenshot_score', 'sy2', str(y2))
            print('conferm')
            conferm = input()
            if conferm.lower() == 'y':
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        elif settings_menu_input == '5':
            clear_terminal()
            change = input("change values(Y/N): ")
            print('tab to ep!!!!!(first is other language)')
            time.sleep(2)
            clicks = 0
            screenshot_position()
            config.set('tasks', 'x11', str(x1))
            config.set('tasks', 'x12', str(x2))
            config.set('tasks', 'y11', str(y1))
            config.set('tasks', 'y12', str(y2))
            clicks = 0
            time.sleep(0.5)
            screenshot_position()
            config.set('tasks', 'x21', str(x1))
            config.set('tasks', 'x22', str(x2))
            config.set('tasks', 'y21', str(y1))
            config.set('tasks', 'y22', str(y2))
            clicks = 0
            time.sleep(0.5)
            screenshot_position()
            config.set('tasks', 'x31', str(x1))
            config.set('tasks', 'x32', str(x2))
            config.set('tasks', 'y31', str(y1))
            config.set('tasks', 'y32', str(y2))
            clicks = 0
            time.sleep(0.5)
            screenshot_position()         
            config.set('tasks', 'x41', str(x1))
            config.set('tasks', 'x42', str(x2))
            config.set('tasks', 'y41', str(y1))
            config.set('tasks', 'y42', str(y2))
            print('conferm')
            conferm = input()
            if conferm.lower() == 'y':
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        elif settings_menu_input == "6":
            clear_terminal()
            x1 = config.get('screenshot_options', 'x1')
            x2 = config.get('screenshot_options', 'x2')
            y1 = config.get('screenshot_options', 'y1')
            y2 = config.get('screenshot_options', 'y2')
            print('From left corner:', x1, y1,"\nFrom right corner:", x2, y2)
            change = input("change values(Y/N): ")
            if change.lower() == 'y':
                print('tab to ep!!!!!')
                time.sleep(2)
                clicks = 0
                screenshot_position()
                config.set('screenshot_options', 'x1', str(x1))
                config.set('screenshot_options', 'x2', str(x2))
                config.set('screenshot_options', 'y1', str(y1))
                config.set('screenshot_options', 'y2', str(y2))
                print('you are changing your screen scan to:', x1, y1, x2, y2, "Y/N")
                conferm = input('')
                if conferm.lower() == 'y':
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
    
    elif main_menu_input == '4':
        clear_terminal()
        sys.exit()
        
    elif main_menu_input == '5':
        conferm = input('full auto mode active!!!!!! continue Y')
        if conferm.lower() != 'y':
            sys.exit()
            
        while True:
            option1 = part_selection(11)
            option2 = part_selection(21)
            option3 = part_selection(31)
            option4 = part_selection(41)
            possibility_in = []
            possibility_out = []
            possibility_in.append(option1)
            possibility_in.append(option2)
            possibility_in.append(option3)
            possibility_in.append(option4)
            best_option, to_learn = '', ''

            for i in possibility_in:
                try:
                    possibility_out.append(OTO_learning.get_data_persistent(i))
                except:
                    learn = True
                    to_learn = i
                    '''OTO_learning.set_data_persistent(i, 0, 100)
                    possibility_out.append(OTO_learning.get_data_persistent(i))
                    best_option = '''''
                    
            x1 = config.get('screenshot_options', 'x1')
            x2 = config.get('screenshot_options', 'x2')
            y1 = config.get('screenshot_options', 'y1')
            y2 = config.get('screenshot_options', 'y2')
            
            screenshot = pyautogui.screenshot(region=(float(x1), float(y1), float(x2) - float(x1), float(y2) - float(y1)))
            screenshot.save("screenshot_option.png")

            if learn == True:
                print(to_learn)
                word_positions = find_words_screen(to_learn, 'screenshot_option.png')
                print(word_positions[1] + float(x1), word_positions[2] + float(y1))
                pyautogui.moveTo(word_positions[1] + float(x1), word_positions[2] + float(y1))
                pyautogui.click()
                x1 = config.get('screenshot_auto', 'ox1')
                x2 = config.get('screenshot_auto', 'ox2')
                y1 = config.get('screenshot_auto', 'oy1')
                y2 = config.get('screenshot_auto', 'oy2')
                screenshot_with_new(float(x1), float(y1), float(x2), float(y2))
                train_data_out_other_ai(to_learn)
                x1 = config.get('screenshot_auto', 'sx1')
                x2 = config.get('screenshot_auto', 'sx2')
                y1 = config.get('screenshot_auto', 'sy1')
                y2 = config.get('screenshot_auto', 'sy2')
                screenshot_with_new(float(x1), float(y1), float(x2), float(y2))
                train_data_out_english_ai(to_learn)
                
                language_list = []
                train_ai(to_learn)
                results_translate = []

                max_threads = len(spanish)

                # Create a thread pool with the specified maximum number of threads
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                    # Submit tasks to the thread pool for each language
                    futures = [executor.submit(translate, lang) for lang in language_list]

                    # Wait for all tasks to complete
                    concurrent.futures.wait(futures)

                    # Print the results after all tasks have completed
                    for future in concurrent.futures.as_completed(futures):
                        translated_result = future.result()
                        results_translate.append(future.result())
                        
                differences = []
                for i in results_translate:
                    if float(i[3]) < 30:
                        differences.append(i)
                        
                '''for i in differences:
                    print(i)
                    if check_likeness(i[1], i[2]) == True:
                        pass
                    else:
                        change = input('a difference has been found do you want to change it to the translated vertion or say the same?(do you want to change Y/N)')
                        if change.lower() == 'y':
                            print(i[1],i[0],i[2],i[0])
                            english.remove(i[1])
                            spanish.remove(i[0])
                            english.append(i[2])
                            spanish.append(i[0])'''

                language_list = []
                try:
                    upto = 1
                    for i in spanish:
                        language_list.append([spanish[upto], english[upto]])
                        
                        upto += 1
                except:
                    print("end of list")
                    
                for i in language_list:
                    print(i)
                
                language_list = []
                train_ai(to_learn)
                sys.exit()
            if best_option == '':
                best_option = OTO_learning.get_day_point_possibilities(possibility_out)
            print(best_option)
            
                
            word_positions = find_words_screen(best_option, 'screenshot_option.png')
            print(word_positions)
            pyautogui.moveTo(word_positions[1], word_positions[2])
            pyautogui.click()
            
            time.sleep(1000) 
            break
        
        