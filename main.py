import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  
cap.set(4, 720)  

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

detector = HandDetector(detectionCon=0.8)


bg_img = cv2.imread("Background (2).png")  
bg_img = cv2.resize(bg_img, (1280, 720))  

lowercase_keys = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                  ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
                  ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]

uppercase_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                  ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                  ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

keys = lowercase_keys 

finalText = ""

keyboard = Controller()
capLock = False 

def drawALL(img, buttonList, transparency=0.3):
    overlay = img.copy()  
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(overlay, button.pos, (x+w, y+h), (255, 0, 255), cv2.FILLED)
        cv2.putText(overlay, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    
    cv2.addWeighted(overlay, transparency, img, 1 - transparency, 0, img)
    
    return img

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

buttonList.append(Button([50, 500], "<-", [135, 85]))  
buttonList.append(Button([200, 500], "_", [135, 85])) 
buttonList.append(Button([350, 500], "Change Mode", [460, 85]))  
buttonList.append(Button([950, 500], "Enter", [235, 85]))  

def toggleCaps():
    global keys
    global capLock
    capLock = not capLock 
    keys = uppercase_keys if capLock else lowercase_keys  

    buttonList.clear()
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

    buttonList.append(Button([50, 500], "<-", [135, 85]))  
    buttonList.append(Button([200, 500], "_", [135, 85]))  
    buttonList.append(Button([350, 500], "Change Mode", [460, 85]))  
    buttonList.append(Button([950, 500], "Enter", [235, 85]))  

while True:
    success, img = cap.read()
    
    if not success:
        print("Error: Could not read the frame.")
        break
    
    img = cv2.flip(img, 1)
    
    hands, img = detector.findHands(img) 
    lmList = []
    
    if hands:
        hand = hands[0]  
        lmList = hand['lmList']  
        bbox = hand['bbox']      
        centerPoint = hand['center']  
        handType = hand['type']   
    
    img = cv2.addWeighted(bg_img, 0.5, img, 0.5, 0) 

    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x+w, y+h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                x1, y1 = lmList[8][0], lmList[8][1]  
                x2, y2 = lmList[12][0], lmList[12][1]  

                l, _, _ = detector.findDistance((x1, y1), (x2, y2), img)

                if l < 25:
                    if button.text == "<-":
                        finalText = finalText[:-1]  
                        keyboard.press(Key.backspace)  
                        keyboard.release(Key.backspace)
                    elif button.text == "_":
                        finalText += " "  
                        keyboard.press(Key.space)  
                        keyboard.release(Key.space)
                    elif button.text == "Change Mode":
                        toggleCaps()  
                    elif button.text == "Enter":
                        finalText += "\n"  
                        keyboard.press(Key.enter)  
                        keyboard.release(Key.enter)
                    else:
                        finalText += button.text
                        keyboard.press(button.text)  
                        keyboard.release(button.text)  
                    sleep(0.2)
                    
                    cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.rectangle(img, (50, 350), (1000, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
