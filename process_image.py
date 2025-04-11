import cv2
import numpy as np
import matplotlib.pyplot as plt

def resize(img, width, height):
    """
    Resize the image to the specified width and height.
    """
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

img_path = "cropped_image.png"

img = cv2.imread(img_path)

img = resize(img, 400, 400)

print(f"Image shape: {img.shape}")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and improve circle detection
blurred_image = cv2.GaussianBlur(gray, (7, 7), 2)

cv2.imshow("blurred_image", blurred_image)
cv2.waitKey(0)

cv2.imwrite("blurred_image.png", blurred_image)

edges = cv2.Canny(img,24,200)

cv2.imshow("edges", edges)
cv2.waitKey(0)

cv2.imshow("difference", blurred_image - edges)
cv2.waitKey(0)

# Use Laplacian to detect edges
edges = cv2.Laplacian(blurred_image, cv2.CV_64F)
edges = np.uint8(np.absolute(edges))

cv2.imshow("edges", edges)
cv2.waitKey(0)

sharpened_image = cv2.addWeighted(blurred_image, 1.5, edges, -0.5, 0)

cv2.imshow("sharpened_image", sharpened_image)
cv2.waitKey(0)