from PIL import Image
import pytesseract
import argparse
import cv2
import os
import imutils
import datetime
import threading
import re
from Tkinter import *
from gtts import gTTS 
from playsound import playsound

DEBUG = False

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

# initialize a rectangular and square structuring kernel
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
img_counter = 0

def play_sound(sound):
    tts = gTTS(text=sound, lang='en')
    tts.save("welcome.mp3")
    playsound('welcome.mp3')

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
    	# SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        
        cv2.imwrite(img_name, frame)

        orig_text = pytesseract.image_to_string(img_name)
        gray = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
        black_text = pytesseract.image_to_string(blackhat)

        if DEBUG:
            print("********************************original")
            print orig_text
            print("********************************grayscale")
            print pytesseract.image_to_string(gray)
            print("********************************gaussian blur")
            print pytesseract.image_to_string(gray)
            print("********************************blackhat")
            print black_text

        orig_predict = re.findall(r"[A-Z]{3}201\d{4}", orig_text)
        black_predict = re.findall(r"[A-Z]{3}201\d{4}", black_text)
        
        currentDT = datetime.datetime.now()

        if len(orig_predict) < 1 or len(black_predict) < 1:
            print("==============================================")
            print("Please try again!!")
            playsound("try_again.mp3")
            print("==============================================")            
        elif orig_predict[0] == black_predict[0]:
            welcome_text = "Welcome " + orig_predict[0]
            print("==============================================")
            print(welcome_text)
            # play_sound(welcome_text)
            log_file = open("log.txt","w")
            log_file.write("ENTRY\t" + orig_predict[0] + "\t" + str(currentDT))
            log_file.close()
            print("Entry logged at " + str(currentDT))
            print("==============================================")
        else:
            print("==============================================")
            print("Please try again!!")
            playsound("try_again.mp3")
            print("==============================================")

        cv2.imwrite('blackhat.jpg', blackhat)
        # print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()