import cv2

import subprocess
from random import randint


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


drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial position of the rectangle
fx, fy = -1, -1  # Final position of the rectangle

def main():

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

            idx = randint(0, 10000)

            cv2.imwrite(f"cropped_image{idx}.png", img)
    # Convert the .dav file to .mp4
    # convert_mp4("CH19_short.dav", "ch19.mp4")

    # Process the video file
    cap = cv2.VideoCapture("ch19.mp4")
    cv2.namedWindow("Video")
    cv2.setMouseCallback("Video", mouse_callback)

    # Set the initial position of the rectangle    paused = False
    paused = False
    rewind_frames = 30  # Number of frames to rewind (adjust as needed)

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("End of video.")
                break

        # Draw the box dynamically
        if drawing or (ix != -1 and iy != -1 and fx != -1 and fy != -1):
            cv2.rectangle(frame, (ix, iy), (fx, fy), (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("Video", frame)

        key = cv2.waitKey(2) & 0xFF  # Wait for 30ms (adjust as needed)

        # Exit on pressing 'q'
        if key == ord('q'):
            break
        elif key == ord('p'):  # Pause/resume on pressing 'p'
            paused = not paused
            print("Paused" if paused else "Resumed")
        elif key == ord('r'):  # Rewind on pressing 'r'
            current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            target_frame = max(0, current_frame - rewind_frames)  # Rewind by `rewind_frames`
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            print(f"Rewinded to frame {target_frame}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
