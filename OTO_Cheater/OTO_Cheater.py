from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import psutil
import os
import multiprocessing
import sys
import pkg_resources

mode = 1

class TextColor:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

def setup():
    cpu_load = psutil.cpu_percent()
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [CPU PERCENT]", cpu_load)
    num_threads = multiprocessing.cpu_count()
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [CPU THREADS]", num_threads)
    total_ram = psutil.virtual_memory().total
    total_ram_gb = total_ram / (1024 ** 3)
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [RAM        ] {total_ram_gb:.2f} GB")
    ram_load = psutil.virtual_memory().percent
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [RAM PERCENT] {ram_load}%")
    ram_free = psutil.virtual_memory().free
    total_ram_free_gb = ram_free / (1024 ** 3)
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [RAM FREE   ] {total_ram_free_gb:.2f} GB")
    python_version = sys.version
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [PYTHON     ]", python_version)
    debug_clear = clear_debug()
    print(f"[{TextColor.YELLOW}WARNING{TextColor.RESET}] [DEBUG CLEAR] {debug_clear}")
    debug_start = debug_setup()
    print(f"[{TextColor.YELLOW}WARNING{TextColor.RESET}] [DEBUG START] {debug_start}")
    check_packages()
    print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [STARTING   ] Program started successfully...")
        
def clear_debug():
    try:
        debug_path = os.path.join(os.path.dirname(__file__), 'debug\\debug.txt')
        with open(debug_path, "w") as f:
            f.write('')
            f.close
        return 'FINISHED'
    except:
        return 'ERROR'
    
def debug_setup():
    try:
        debug_path = os.path.join(os.path.dirname(__file__), 'debug\\debug.txt')
        with open(debug_path, "r") as f:
            line = f.readlines()
            f.close
        return 'FINISHED'
    except:
        return 'ERROR'
    
def check_packages():
    # List of packages to check
    packages_to_check = ["pytesseract",
                        "datetime",
                        "pyautogui",
                        "matplotlib",
                        "python-Levenshtein",
                        "configparser",
                        "opencv-python-headless",
                        "numpy",
                        "psutil",
                        "pyperclip",
                        "requests",
                        "socketIO-client",
                        "translate",
                        "fuzzywuzzy",
                        "nltk",]

    # Function to check if a package is installed
    def is_package_installed(package_name):
        try:
            pkg_resources.get_distribution(package_name)
            return True
        except pkg_resources.DistributionNotFound:
            return False

    # Check if each package is installed
    for package in packages_to_check:
        if is_package_installed(package):
            print(f"[{TextColor.GREEN}INFO   {TextColor.RESET}] [PACKAGE    ]", package)
        else:
            print(f"[{TextColor.RED}ERROR  {TextColor.RESET}] [PACKAGE    ]", package)

    


def possibility():
    possibility_s = []

    # Create a WebDriverWait instance with a timeout
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed

    try:
        # Wait for at least one element with class "item-title" to be present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item-title")))

        # Find all elements with class "item-title"
        elements = driver.find_elements(By.CLASS_NAME, "item-title")

        # Loop through each element and collect their text values
        for element in elements:
            print(element.text)
            time.sleep(0.2)
            possibility_s.append(element.text)

    except Exception as e:
        print("Error:", str(e))
        print("Generating work load")

    return possibility_s

def possibility_1():
    possibility_s = []

    # Create a WebDriverWait instance with a timeout
    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed

    try:
        # Wait for at least one element with class "item-title" to be present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "crumb-child")))

        # Find all elements with class "item-title"
        elements = driver.find_elements(By.CLASS_NAME, "crumb-child")

        # Loop through each element and collect their text values
        for element in elements:
            print(element.text)
            time.sleep(0.2)
            possibility_s.append(element.text)

    except Exception as e:
        print("Error:", str(e))
        print("Generating work load")

    return possibility_s


def start_learning():
    print('starting learning')
    learnt = []
    
    # Find the div element with the specified class
    element = driver.find_element(By.CSS_SELECTOR, "div.prompt.ep-animate.ng-binding.ng-scope")

    # Extract and print the text content of the element
    text_content = element.text
    print("Text:", text_content)
    
    while True:
        try:
            if driver.find_element(By.ID, "start-button-main"):
                break
        
        except:
            print('continue')
        
        element = wait.until(EC.visibility_of_element_located((By.ID, "question-text")))
        text_content_prompt = element.text
        print("Text:", text_content_prompt)
        
        for sublist in learnt:
            if sublist[0] == text_content_prompt:
                answer = sublist[1]
                print("Answer:",answer)
                time.sleep(1)
                text_box = wait.until(EC.visibility_of_element_located((By.ID, "answer-text-container")))
                text_box = driver.find_element(By.ID, "answer-text-container").find_element(By.ID, "answer-text")
                text_box.send_keys(answer)
                text_box.send_keys(Keys.RETURN)
                break
            
        else:
            text_box = wait.until(EC.visibility_of_element_located((By.ID, "answer-text-container")))
            text_box = driver.find_element(By.ID, "answer-text-container").find_element(By.ID, "answer-text")
            text_box.send_keys("?")
            time.sleep(0.2)
            text_box.send_keys(Keys.RETURN)
            
            time.sleep(0.5)
            
            # Find the <tr> element with class "correct"
            tr_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "correct")))

            # Within the <tr> element, locate the <td> element with id "correct-answer-field"
            td_element = tr_element.find_element(By.ID, "correct-answer-field")

            # Extract and print the text content of the <td> element
            text_content_ans = td_element.text
            
            text = text_content_ans.split(",")[0]
            
            print("Extracted Text:", text)
            
            text_box = wait.until(EC.visibility_of_element_located((By.ID, "answer-text-container")))
            
            text_box = driver.find_element(By.ID, "answer-text-container").find_element(By.ID, "answer-text")
            
            text_box.send_keys(text)
            
            time.sleep(2)
            try:
                text_box.send_keys(Keys.RETURN)
            except:
                print('error return')
            
            learnt.append((text_content_prompt, text))
            
            print(learnt)
            
            time.sleep(0.5)
            
        time.sleep(0.5)

    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "back-arrow")))
    button.click()
    time.sleep(3)
    print('done')
    return

def find_R_W(select):
    if select == "R":
        goal = "Translate from Spanish to English"
    elif select == "W":
        goal = "Translate from English to Spanish"
        
    try:
        link = wait.until(EC.presence_of_element_located((By.ID, "full-list-switcher")))
        link.click()
    except:
        print('NO full list')
        
    buttons1 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[ng-click='starter.numberQuestions = item']")))
    buttons1[4].click()
    time.sleep(3)
    
    for i in range(5):
        buttons2 = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[ng-click='starter.selectLearningMode(item)']")))
        buttons2[i].click()
        
        element_to_wait_for = wait.until(EC.visibility_of_element_located((By.ID, "start-button-main-label")))
        
        element_to_wait_for.click()
        
        time.sleep(1)
        
        element = driver.find_element(By.CSS_SELECTOR, "div.prompt.ep-animate.ng-binding.ng-scope")

        # Extract and print the text content of the element
        text_content = element.text
        print("Text:", text_content)

        if text_content == (goal):
            break
        else:
            button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-bar-exit")))
            button.click()
            time.sleep(3)
            
    return

def click_element_text(text):
    
    # Specify the text string you are looking for
    specified_text = text

    # Use WebDriverWait to wait until the element is clickable
    element_to_wait_for = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "item-title"))
    )

    try:
        # Wait for at least one element with class "item-title" to be present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "item-title")))

        # Find all elements with class "item-title"
        elements = driver.find_elements(By.CLASS_NAME, "item-title")

        # Loop through each element and collect their text values
        for element in elements:
            if specified_text in element.text:
                # If it does, click on the element
                element.click()

    except Exception as e:
        print("Error:", str(e))
    
def main_loop_0():
    driver.get("https://app.educationperfect.com/app/")
    login()
    possibility_s = possibility()
    for i in range(len(possibility_s)):
        #element_to_wait_for = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-title")))
        #element_to_wait_for.click()
        print(possibility_s[i])
        click_element_text(possibility_s[i])
        try:
            possibility_sub = possibility()
            click_element_text(possibility_sub[i])
        except:
            print('no sub list')
        time.sleep(0.5)
        find_R_W("R")
        start_learning()
        time.sleep(5)
        find_R_W("W")
        start_learning()
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-button")))
        button.click()
        
        try:
            # Wait for the div with class "subject-title" and text "Spanish" to be clickable
            element_to_wait_for = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='subject-title' and contains(text(), 'Spanish')]"))
            )

            # Click on the div element
            element_to_wait_for.click()
            
        except Exception as e:
            print("Element not found or unable to click:", str(e))
        print('done')
        time.sleep(3)
        
    
def main_loop_1():
    url = 'https://app.educationperfect.com/app/dashboard/spanish/content/8379653/Experiencias'
    driver.get(url)
    time.sleep(2)
    login()
    possibility_s = possibility_1()
    for i in range(len(possibility_s)):
        #element_to_wait_for = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "item-title")))
        #element_to_wait_for.click()
        print(possibility_s[i])
        click_element_text(possibility_s[i])
        try:
            possibility_sub = possibility()
            click_element_text(possibility_sub[i])
        except:
            print('no sub list')
        time.sleep(0.5)
        find_R_W("R")
        start_learning()
        time.sleep(5)
        find_R_W("W")
        start_learning()
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav-button")))
        button.click()
        
        driver.get(url)
        
        print('done')
        time.sleep(3)
    
    
def login():
    print('logging in')
    # Navigate to a website

    wait = WebDriverWait(driver, 10)

    element_to_wait_for = wait.until(EC.visibility_of_element_located((By.ID, "sso-btn")))

    button_by_id = driver.find_element(By.ID, "sso-btn")
    button_by_id.click()

    element_to_wait_for = wait.until(EC.visibility_of_element_located((By.ID, "school-selection")))

    text_box = driver.find_element(By.ID, "school-selection")
    text_box.send_keys("Radford College, Canberra")

    element_to_wait_for = wait.until(EC.visibility_of_element_located((By.ID, "a8576eca-874e-481e-9a7a-2b979ea91663")))

    button_by_link_text = driver.find_element(By.ID, "a8576eca-874e-481e-9a7a-2b979ea91663")
    button_by_link_text.click()

    try:
        # Wait for the div with class "subject-title" and text "Spanish" to be clickable
        element_to_wait_for = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='subject-title' and contains(text(), 'Spanish')]"))
        )

        # Click on the div element
        element_to_wait_for.click()

    except Exception as e:
        print("Element not found or unable to click:", str(e))
    print('done')
    

setup()
time.sleep(2)
        
        
# Initialize the web driver
driver = webdriver.Edge()  # You can choose a different driver for other browsers
wait = WebDriverWait(driver, 10)

if mode == 0:
    main_loop_0()
elif mode == 1:
    main_loop_1()
    

# Close the browser window
input("Press Enter to close the browser...")
driver.quit()