import cv2
import os

dir = "Barcode"

url = "udp://192.168.0.2:8554"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

while True:
    ret, frame = cv2.imread()
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        count = 0
        if os.path.exists(dir):
            pass
        else:
            os.mkdir(dir)
        while count <= 500:
            file_path = "captured_", count, ".jpg"
            cv2.imwrite(file_path, frame)
            count += 1
cap.release()