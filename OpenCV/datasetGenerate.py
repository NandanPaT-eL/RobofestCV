import cv2
import time
import os

# Directory to save captured images
dir = "Barcode_Data_q1"

# Video stream URL
url = "udp://192.168.0.2:8554"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# Ensure the directory exists
if not os.path.exists(dir):
    os.mkdir(dir)

print("Press 's' to start capturing 500 photos or 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to read frame from stream.")
        break

    # Display the current frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        print("Capturing 500 photos...")
        for count in range(1, 501):
            # Capture frame
            start = time.time()
            ret, frame = cap.read()

            if not ret:
                print("Error: Unable to read frame.")
                break

            # Save frame to file
            file_path = os.path.join(dir, f"cap_{count}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"Saved: {file_path}")

            # Display capturing progress
            cv2.imshow("Capturing", frame)

            while time.time() - start < 0.01:
                pass

        print("500 photos captured successfully.")

    elif key == ord('q'):
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()