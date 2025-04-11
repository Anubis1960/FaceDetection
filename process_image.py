import cv2
import numpy as np


def resize(img, width, height):
    """
    Resize the image to the specified width and height.
    """
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def view_image(image, title="Image"):
    """
    Display the image in a window.
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # Load the image
    img_path = "cropped_image.png"
    img = cv2.imread(img_path)

    # Resize the image
    img = resize(img, 400, 400)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(gray, (7, 7), 2)

    view_image(blurred_image, "Blurred Image")

    # Save the blurred image
    cv2.imwrite("blurred_image.png", blurred_image)

    # Edge detection using Canny
    edges = cv2.Canny(img, 24, 200)

    view_image(edges, "Canny Edges")

    # Show difference between blurred and edges
    view_image(blurred_image - edges, "Difference between Blurred and Edges")

    # Use Laplacian to detect edges
    edges = cv2.Laplacian(blurred_image, cv2.CV_64F)
    edges = np.uint8(np.absolute(edges))

    view_image(edges, "Laplacian Edges")

    # Sharpen the image
    sharpened_image = cv2.addWeighted(blurred_image, 1.5, edges, -0.5, 0)

    view_image(sharpened_image, "Sharpened Image")


if __name__ == "__main__":
    main()
