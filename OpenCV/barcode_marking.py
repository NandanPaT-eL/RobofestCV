import cv2
import numpy as np
import time

# data = np.load("calibration_IMX335.npz")
# mtx = data["camera_matrix"]
# dist = data["distortion_coefficients"]
# print("Calibration data loaded successfully.")

stream_url = "udp://192.168.0.2:8554"
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# map1, map2 = cv2.initUndistortRectifyMap(mtx, dist, None, mtx, (width, height), cv2.CV_32FC1)

detector = cv2.barcode_BarcodeDetector()

while True:
    ret, frame = cap.read()

    # undistorted_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    paper_contour = None
    max_area = 0
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                paper_contour = approx

    if paper_contour is not None:
        mask = cv2.drawContours(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), [paper_contour], -1, (255), thickness=cv2.FILLED)
        paper_roi = cv2.bitwise_and(frame, frame, mask=mask)
        retval, decoded_info, decoded_type, points = detector.detectAndDecodeMulti(paper_roi)

        if retval:
            for info in decoded_info:
                print("Barcode data:", info)
            break

        image_with_border = frame.copy()
        cv2.drawContours(image_with_border, [paper_contour], -1, (0, 0, 255), 3)
        cv2.imshow("Video Stream", image_with_border)
    else:
        cv2.imshow("Video Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()