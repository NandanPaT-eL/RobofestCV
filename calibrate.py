import numpy as np
import cv2 as cv
import glob

chessSize = (8, 6)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

obj = np.zeros((chessSize[0] * chessSize[1], 3), np.float32)
obj[:, :2] = np.mgrid[0:chessSize[0], 0:chessSize[1]].T.reshape(-1, 2)

objPt = []  # 3D points
imgPt = []  # 2D points

images = glob.glob("Assets/*.jpg")

for image_path in images:
    print("Processing: ", image_path)
    img = cv.imread(image_path)
    if img is None:
        print("Error loading image: ", image_path)
        continue

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, chessSize, None)

    if ret:
        objPt.append(obj)
        refined_corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgPt.append(refined_corners)

        # Draw and display corners
        cv.drawChessboardCorners(img, chessSize, refined_corners, ret)
        cv.imshow('Chessboard corners', img)
        cv.waitKey(500)
    else:
        print("Chessboard corners not found in ", image_path)

cv.destroyAllWindows()

# Perform camera calibration and save data
if len(objPt) > 0 and len(imgPt) > 0:
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPt, imgPt, gray.shape[::-1], None, None)

    if ret:
        print("Camera Calibration Successful")
        print("\nCamera Matrix:\n", mtx)
        print("\nDistortion Coefficients:\n", dist)

        # Save calibration data
        calibration_data_path = "calibration_IMX335.npz"
        np.savez(calibration_data_path, camera_matrix=mtx, distortion_coefficients=dist,
                 rotation_vectors=rvecs, translation_vectors=tvecs)
        print("Calibration data saved to ", calibration_data_path)
    else:
        print("Camera calibration failed.")
else:
    print("Not enough valid image points for calibration.")

