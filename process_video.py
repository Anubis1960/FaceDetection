import cv2

import subprocess


def convert_mp4(file_path: str, out_path: str) -> None:
    """
    Convert a .dav file to .mp4 using ffmpeg.
    :param file_path: Path to the input .dav file.
    :param out_path: Path to the output .mp4 file.
    """
    command = [
        "ffmpeg",
        "-i", file_path,
        "-c:v", "copy",
        "-c:a", "copy",
        out_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"File converted successfully: {out_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")


def main():
    drawing = False  # True if the mouse is pressed
    ix, iy = -1, -1  # Initial position of the rectangle
    fx, fy = -1, -1  # Final position of the rectangle

    # Mouse callback function
    def mouse_callback(event, x, y):
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
    # Convert the .dav file to .mp4
    convert_mp4("input.dav", "output.mp4")

    # Process the video file
    cap = cv2.VideoCapture("output.mp4")
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


if __name__ == "__main__":
    main()
