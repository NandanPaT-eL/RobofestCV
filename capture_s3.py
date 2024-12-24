#Capturing video and saving it into 30 seconds video clips so that it could be uploaded on Amazon S3 bucket

import cv2
import time
import os

def main():
    if not os.path.exists('Videos'):
        os.makedirs('Videos')
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        return
    
    seq = 1
    start = time.time()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'Videos/video_{seq}.mp4', fourcc, 20.0, (640, 480))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error!")
            break
        out.write(frame)
        if time.time() - start >= 30:
            out.release()
            seq += 1
            out = cv2.VideoWriter(f'Videos/video_{seq}.mp4', fourcc, 20.0, (640, 480))
            start = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()