import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import time 
import pyttsx3
import pyautogui
from trie import TextEngine
from eyeGaze import EyeGaze
import threading 
# controller frame of all frames to invoke the next frame
sentence = ''
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
        self.eyetracker = EyeGaze()
        self.wd_list = []
        self.move_to_start = False
        self.inputSeq = ''
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
        for F in (StartPage, Page1, Page2, Page3, manualKB, InputMethod):
  
            frame = F(container, self)
  
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
        # self.current_frame = self.frames[InputMethod]  
        self.show_frame(InputMethod)
        self.t1 = threading.Thread(target=self.eyetracker.gaze)
        self.t1.start()
  
    def show_frame(self, cont):
        
        # print(type(cont))
        frame = self.frames[cont]
        self.f = frame.__str__()
        self.current_frame = frame
        self.eyetracker.set_frame(frame)
        if cont == Page1:
            self.current_frame.en.delete(0,'end')
            self.current_frame.en.insert(0,sentence)
        time.sleep(0.5)
        frame.tkraise()
# manual keyboard interface 
class manualKB(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.sentence = ''
        self.engine = pyttsx3.init() 
        self.engine.setProperty('rate',110)
        self.x=335
        self.y=230
        pyautogui.moveTo(self.x, self.y, duration = 0.5)
        self.curser = 3 
        self.displayKB()
        self.text_update("")
    def on_enter1(self, e):
        e.widget['background'] = 'light blue'
    def on_leave1(self, e):
        e.widget['background'] = 'white'
    def s (self):
        global sentence  
        print(sentence)
        if sentence != '':  
            self.engine.say(sentence)
            self.engine.runAndWait() 

        
    def displayKB(self):
        # action = lambda x = letter: self.text_update(x)
        self.text = tk.Entry(self, width=25, bg='white', justify = CENTER,
        font = ('courier', 15, 'bold'))

        # text=tk.Text(width=20, height=2, font=("Bold",20)
        self.text.grid(row=0, column=0, columnspan=2,padx=10,pady=20,ipadx=5,ipady=12) 
        self.text.focus_force()
        self.speakButton = tk.Button(self, text="Speak",width=10,height=1,
        font=('Arial',22, 'bold'),
        foreground='Green',background='white',
        borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5, command= self.s) 
        self.speakButton.grid(row=0, column=2,columnspan=2)
        self.backButton = tk.Button(self, text="Back",width=10,height=1,
        font=('Arial',22, 'bold'),
        foreground='Green',background='white',
        borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5, command= self.leave_page) 
        self.backButton.grid(row=0, column=4,columnspan=2)
        self.speakButton.bind("<Enter>", self.on_enter1)
        self.speakButton.bind("<Leave>", self.on_leave1) 
        self.backButton.bind("<Enter>", self.on_enter1)
        self.backButton.bind("<Leave>", self.on_leave1) 
        self.btn_dict = {}

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
                action = lambda x = letter: self.text_update(x)
                # create the buttons and assign to animal:button-object dict pair
                if(letter==" "):
                    self.btn_dict[letter] = tk.Button(self, text="Space",width=24,height=1, command=action,
                                                    font=('Arial',20, 'bold'),
                                                    foreground='Green',background='white',
                                                    borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5) 
                    self.btn_dict[letter].grid(row=r, column=col, pady=5,columnspan=3) 
                else:
                    self.btn_dict[letter] = tk.Button(self, text=letter,width=8,height=1, command=action,
                                            font=('Arial',20, 'bold'),
                                            foreground='Green',background='white',
                                            borderwidth=5,relief=GROOVE, highlightthickness=5,padx=2, pady=5)
                    self.btn_dict[letter].grid(row=r, column=col, pady=5) 
                self.btn_dict[letter].bind("<Enter>", self.on_enter1)
                self.btn_dict[letter].bind("<Leave>", self.on_leave1)
                
                col += 1 
    
    def text_update(self, word):
        global sentence
        sentence = sentence + word
        self.text.insert(115, word.lower()) 
    def leave_page(self):
        self.controller.show_frame(StartPage)
        
    def move_currsor(self, x_dir, y_dir):
        pyautogui.moveRel(x_dir,y_dir, duration = 0.2)


selected_button = None
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.curser = 2
        self.count = 0
        self.selected_button = None
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)
        self.btn1= tk.Button(self, text= "Speak!", width=15, height=7, command = lambda : self.speak(self.btn1))
        self.btn1.grid(row=0, column=1)
        self.btn2= tk.Button(self, text= "Manual input", width= 15, height=7, command = lambda : self.changeBG(manualKB, self.btn2))
        self.btn2.grid(row=1, column=0)
        self.btn3= tk.Button(self, text= "Predictive input", width=15, height=7, command = lambda : self.changeBG(Page1, self.btn3))
        self.btn3.grid(row=1, column=2)
        self.btn4= tk.Button(self, text= "Delete", width=15, height=7, command = lambda : self.changeBG(Page3, self.btn4))
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
        # self.changeBG(butn)   
        self.count = 0
        if butn == self.btn3:
            self.controller.move_to_start = False
        self.selected_button.config(bg = 'white')
        self.controller.show_frame(page)
        move_to_start = False
        if page == Page2:
            self.controller.move_to_start = False
            self.controller.current_frame.update_buttons(self.controller.wd_list)
       
    def changeBG(self, page, button):
        if self.selected_button is not None:
            self.selected_button.config(bg = 'white')
        button.config(bg="light blue")
        self.selected_button = button
        self.count += 1
        if self.count > 1 :
            self.next_page(page, button)

# Letters frame (Keyboard)
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.te = TextEngine()
        self.inputSeq = ''
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 3, weight = 1)
        self.count = 0
        self.move_to_start = False
        self.selected_button = None
        self.en = tk.Entry(self)
        self.en.grid(row = 0, column = 1, sticky=N+E+W)
        self.btn1= tk.Button(self, text= "A B C \nD E F ", width=15, height=7, command = lambda : self.getWd(self.btn1,'1'))
        self.btn1.grid(row=1, column=1)
        self.btn2= tk.Button(self, text= "G H I \nJ K L", width= 15, height=7, command = lambda : self.getWd(self.btn2,'2'))
        self.btn2.grid(row=2, column=0)
        self.btn3= tk.Button(self, text= "M N O \nP Q R S", width=15, height=7, command = lambda : self.getWd(self.btn3,'3'))
        self.btn3.grid(row=2, column=2)
        self.btn4= tk.Button(self, text= "T U V \nW X Y Z", width=15, height=7, command = lambda : self.getWd(self.btn4,'4'))
        self.btn4.grid(row=3, column=1)
        self.centerBtn = tk.Button(self, text= '',width= 15, height=7, command = self.next_page)
        self.centerBtn.grid(row=2, column=1)

        self.curser = 2

    def getWd(self, button, gesture):
        self.count = 0
        self.move_to_start = True
        self.controller.move_to_start = True
        self.gesturesToWord(gesture)
        if self.selected_button is not None :
            self.selected_button.config(bg="white")
        button.config(bg="light blue")
        self.selected_button = button

    def next_page(self):
        if self.count > 20 and self.controller.move_to_start :
            self.count = 0
            self.selected_button.config(bg = 'white')
            self.controller.show_frame(Page2)
            self.controller.current_frame.update_buttons(self.controller.wd_list)
            # selected_button = None
        elif self.count > 1 and self.selected_button is not None:
            self.selected_button.config(bg = 'white')
            self.count += 1
        else:
            self.count += 1
    def gesturesToWord(self, gesture):
        self.controller.inputSeq = self.controller.inputSeq + gesture
        self.te.text_comp(self.controller.inputSeq)
        self.controller.wd_list = self.te.words
        print(self.controller.inputSeq)
        print(self.te.words)
# Words frame                
class Page2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)       
        self.controller = controller
        self.curser = 2
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)
        self.btn1= tk.Button(self, text= '', width=15, height=7, command = lambda : self.update_sentence(1))
        self.btn1.grid(row=0, column=1)        
        self.btn2= tk.Button(self, text= '', width= 15, height=7, command = lambda : self.update_sentence(2))
        self.btn2.grid(row=1, column=0)
        self.btn3= tk.Button(self, text= '', width=15, height=7, command = lambda : self.update_sentence(3))
        self.btn3.grid(row=1, column=2)
        self.btn4= tk.Button(self, text= "Back", width=15, height=7, command = lambda : self.next_page(4))
        self.btn4.grid(row=2, column=1)
        self.centerBtn = tk.Button(self, text= '',width= 15, height=7) 
        self.centerBtn.grid(row=1, column=1)
        self.btn1.bind("<Enter>", self.on_enter1)
        self.btn2.bind("<Leave>", self.on_leave1) 
    def __str__(self):
        return 'Page2' 
    def update_buttons(self, wl):
        global inputSeq
        self.btn1['text'] = wl[0]
        self.btn2['text'] = wl[1]
        self.btn3['text'] = wl[2]
    def update_sentence(self, btnNum):
        global sentence
        if btnNum == 1:
            sentence = sentence+" " + self.btn1['text']
            self.controller.inputSeq = ''
            self.controller.wd_list = []
            
        elif btnNum == 2 :
            sentence = sentence +' '+ self.btn2['text']
            self.controller.inputSeq = ''
            self.controller.wd_list = []
            
        else :
            sentence = sentence +' '+ self.btn3['text']
            self.controller.inputSeq = ''
            self.controller.wd_list = []

        self.next_page(btnNum)
    def next_page(self, btn):
        global wd_list, words_const
        
        if btn == 4:
            # words_const = words_const + 1
            # if len(wd_list) >= words_const :
            #     self.controller.move_to_start = False
            #     self.update_buttons(wd_list[words_const - 1 : words_const +3])
            # else :
            #     self.controller.show_frame(Page1)
            #     self.controller.inputSeq = ''
            self.controller.move_to_start = False
            self.controller.show_frame(Page1)
        else :
            self.controller.show_frame(StartPage)
            self.controller.inputSeq = ''
    def on_enter1(self, e):
        e.widget['background'] = '#F0E1A8'
    def on_leave1(self, e):
        e.widget['background'] = '#DAD2B4'

# deleting options frame
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.curser = 2
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.rowconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        tk.Grid.columnconfigure(self, 2, weight = 1)
        tk.Grid.rowconfigure(self, 2, weight = 1)
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

class InputMethod(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Grid.rowconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 1, weight = 1)
        self.btn2= tk.Button(self, text= 'Manual input', width=15, height=7, command = lambda : self.choose_input(self.btn2))
        self.btn2.grid(row=0, column=0, sticky=N+S+E+W) 
        self.btn3= tk.Button(self, text= 'Predictive input', width=15, height=7, command = lambda : self.choose_input(self.btn3))
        self.btn3.grid(row=0, column=1, sticky=N+S+E+W) 
        self.count = 0
        self.selected_button = None
        self.curser = 1

    def next_page(self, btn):
        self.selected_button.config(bg = 'white')
        self.count = 0
        if btn  == self.btn2    :
            self.controller.show_frame( manualKB)
        else:
            self.controller.show_frame(Page1)

    def choose_input(self, button):
        
        if self.selected_button is not None:
            self.selected_button.config(bg = 'white')
        button.config(bg="light blue")
        self.selected_button = button
        self.count += 1
        if self.count > 1 :
            self.next_page(button)
