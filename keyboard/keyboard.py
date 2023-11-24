from tkinter import *
import ttkthemes as td
from tkinter import ttk

from tensorflow.keras.models import load_model
import numpy as np
import pickle

# Load the model and tokenizer
model = load_model('next_words.h5')
tokenizer = pickle.load(open('token.pkl', 'rb'))

root = td.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root.title('EYE TRACKER')
root.config(bg='whitesmoke')
root.resizable(0,0)
root.geometry("1350x500")

n=' '
pre=""
global predicted_word
def select(value):

    global pre
    if value == 'Space':
        textarea.insert(INSERT, ' ')
        
        


    elif value == 'Enter':
        textarea.insert(INSERT, '\n')

    elif value == 'Tab':
        textarea.insert(INSERT, '\t')

    elif value == 'Del':
        textarea.delete(1.0, END)

    elif value == 'Backs':
        i = textarea.get(1.0, END)
        newtext = i[:-2]

        textarea.delete(1.0, END)
        textarea.insert(INSERT, newtext)

    elif value == 'Shift ↑':
        varRow = 2
        varColumn = 0

        for button in leftShiftButtons:

            command = lambda x=button: select(x)
            if button != 'Space':
                ttk.Button(root, text=button, command=command, width=10, ).grid(row=varRow, column=varColumn)

            varColumn += 1
            if varColumn > 14:
                varColumn = 0
                varRow += 1

    elif value == '↑ Shift':
        varRow = 2
        varColumn = 0

        for button in buttons:

            command = lambda x=button: select(x)
            if button != 'Space':
                ttk.Button(root, text=button, command=command, width=10, ).grid(row=varRow, column=varColumn)

            varColumn += 1
            if varColumn > 14:
                varColumn = 0
                varRow += 1

    elif value == 'Caps':

        varRow = 2
        varColumn = 0

        for button in capsButtons:

            command = lambda x=button: select(x)
            if button != 'Space':
                ttk.Button(root, text=button, command=command, width=10, ).grid(row=varRow, column=varColumn)

            varColumn += 1
            if varColumn > 14:
                varColumn = 0
                varRow += 1

    elif value == 'CAPS':

        varRow = 2
        varColumn = 0

        for button in buttons:

            command = lambda x=button: select(x)
            if button != 'Space':
                ttk.Button(root, text=button, command=command, width=10, ).grid(row=varRow, column=varColumn)

            varColumn += 1
            if varColumn > 14:
                varColumn = 0
                varRow += 1


    else:
        textarea.insert(INSERT, value)
    n=textarea.get(1.0,END)
    print(n)
    textarea.focus_set()
   
    n = n.split(" ")
    n= n[-3:]
    print(n)
    pre=Predict_Next_Words(model, tokenizer, n)
    dynamicButton(pre)
    

def Predict_Next_Words(model, tokenizer, text):

  sequence = tokenizer.texts_to_sequences([text])
  sequence = np.array(sequence)
  preds = np.argmax(model.predict(sequence))
  predicted_word = ""
  
  for key, value in tokenizer.word_index.items():
      con=1
      if value == preds:
          predicted_word = key
          print("### " + key + " ###" +"\n")
          con=con+1
          if(con!=3):
              continue
          break
              
          
  #command= lambda  : select(predicted_word)
  #ttk.Button(root, text=predicted_word , command=command, width=20).grid(row=8,column=5)
  

  print(predicted_word)
  return predicted_word 
  
     


titleLabel = Label(root, text='EYE TRACKER', font=('arial', 20, 'bold'), bg='whitesmoke', fg='gray30')
titleLabel.grid(row=0, columnspan=15)

textarea = Text(root, font=('arial', 15, 'bold'), height=5, width=100, wrap='word',bd=8,relief=SUNKEN)
textarea.grid(row=1, columnspan=15)
textarea.focus_set()

buttons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
           'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', '7', '8', '9',
           'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', 'Enter', '4', '5', '6',
           'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '↑ Shift', '1', '2', '3',
           'Space']

leftShiftButtons = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Backs', 'Del',
                    'Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ']', '7', '8', '9',
                    'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', 'Enter', '4', '5', '6',
                    'Shift ↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '<', '>', '?', '↑ Shift', '1', '2', '3',
                    'Space'

                    ]

capsButtons = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backs', 'Del',
               'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', '7', '8', '9',
               'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 'Enter', '4', '5', '6',
               'Shift ↑', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', '↑ Shift', '1', '2', '3',
               'Space']

varRow = 2
varColumn = 0

for button in buttons:

    command = lambda x=button: select(x)
    if button != 'Space':
        ttk.Button(root, text=button, command=command, width=10 ).grid(row=varRow, column=varColumn)

    if button == 'Space':
        ttk.Button(root, text=button, command=command, width=30, ).grid(row=6, column=0, columnspan=8)

    varColumn += 1
    if varColumn > 14:
        varColumn = 0
        varRow += 1



# def Predict_Next_Words(model, tokenizer, text):

#   sequence = tokenizer.texts_to_sequences([text])
#   sequence = np.array(sequence)
#   preds = np.argmax(model.predict(sequence))
#   predicted_word = ""
  
#   for key, value in tokenizer.word_index.items():
#       if value == preds:
#           predicted_word = key
#           break
  
#   print(predicted_word)
#   return predicted_word
   
#while(True):

#  text = "basel"
  
#  if text == "0":
#      print("Execution completed.....")
#      break
  
#  else:
#      try:
#          text = text.split(" ")
#          text = text[-3:]
#          print(text)
        
#          Predict_Next_Words(model, tokenizer, text)
          
#      except Exception as e:
#        print("Error occurred: ",e)
#        continue
ttk.Button(root, text=pre , command=command, width=20).grid(row=6,column=9,columnspan=4)
def dynamicButton(x):
    command = lambda : select(x)
    ttk.Button(root, text=x , command=command, width=20).grid(row=6,column=9,columnspan=4) 
root.mainloop()
