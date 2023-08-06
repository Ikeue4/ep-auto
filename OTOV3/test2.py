import ctypes

# Load the C++ DLL
mylib = ctypes.CDLL('OTOV3\CV2.dll')

# Define the function prototype for 'add'
mylib.ping.restype = ctypes.c_int
mylib.ping.argtypes = [ctypes.c_int]

# Call the 'add' function from the C++ DLL
try:
    resalt = mylib.ping(1)
    if resalt == 1:
        print ("-----------------------\nconnected to C++ DLL\n-----------------------")
    else:
        print("-----------------------\nERROR!\n-----------------------")
except:
    print("-----------------------\nERROR!\n-----------------------")