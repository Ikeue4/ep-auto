#include <opencv2/opencv.hpp>

void processTemplate()
{
    // Set confidence threshold
    double confidence_threshold = 8.0;

    // Load the target image
    cv::Mat target = cv::imread("C:/GitHub/ep-auto/screenshot_scan_test.png", cv::IMREAD_GRAYSCALE);

    // Create a SIFT object
    cv::Ptr<cv::SIFT> sift = cv::SIFT::create();

    // Load the template image
    cv::Mat template_image = cv::imread("C:/GitHub/ep-auto/error_windows/Web capture_4-8-2023_221021_app.educationperfect.com.jpeg", cv::IMREAD_GRAYSCALE);

    // Downscale the target and template images by a factor (e.g., 0.5 for half size)
    double scale_factor = 1;
    cv::resize(target, target, cv::Size(), scale_factor, scale_factor);
    cv::resize(template_image, template_image, cv::Size(), scale_factor, scale_factor);

    // Detect and compute keypoints and descriptors for the template and target images
    std::vector<cv::KeyPoint> keypoints_template, keypoints_target;
    cv::Mat descriptors_template, descriptors_target;
    sift->detectAndCompute(template_image, cv::noArray(), keypoints_template, descriptors_template);
    sift->detectAndCompute(target, cv::noArray(), keypoints_target, descriptors_target);

    // Create a brute-force matcher
    cv::BFMatcher bf(cv::NORM_L2);

    // Match descriptors between the template and target images
    std::vector<cv::DMatch> matches;
    bf.match(descriptors_template, descriptors_target, matches);

    // Sort the matches by distance (lower distance means better match)
    std::sort(matches.begin(), matches.end(), [](const cv::DMatch& a, const cv::DMatch& b) {
        return a.distance < b.distance;
    });

    // Select reliable matches using RANSAC
    std::vector<cv::Point2f> src_pts, dst_pts;
    for (size_t i = 0; i < matches.size(); i++) {
        src_pts.push_back(keypoints_template[matches[i].queryIdx].pt);
        dst_pts.push_back(keypoints_target[matches[i].trainIdx].pt);
    }
    cv::Mat homography = cv::findHomography(src_pts, dst_pts, cv::RANSAC, 5.0);

    // Calculate the number of inliers
    std::vector<uchar> mask(matches.size(), 0);
    cv::perspectiveTransform(src_pts, dst_pts, homography);
    for (size_t i = 0; i < matches.size(); i++) {
        if (cv::norm(dst_pts[i] - src_pts[i]) < 5.0) {  // Set a distance threshold (5.0) for inliers
            mask[i] = 1;
        }
    }
    int num_inliers = cv::countNonZero(mask);

    // Calculate the percentage of inliers
    double confidence = static_cast<double>(num_inliers) / matches.size() * 100;
    std::cout << confidence << std::endl;

    if (confidence >= confidence_threshold)
    {
        // Draw bounding box around the template in the target image
        std::vector<cv::Point2f> corners = { cv::Point2f(0, 0), cv::Point2f(0, template_image.rows),
                                             cv::Point2f(template_image.cols, template_image.rows),
                                             cv::Point2f(template_image.cols, 0) };
        std::vector<cv::Point2f> corners_transformed;
        cv::perspectiveTransform(corners, corners_transformed, homography);
        std::vector<cv::Point> int_corners_transformed;
        for (const auto& corner : corners_transformed) {
            int_corners_transformed.push_back(cv::Point(static_cast<int>(corner.x), static_cast<int>(corner.y)));
        }
        std::vector<std::vector<cv::Point>> contour = { int_corners_transformed };
        cv::polylines(target, contour, true, cv::Scalar(0, 255, 0), 3);

        // Display the target image with the bounding box
        cv::imshow("Target Image with Bounding Box", target);
        cv::waitKey(0);
    }
    
}

int main(int argc, char* argv[])
{
    // Call the function to process the template using the provided command-line argument
    processTemplate();

    return 0;
}
