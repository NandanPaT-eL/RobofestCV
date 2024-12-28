import cv2
import numpy as np

calibration_file = 'calibration_IMX335.npz'

try:
    data = np.load(calibration_file)
    mtx = data["camera_matrix"]
    dist = data["distortion_coefficients"]
    print("Calibration data loaded successfully.")
except FileNotFoundError:
    print(f"Error: Calibration file '{calibration_file}' not found.")
    exit()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to open the video source.")
    exit()


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

map1, map2 = cv2.initUndistortRectifyMap(mtx, dist, None, mtx, (frame_width, frame_height), cv2.CV_32FC1)

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from video source.")
        break

    undistorted_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)

    cv2.imshow("Original Frame", frame)
    cv2.imshow("Undistorted Frame", undistorted_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
