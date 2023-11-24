import tkinter as tk
import cv2
import numpy as np
import dlib
import threading 
import tensorflow as tf
import time 
import pyttsx3
from tkinter import *
count = 0
move_to_start = False
words_const = 3
wd_list = []
current_frame = None

engine = pyttsx3.init()
newVoiceRate = 110
engine.setProperty('rate',newVoiceRate)

t = time.time()
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

interpreter = tf.lite.Interpreter(model_path ='C:/courses/Graduation/firstTry/p2/CNN/model20.tflite')
interpreter.allocate_tensors()
input_d = interpreter.get_input_details()
out_d = interpreter.get_output_details()

input_shape = input_d[0]['shape'] 
inputs, outputs = [], []


inputSeq = ''
selected_button = None
sentence = ''
wd = ''
wdDict = {}

# Word class used to represent a word and its frequency
class Word():
    frq = 0
    def __init__(self, wd):
        self.wd = wd
        self.freq = 1
    def setFreq(self, freq):
        self.freq = freq
    def getFreq(self):
        return self.freq
    
    def __lt__(self, newW):
        return self.getFreq() < newW.getFreq()
    def __gt__(self, newW):
        return self.getFreq() > newW.getFreq()
    def __le__(self, newW):
        return self.getFreq() <= newW.getFreq()
    def __ge__(self, newW):
        return self.getFreq() >= newW.getFreq()
    def __eq__(self, newW):
        return self.getFreq()== newW.getFreq()
    def getName(self):
        return self.wd
    
    def __iter__(self):
        return self

    def compare(self, woord):
        if self.wd == woord.wd:
            return True
        else :
            return False

def min_duration(t1, t2):
    if (t2 - t1)>= 0.9:
        return True
    else :
        return False

# Generates a sequence for a word 
def seqGen(seq):
    sr = ''
    for i in seq:
        sr = sr + str(seqDigit(i)) 
    return sr  

# Maps a letter to its corrsponding keyboard number
def seqDigit(char):
    switcher = {
        'a' : 1,
        'b' : 1, 
        'c' : 1,
        'd' : 1,
        'e' : 1,
        'f' : 1,
        
        'g' : 2,
        'h' : 2,
        'i' : 2,
        'j' : 2,
        'k' : 2,
        'l' : 2,

        'm' : 3,
        'n' : 3,
        'o' : 3,
        'p' : 3,
        'q' : 3,
        'r' : 3,
        's' : 3,

        't' : 4,
        'u' : 4,
        'v' : 4,
        'w' : 4,
        'x' : 4,
        'y' : 4,
        'z' : 4
    }
    return switcher.get(char,'')

# Inserting pair of a sequence and word to the dictionary 
def insert(seq, w):
    newWd = Word(w)
    if wdDict.__contains__(seq):
        wd_list = wdDict.__getitem__(seq)    
        for eachwd in wd_list:
            if eachwd.compare(newWd):
                newWd = eachwd
                newWd.setFreq(newWd.getFreq()+1)
                wd_list.remove(eachwd)
        wd_list.append(newWd)  
        wd_list = sorted(wd_list)
        wdDict.__setitem__(seq, wd_list)    
    else :
        l = []
        l.append(newWd)
        wdDict.update({seq :l})

def gesturesToWord(gesture):
    global inputSeq, selected_button, wd_list
    inputSeq = inputSeq + gesture
    s=''
    if wdDict.__contains__(inputSeq):
        wd_list = []
        # wDic = wdDict[inputSeq]
        for w in reversed(wdDict[inputSeq]):
            wd_list.append(w.getName())
        
    # else:
    #     inputSeq = ''

# to change the back ground of the btn 
def change_selected_button(button, gesture):
    global selected_button
    if selected_button is not None :
        selected_button.config(bg="white")
    button.config(bg="light blue")
    selected_button = button

# loading the text data to preaper it 
file = open('13.txt', encoding="utf8")
for line in file:
    for word in line.split():
         wd = word.lower()
         
         seq = seqGen(wd)
         insert(seq, wd)         

# Contoler frame of all frames to invoke the next frame
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
         
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (StartPage, Page1, Page2, Page3):
  
            frame = F(container, self)
  
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Page1)
  
    def show_frame(self, cont):
        global current_frame, time, sentence
        # print(type(cont))
        frame = self.frames[cont]
        self.f = frame.__str__()
        current_frame = frame
        if cont == Page1:
            current_frame.en.delete(0,'end')
            current_frame.en.insert(0,sentence)
        time.sleep(0.5)
        frame.tkraise()

#  Options frame  
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.btn1= tk.Button(self, text= "Speak!", width=15, height=7, command = lambda : self.speak(self.btn1))
        self.btn1.grid(row=0, column=1)
        self.btn2= tk.Button(self, text= "Keyboard", width= 15, height=7, command = lambda : self.next_page(Page1, self.btn2))
        self.btn2.grid(row=1, column=0)
        self.btn3= tk.Button(self, text= "Choose word", width=15, height=7, command = lambda : self.next_page(Page2, self.btn3))
        self.btn3.grid(row=1, column=2)
        self.btn4= tk.Button(self, text= "Delete", width=15, height=7, command = lambda : self.next_page(Page3, self.btn4))
        self.btn4.grid(row=2, column=1)  
        self.centerBtn = tk.Button(self, text= '',width= 15, height=7) 
        self.centerBtn.grid(row=1, column=1)
    def __str__(self):
        return 'StartPage'          
    def speak(self, butn) :
        global sentence, engine, inputSeq
        self.changeBG(butn)
        if sentence != '':
            engine.say(sentence)
            engine.runAndWait() 
            sentence = ''
            inputSeq = ''
            self.controller.show_frame(Page1)
    def next_page(self, page, butn):
        global current_frame, time,wd_list, move_to_start       
        self.changeBG(butn)      
        self.controller.show_frame(page)
        move_to_start = False
        if page == Page2:
            current_frame.update_buttons(wd_list[0:3])
    def changeBG(self, butn):
        global selected_button
        if selected_button is not None :
            selected_button.config(bg="white")
        butn.config(bg="light blue")
        selected_button = butn

# Letters frame (Keyboard)
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 3, weight = 1)


        self.en = tk.Entry(self)
        self.en.grid(row = 0, column = 1,sticky=N+S+E+W)
        self.btn1= tk.Button(self, text= "A B C \nD E F ", width=15, height=7, command = lambda : self.getWd(self.btn1,'1'))
        self.btn1.grid(row=1, column=1, sticky=N+S+E+W)
        self.btn2= tk.Button(self, text= "G H I \nJ K L", width= 15, height=7, command = lambda : self.getWd(self.btn2,'2'))
        self.btn2.grid(row=2, column=0, sticky=N+S+E+W)
        self.btn3= tk.Button(self, text= "M N O \nP Q R S", width=15, height=7, command = lambda : self.getWd(self.btn3,'3'))
        self.btn3.grid(row=2, column=2, sticky=N+S+E+W)
        self.btn4= tk.Button(self, text= "T U V \nW X Y Z", width=15, height=7, command = lambda : self.getWd(self.btn4,'4'))
        self.btn4.grid(row=3, column=1, sticky=N+S+E+W)
        self.centerBtn = tk.Button(self, text= '',width= 15, height=7, command = self.next_page)
        self.centerBtn.grid(row=2, column=1, sticky=N+S+E+W)
    def __str__(self):
        return "Page1"
    def p(self) :
        print('Page1')
    def getWd(self, button, gesture):
        global selected_button, count, move_to_start
        count = 0
        move_to_start = True
        if selected_button is not None :
            selected_button.config(bg="white")
        button.config(bg="light blue")
        selected_button = button
        gesturesToWord(gesture)
    def next_page(self):
        global count, move_to_start, selected_button
        if count > 20 and move_to_start:
            count = 0
            self.controller.show_frame(StartPage)
            # selected_button = None
        else:
            count += 1

# Words frame                
class Page2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)       
        self.controller = controller
        self.btn1= tk.Button(self, text= '', width=15, height=7, command = lambda : self.update_sentence(1))
        self.btn1.grid(row=0, column=1)        
        self.btn2= tk.Button(self, text= '', width= 15, height=7, command = lambda : self.update_sentence(2))
        self.btn2.grid(row=1, column=0)
        self.btn3= tk.Button(self, text= '', width=15, height=7, command = lambda : self.update_sentence(3))
        self.btn3.grid(row=1, column=2)
        self.btn4= tk.Button(self, text= "More", width=15, height=7, command = lambda : self.next_page(4))
        self.btn4.grid(row=2, column=1)
        self.centerBtn = tk.Button(self, text= '',width= 15, height=7) 
        self.centerBtn.grid(row=1, column=1)
    def __str__(self):
        return 'Page2' 
    def update_buttons(self, wl):
        global inputSeq
        self.btn1['text'] = wl[0]
        self.btn2['text'] = wl[1]
        self.btn3['text'] = wl[2]
    def update_sentence(self, btnNum):
        global sentence, inputSeq
        if btnNum == 1:
            self.changeBG(self.btn1)
            sentence = sentence+" " + self.btn1['text']
            inputSeq = ''
            
        elif btnNum == 2 :
            self.changeBG(self.btn2)
            sentence = sentence +' '+ self.btn2['text']
            inputSeq = ''
            
        else :
            self.changeBG(self.btn3)
            sentence = sentence +' '+ self.btn3['text']
            inputSeq = ''
        self.next_page(btnNum)
    def next_page(self, btn):
        global wd_list, words_const
        
        if btn == 4:
            words_const = words_const + 1
            if len(wd_list) >= words_const :
                self.update_buttons(wd_list[words_const - 1 : words_const +3])
            else :
                self.controller.show_frame(Page1)
        else :
            self.controller.show_frame(Page1)
    def changeBG(self, butn):
        global selected_button
        if selected_button is not None :
            selected_button.config(bg="white")
        butn.config(bg="light blue")
        selected_button = butn

# deleting options frame
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.btn1= tk.Button(self, text= 'Delete letters', width=15, height=7, command = lambda : self.update_sentence(1))
        self.btn1.grid(row=0, column=1)        
        self.btn2= tk.Button(self, text= 'Delete last word', width= 15, height=7, command = lambda : self.update_sentence(2))
        self.btn2.grid(row=1, column=0)
        self.btn3= tk.Button(self, text= 'Delete last letter', width=15, height=7, command = lambda : self.update_sentence(3))
        self.btn3.grid(row=1, column=2)
        self.btn4= tk.Button(self, text= "Back", width=15, height=7, command = lambda : self.next_page())
        self.btn4.grid(row=2, column=1)
        self.centerBtn = tk.Button(self, text= 'select',width= 15, height=7) 
        self.centerBtn.grid(row=1, column=1)     
    def update_sentence(self, btnNum):
        global sentence, inputSeq
        if btnNum == 1:
            # to reset the input sequence 
            inputSeq = ''
            self.next_page()
        elif btnNum == 2 :
            # to deletet the last sentence 
            sentence = sentence.rsplit(' ', 1)[0]
            self.next_page()
        elif btnNum == 3:
            # to delete the last letter to the sequence 
            inputSeq = inputSeq[0:len(inputSeq)-1]
            self.next_page()
        else:
            self.next_page()
    def next_page(self):
        self.controller.show_frame(StartPage)
app = tkinterApp()

# Based on a eye image this method determins the postion of of the iris postion using the tensorflow trained model
def iris_pos(img):
    global interpreter, out_d
    img_ar = np.asarray( img, dtype ='float32')
    img_ar = np.expand_dims(img_ar, axis=0)
    interpreter.set_tensor(input_d[0]['index'], img_ar)
    interpreter.invoke()
    tflite_result = interpreter.get_tensor(out_d[0]['index'])
    output_details = interpreter.get_output_details()
    output = np.squeeze(interpreter.get_tensor(out_d[0]['index']))
    result = []
    _, topP= tf.math.top_k(tflite_result, k = 4)
    d = {0:'Center', 1:'Down', 2:'right', 3:'Left', 4 :'up'}
    topP = np.array(topP)[0]
    return d[topP[0]]

# Observing the eye movement 
def eye_gaze():
    global inputSeq, t, current_frame
    t = time.time()
    b = True
    global sentence, wd
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            cimg = frame[ landmarks.part(22).y : (landmarks.part(28).y)+8, (landmarks.part(27).x) : (landmarks.part(26).x)]            
            img1 = cv2.resize(cimg,(150,150))
            gesture1 = iris_pos(img1)
            grey1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            cimg2 = frame[ landmarks.part(20).y : (landmarks.part(28).y)+12, (landmarks.part(17).x) : (landmarks.part(21).x)]            
            img2 = cv2.resize(cimg2,(150,150))
            gesture2 = iris_pos(img2)
            grey2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            if (gesture1 == 'Down') and (gesture2 == 'Down'):
                if min_duration(t, time.time()):
                    current_frame.btn4.invoke()
                    t = time.time()
            elif (gesture1 == 'right') and  (gesture2 == 'right'):
                if min_duration(t, time.time()):
                    current_frame.btn3.invoke()
                    t = time.time()
            elif (gesture1 == 'up') and (gesture2 == 'up'):
                if min_duration(t, time.time()):
                    current_frame.btn1.invoke()
                    t = time.time()
            elif (gesture1 == 'Left') and (gesture2 == 'Left'):
                if min_duration(t, time.time()):
                    current_frame.btn2.invoke()
                    t = time.time()
            else :
                if (t, time.time()):
                    current_frame.centerBtn.invoke()
                    # print('center')
            # time.sleep(0.1)
            # cv2.imshow('image',grey1)
            # cv2.imshow('image2',grey2)
            cv2.imshow('face', gray)
        key = cv2.waitKey(1)
        if key == 27:
            b = False

t1 = threading.Thread(target=eye_gaze)
t1.start()
app.eval('tk::PlaceWindow . center')
app.mainloop()