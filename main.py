import pytesseract
from PIL import ImageGrab
import pyautogui
import time
import keyboard
import sys
time.sleep(2)

while True:
    
    to_type='el helado'

    time.sleep(2)

    language_list = [["la fruta", "fruit"],['la leche', "milk"],['el pan', 'bread'],["el pastel", "cake"],
    ["el queso", "cheese"],
    ["las patatas fritas", "chips"],
    ["las verduras", "vegetables"],
    ["el chocolate", "chocolate"],
    ["el pescado", "fish"],
    ["el pollo", "the chicken"],
    ["me gusta", "i like it"],
    ["el helado", "ice cream"],
    ["no me gusta", "i don't like it"],
    ["las galletas", "biscuits"],
    ["el arroz", "rice"],
    ["me gusta", "| like it"],
    ["no me gusta", "| don't like it"],
    ]

    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
        if i[1] == result.lower():
            print("recognized text")
            print(i[0])
            to_type=i[0]
            
    pyautogui.moveTo(1650, 1400, duration=1)

    pyautogui.click()

    pyautogui.typewrite(to_type, interval=0.1)
    

    # Simulate pressing the "Enter" key
    pyautogui.press('enter')

