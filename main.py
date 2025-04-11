import cv2

# Path to the .dav file

# import subprocess
#
# # Path to the .dav file
# input_file = "your_file.dav"
# output_file = "cvtv_19.mp4"
#
# # Use ffmpeg to convert the .dav file to a more common format (e.g., MP4)
# command = [
#     "ffmpeg",
#     "-i", file_path,       # Input file
#     "-c:v", "copy",         # Copy video stream without re-encoding
#     "-c:a", "copy",         # Copy audio stream without re-encoding
#     output_file             # Output file
# ]
#
#
#
# try:
#     subprocess.run(command, check=True)
#     print(f"File converted successfully: {output_file}")
# except subprocess.CalledProcessError as e:
#     print(f"Error during conversion: {e}")

# Open the video file

drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Initial coordinates of the box
fx, fy = -1, -1  # Final coordinates of the box

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global drawing, ix, iy, fx, fy

    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button pressed
        drawing = True
        ix, iy = x, y  # Record the initial position

    elif event == cv2.EVENT_MOUSEMOVE:  # Mouse is moving
        if drawing:
            fx, fy = x, y  # Update the final position while dragging

    elif event == cv2.EVENT_LBUTTONUP:  # Left mouse button released
        drawing = False
        fx, fy = x, y  # Finalize the box
        print(f"Box drawn from ({ix}, {iy}) to ({fx}, {fy})")

        img = frame[iy:fy, ix:fx]  # Crop the image using the box coordinates

        # Save the cropped image
        cv2.imwrite("cropped_image.png", img)


file_path = "cvtv_19.mp4"

cap = cv2.VideoCapture(file_path)
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", mouse_callback)

# Create a named window and set the mouse callback
cv2.namedWindow("Video")
cv2.setMouseCallback("Video", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break

    # Draw the box dynamically
    if drawing or (ix != -1 and iy != -1 and fx != -1 and fy != -1):
        cv2.rectangle(frame, (ix, iy), (fx, fy), (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Video", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()