import cv2
import os
import csv

image_directory = "Barcode"
output_csv_file = "output.csv"

detector = cv2.barcode_BarcodeDetector()

with open(output_csv_file, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Image Name", "Detected Barcodes"])

image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

if not image_files:
    print("Error: No image files found in the directory.")
    exit()

for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Unable to read image ", image_file,". Skipping.")
        continue

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
        mask = cv2.drawContours(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), [paper_contour], -1, (255), thickness=cv2.FILLED)
        paper_roi = cv2.bitwise_and(image, image, mask=mask)
        retval, decoded_info, decoded_type, points = detector.detectAndDecodeMulti(paper_roi)
    barcode_data = ", ".join(decoded_info) if retval else "No barcode detected"

    with open(output_csv_file, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([image_file, barcode_data])
    print("Processed image ", image_file, ": ", barcode_data)

print("Processing complete. Results saved in ", output_csv_file)