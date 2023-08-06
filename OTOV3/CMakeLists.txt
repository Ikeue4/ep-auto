cmake_minimum_required(VERSION 3.20)
find_package(OpenCV REQUIRED)
project(CV2)

# Find the OpenCV package
find_package(OpenCV REQUIRED)

# Add your C++ source file(s) here
add_executable(CV2 CV2.cpp)

# Link OpenCV libraries with your project
target_link_libraries(CV2 PRIVATE ${OpenCV_LIBS})