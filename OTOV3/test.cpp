#include <opencv2/opencv.hpp>

int main() {
    // Read an image from a file
    cv::Mat image = cv::imread("path/to/your/image.jpg");

    if (image.empty()) {
        std::cout << "Error: Could not open or find the image.\n";
        return -1;
    }

    // Display the image in a window
    cv::imshow("Image", image);

    // Wait for a key press and then close the window
    cv::waitKey(0);
    cv::destroyAllWindows();

    return 0;
}
