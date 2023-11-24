import cv2
import numpy as np
import dlib
import threading 
import tensorflow as tf
import pyttsx3
import pyautogui
import time 
import threading
import pyautogui
current_frame = None
# EyeGaze class to track and interpert eye movement
class EyeGaze:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.interpreter = tf.lite.Interpreter(model_path='C:/finalproject/model20.tflite')
        self.interpreter.allocate_tensors()
        self.input_d = self.interpreter.get_input_details()
        self.out_d = self.interpreter.get_output_details()
        self.input_shape = self.input_d[0]['shape'] 
        self.inputs, self.outputs = [], []
    # inorder to perform the appropriate action we need to know in which frame we are
    def set_frame (self, current_frame):
        self.current_frame = current_frame       
    # what is the minimum duration between two clicks
    def min_duration(self,t1, t2):
        if (t2 - t1)>= 0.5:
            return True
        else :
            return False

    def get_frame (self):
        return self.current_frame
    #using the trained model to classify the eye gaze
    def iris_pos(self, img):
        
        img_ar = np.asarray( img, dtype='float32')
        img_ar = np.expand_dims(img_ar, axis=0)
        self.interpreter.set_tensor(self.input_d[0]['index'], img_ar)
        self.interpreter.invoke()
        tflite_result = self.interpreter.get_tensor(self.out_d[0]['index'])
        output_details = self.interpreter.get_output_details()
        output = np.squeeze(self.interpreter.get_tensor(self.out_d[0]['index']))
        result = []
        _, topP= tf.math.top_k(tflite_result, k = 4 )
        d = {0:'Center', 1:'Down', 2:'right', 3:'Left', 4 :'up'}
        topP = np.array(topP)[0]
        return d[topP[0]]
    # will be used as a background thread to detect the presince of a person 
    def gaze(self):
        self.t = time.time()
        b = True
        while True:
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray)
            for face in faces:
                landmarks = self.predictor(gray, face)
                cimg = frame[ landmarks.part(22).y : (landmarks.part(28).y)+8, (landmarks.part(27).x) : (landmarks.part(26).x)]            
                img1 = cv2.resize(cimg,(150,150))
                gesture1 = self.iris_pos(img1)
                grey1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                cimg2 = frame[ landmarks.part(20).y : (landmarks.part(28).y)+8, (landmarks.part(17).x) : (landmarks.part(21).x)]            
                img2 = cv2.resize(cimg2,(150,150))
                gesture2 = self.iris_pos(img2)
                grey2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

                if (gesture1 == 'Down') and (gesture2 == 'Down'):
                    if self.min_duration(self.t, time.time()):
                        # pyautogui.moveRel(0,90, duration = 0.5)
                        if (self.current_frame.curser == 2):
                            self.current_frame.btn4.invoke()
                        if (self.current_frame.curser == 3):
                            self.current_frame.move_currsor(0,90)

                        self.t = time.time()

                elif (gesture1 == 'right') and  (gesture2 == 'right'):
                    if self.min_duration(self.t, time.time()):
                        # pyautogui.moveRel(170,0, duration = 0.2)
                        if (self.current_frame.curser == 2 or self.current_frame.curser == 1):
                            self.current_frame.btn3.invoke()
                        else :
                            self.current_frame.move_currsor(170,0)
                        self.t = time.time()
                        

                elif (gesture1 == 'up') and (gesture2 == 'up'):
                    if self.min_duration(self.t, time.time()):
                        if (self.current_frame.curser == 2):
                            self.current_frame.btn1.invoke()
                        if (self.current_frame.curser == 3):
                            self.current_frame.move_currsor(0,-90)
                        # pyautogui.moveRel(0,-90, duration = 0.2)
                        self.t = time.time()
                        
                elif (gesture1 == 'Left') and (gesture2 == 'Left'):
                    if self.min_duration(self.t, time.time()):
                        self.t = time.time()
                        if (self.current_frame.curser == 2 or self.current_frame.curser == 1):
                            self.current_frame.btn2.invoke()
                        else :
                            self.current_frame.move_currsor(-170,0)
                        # pyautogui.moveRel(-170,0, duration = 0.2)
                elif (gesture1 !='Down') and (gesture2 == 'Down'):
                    if self.min_duration(self.t, time.time()):
                        self.t = time.time()
                        if (self.current_frame.curser == 3):
                            pyautogui.click(pyautogui.position())


                else :
                    if (self.t, time.time()):
                        if self.current_frame.curser == 2:
                            self.current_frame.centerBtn.invoke()
                cv2.imshow('image',grey1)
                cv2.imshow('image2',grey2)
            key = cv2.waitKey(1)
            if key == 27:
                b = False
        self.cap.release()
        cv2.destroyAllWindows()
    # for closing the background thread (opencv) once the main thread has been terminated (GUI)
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
