import cv2
import time

def Webcam():
    cap = cv2.VideoCapture(0)
    time.sleep(1)

    result, image = cap.read()

    if not result:
        print("No image detected. Please! try again")
    
    return image