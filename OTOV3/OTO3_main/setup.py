import subprocess
import sys
import time
def clear_terminal():
    print("\n")
    #os.system("cls")

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█', end='\r'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}'),
    sys.stdout.flush()
    if iteration == total:
        print()


def install_library(library_name):
    try:
        # Use pip to install the library
        subprocess.run(["pip", "install", library_name], check=True)
        print(f"{library_name} installed successfully.")
    except subprocess.CalledProcessError:
        print(f"Error occurred while installing {library_name}.")

if __name__ == "__main__":
    # Example usage:
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "numpy"  # Replace "numpy" with the name of the library you want to install
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "pytesseract"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "Pillow"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "PyAutoGUI"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "time"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "matplotlib"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "fuzzywuzzy"
    install_library(library_name)
    clear_terminal()
    total_iterations = 20
    for i in range(total_iterations + 1):
        time.sleep(0.1)  # Simulate some work being done
        print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
    library_name = "opencv-python"
    install_library(library_name)