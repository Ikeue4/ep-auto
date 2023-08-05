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

tessdata_path = os.path.join(os.path.dirname(__file__), 'tessdata')
os.environ['TESSDATA_PREFIX'] = tessdata_path

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
        corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        corners_transformed = cv2.perspectiveTransform(corners, homography)
        target_with_box = cv2.polylines(target, [np.int32(corners_transformed)], True, (0, 255, 0), 3)
        
        island_center_x = int(np.mean(corners_transformed[:, :, 0]))
        island_center_y = int(np.mean(corners_transformed[:, :, 1]))
        
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
        h, w = template.shape
        corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        corners_transformed = cv2.perspectiveTransform(corners, homography)
        target_with_box = cv2.polylines(target, [np.int32(corners_transformed)], True, (0, 255, 0), 3)
        
        island_center_x = int(np.mean(corners_transformed[:, :, 0]))
        island_center_y = int(np.mean(corners_transformed[:, :, 1]))
        
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
    recognized_text = pytesseract.image_to_string('screenshot.png', lang='spa')
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
    clear_terminal()
    print("1. Train\n2. Test\n3. Settings\n4. quit...")
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
        clear_terminal()
        read_write = input('R for Read, W for Write: ')
        language_list = []
        train()
        time_delay = float(input('time delay(for dash, for normal do 0): '))
        stop = False
        errors = 0
        stop_flag = False
        times = int(input('how many times: '))
        #checking = input('would you like error checking(uses cpu resources!)(Y/N): ')
        thread1 = threading.Thread(target=num3)
        #thread1.start()
        for i in range(times):
            error = False
            
            generate_image()
            
            template_file1 = 'C:\GitHub\ep-auto\error_windows\Web capture_3-8-2023_183936_app.educationperfect.com.jpeg'
            template_file2 = 'C:\GitHub\ep-auto\error_windows\Web capture_3-8-2023_17436_app.educationperfect.com.jpeg'
            template_file3 = 'C:\GitHub\ep-auto\error_windows\Web capture_3-8-2023_1979_app.educationperfect.com.jpeg'
            
            thread2 = threading.Thread(target=process_template, args=(template_file1,))
            thread3 = threading.Thread(target=process_template_error, args=(template_file2,))
            thread4 = threading.Thread(target=process_template, args=(template_file3,))
            
            thread2.start()
            thread3.start()
            thread4.start()
            
            thread2.join()
            thread3.join()
            thread4.join()
            
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
                        
                print(recognized_text)
                if read_write.lower() == 'r':
                    closest_word = find_closest_match(result, spanish)
                    print("Closest match for '{}' is '{}'.".format(result, closest_word))
                    print(spanish)
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
    
                        
                print('=================to type=================')
                print(to_type)

                pyperclip.copy(to_type)
                pyautogui.hotkey('ctrl', 'v')

                # Simulate pressing the "Enter" key
                pyautogui.press('enter')
            else:
                time.sleep(2)
                pyautogui.press('enter')
        stop_flag = True
        clear_terminal()
        
    elif main_menu_input == '3':
        clear_terminal()
        print('1. screenshot scan area calibration\n2. cerise scan area calibration\n')
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
    
    elif main_menu_input == '4':
        clear_terminal()
        sys.exit()
            