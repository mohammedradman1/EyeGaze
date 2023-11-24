import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import cv2
import numpy as np
import dlib
from math import hypot
import threading 
import tensorflow as tf
import time 
import pyttsx3
import pyautogui
from tkinter import *

engine = pyttsx3.init()
newVoiceRate = 110
engine.setProperty('rate',newVoiceRate)
x=335
y=230
pyautogui.moveTo(x, y, duration = 0.3)
t = time.time()
cap = cv2.VideoCapture(1)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

interpreter = tf.lite.Interpreter(model_path='C:/courses/Graduation/firstTry/p2/CNN/model20.tflite')
interpreter.allocate_tensors()
input_d = interpreter.get_input_details()
out_d = interpreter.get_output_details()

input_shape = input_d[0]['shape'] 
inputs, outputs = [], []
sentence = ''

def text_update(word):
    global sentence
    #text.delete(0, tk.END)
    text.insert(115, word) 
    sentence += word
root = tk.Tk()
# root.resizable(False,False)
# root.geometry('982x550+250+50')

def on_enter1(e):
    e.widget['background'] = '#F0E1A8'
def on_leave1(e):
    e.widget['background'] = '#DAD2B4'

text = tk.Entry(root, width=25, bg='white', justify = CENTER,
                font = ('courier', 15, 'bold'))

# text=tk.Text(width=20, height=2, font=("Bold",20)
text.grid(row=0, column=0, columnspan=2,padx=10,pady=20,ipadx=5,ipady=12) 
text.focus_force()

def s ():
    global sentence  , engine
    print(sentence)
    if sentence != '':  
        engine.say(sentence)
        engine.runAndWait() 
speakButton = tk.Button(root, text="Speak",width=10,height=1,
        font=('Arial',22, 'bold'),
        foreground='Green',background='#DAD2B4',
        borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5, command = s) 
speakButton.grid(row=0, column=2,columnspan=2)
speakButton.bind("<Enter>", on_enter1)
speakButton.bind("<Leave>", on_leave1) 

backButton = tk.Button(root, text="Back",width=10,height=1,
        font=('Arial',22, 'bold'),
        foreground='Green',background='#DAD2B4',
        borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5) 
backButton.grid(row=0, column=4,columnspan=2)
backButton.bind("<Enter>", on_enter1)
backButton.bind("<Leave>", on_leave1) 

btn_dict = {}

letters = [['A','B','C','D','E','F'] ,
        ['G','H','I','J','K','L'] ,
        ['M','N','O','P','Q','R'],
        ['S','T','U','V','W','X'],
        ['Y','Z',' ']
        ]
    
r=0
for letterRow in letters:
    r=r+1
    col = 0 
    for letter in letterRow:
        # pass each button's text to a function
        action = lambda x = letter: text_update(x)
        # create the buttons and assign to animal:button-object dict pair
        if(letter==" "):
            btn_dict[letter] = tk.Button(root, text="Space",width=24,height=1, command=action,
                                            font=('Arial',20, 'bold'),
                                             foreground='Green',background='#DAD2B4',
                                             borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5) 
            btn_dict[letter].grid(row=r, column=col, pady=5,columnspan=3) 
        else:
            btn_dict[letter] = tk.Button(root, text=letter,width=8,height=1, command=action,
                                    font=('Arial',20, 'bold'),
                                    foreground='Green',background='#DAD2B4',
                                    borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5)
            btn_dict[letter].grid(row=r, column=col, pady=5) 
        btn_dict[letter].bind("<Enter>", on_enter1)
        btn_dict[letter].bind("<Leave>", on_leave1)
        
        col += 1 

 
def min_duration(t1, t2):
    if (t2 - t1)>= 0.05:
        return True
    else :
        return False

def iris_pos(img):
    global interpreter, out_d
    img_ar = np.asarray( img, dtype='float32')
    img_ar = np.expand_dims(img_ar, axis=0)
    interpreter.set_tensor(input_d[0]['index'], img_ar)
    interpreter.invoke()
    tflite_result = interpreter.get_tensor(out_d[0]['index'])
    output_details = interpreter.get_output_details()
    output = np.squeeze(interpreter.get_tensor(out_d[0]['index']))
    result = []
    _, topP= tf.math.top_k(tflite_result, k = 4 )
    d = {0:'Center', 1:'Down', 2:'right', 3:'Left', 4 :'up'}
    topP = np.array(topP)[0]
    return d[topP[0]]

def exi():
    global t
    t = time.time()
    b = True
    global sentence, wd
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        print(pyautogui.position())
        for face in faces:
            landmarks = predictor(gray, face)
            cimg = frame[ landmarks.part(22).y : (landmarks.part(28).y)+8, (landmarks.part(27).x) : (landmarks.part(26).x)]            
            img1 = cv2.resize(cimg,(150,150))
            gesture1 = iris_pos(img1)
            grey1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            cimg2 = frame[ landmarks.part(20).y : (landmarks.part(28).y)+8, (landmarks.part(17).x) : (landmarks.part(21).x)]            
            img2 = cv2.resize(cimg2,(150,150))
            gesture2 = iris_pos(img2)
            grey2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            if (gesture1 == 'Down') and (gesture2 == 'Down'):
                if min_duration(t, time.time()):
                    pyautogui.moveRel(0,90, duration = 0.5)
                    t = time.time()
                    print('down')

            elif (gesture1 == 'right') and  (gesture2 == 'right'):
                if min_duration(t, time.time()):
                    pyautogui.moveRel(170,0, duration = 0.2)
                    t = time.time()
                    print('right')

            elif (gesture1 == 'up') and (gesture2 == 'up'):
                if min_duration(t, time.time()):
                    print('up')
                    pyautogui.moveRel(0,-90, duration = 0.2)
                    t = time.time()
                    
            elif (gesture1 == 'Left') and (gesture2 == 'Left'):
                if min_duration(t, time.time()):
                    t = time.time()
                    print('left')
                    pyautogui.moveRel(-170,0, duration = 0.2)
            elif (gesture1 !='Down') and (gesture2 == 'Down'):
                if min_duration(t, time.time()):
                    t = time.time()
                    x,y=pyautogui.position()
                    pyautogui.click(x, y)

            else :
                if (t, time.time()):
                    print('center')

            cv2.imshow('image',grey1)
            cv2.imshow('image2',grey2)
        key = cv2.waitKey(1)
        if key == 27:
            b = False

t1 = threading.Thread(target=exi)
t1.start()
root.mainloop()

cap.release()
cv2.destroyAllWindows()