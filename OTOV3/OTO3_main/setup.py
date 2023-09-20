import subprocess
import time

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='='):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()


def install_libraries(library_list):
    for library_name in library_list:
        try:
            # Use pip to install the library
            subprocess.run(["pip", "install", library_name], check=True)
            print(f"{library_name} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Error occurred while installing {library_name}.")

if __name__ == "__main__":
    libraries_to_install = [
        "numpy",
        "pytesseract",
        "Pillow",
        "PyAutoGUI",
        "time",
        "matplotlib",
        "fuzzywuzzy",
        "opencv-python"
    ]
    
    for library in libraries_to_install:
        total_iterations = 20  # Adjust this value as needed
        for i in range(total_iterations + 1):
            time.sleep(0.1)  # Simulate some work being done
            print_progress_bar(i, total_iterations, prefix=f'Installing {library}:', suffix='Complete', length=50)
        install_libraries([library])
