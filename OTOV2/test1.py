import cv2
import numpy as np
import pyautogui
import matplotlib.image as mpimg
import time 

def process_template(template_file):
    time.sleep(1)
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot_scan.png")
    
    img_path = 'screenshot_scan.png'
    img = mpimg.imread(img_path)
    confidence_threshold = 30
    # Load the target image
    target = cv2.imread('screenshot_scan.png', 0)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Load the template image
    template = cv2.imread(template_file, 0)

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
    #print('checking confidence')
    #print(confidence, template_file)
    print(confidence)
    if confidence >= confidence_threshold:
        print('success')
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

while True:
    process_template('C:\GitHub\ep-auto\error_windows\Web capture_3-8-2023_183936_app.educationperfect.com.jpeg')
    process_template('C:\GitHub\ep-auto\error_windows\Web capture_3-8-2023_17436_app.educationperfect.com.jpeg')