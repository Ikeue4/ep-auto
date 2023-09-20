import psutil
import os
import multiprocessing
import sys
import pkg_resources

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
