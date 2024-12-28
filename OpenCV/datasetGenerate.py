import cv2
import os
import time

dir = "Barcode"

stream_url = "udp://192.168.0.2:8554"
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

if not os.path.exists(dir):
    os.mkdir(dir)

print("Press 's' to capture 500 photos")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        print("Capturing 500 photos...")
        for count in range(1, 501):
            file_path = os.path.join(dir, f"captured_{count}.jpg")
            cv2.imwrite(file_path, frame)
            print("Saved: ", file_path)
            time.sleep(0.02)
        print("500 photos captured successfully.")

    elif key == ord('q'):
        print("Exiting...")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()