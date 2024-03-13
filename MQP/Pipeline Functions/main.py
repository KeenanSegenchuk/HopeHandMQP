# Modified from https://github.com/AssemblyAI-Examples/realtime-voice-command-recognition
import numpy as np
import sys
import os
import socket
# from configparser import ConfigParser
# config = ConfigParser()
# config.read('config.ini')
# print(config.sections())
# print(list(config['class']))
# print(config['class'] ['var1'])
import matlab.engine
eng = matlab.engine.start_matlab()

print("Connected to Engine")

# Tensorflow - expects model
from tensorflow.keras import models

#from recording_helpercopy import record_audio, terminate
#proof of concept - play the audio back at us
from recording_helper import record_audio
from recording_helper2 import record_audio2, terminate
from tf_helper import preprocess_audiobuffer

# Modify this in the correct order (follows folders)
commands = ['close', 'down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']
#commandsopen = ['close', 'notclose']
#commandsclose = ['open', 'notopen']

###tcp goes in setup, run check every once and a while

#0 is open
#1 is close
state = 'open'
host = '127.0.0.1'
port = 65432


#conn = <socket.socket fd=3812, family=2, type=1, proto=0, laddr=('127.0.0.1', 61581), raddr=('127.0.0.1', 51511)>

def socketconnectfunc():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("looking for connection")
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # if True:
                # data = conn.recv(1024)
                # have something recieving from matlab (constantly spamming port w data is not good, you want to send message to make sure its efficient)
                # if not data:
                #     break
                # conn.sendall(b'%d',state)
            if state == 'open':
                    conn.sendall(b'open ')
                    tf = eng.practicefunction2
                    print(tf)
            else:
                    conn.sendall(b'close')
                    tf = eng.practicefunction2
                    print(tf)
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     print("looking for connection")
    #     s.bind((host, port))
    #     s.listen()
    #     conn, addr = s.accept()
    #         # tf = eng.practicefunctionHelloWorldforupdatedcode()
    #     with conn:
    #         print(f"Connected by {addr}")
    #         if type != 1:
    #             if True:
    #             #     # data = conn.recv(1024)
    #             #     # have something recieving from matlab (constantly spamming port w data is not good, you want to send message to make sure its efficient)
    #             #     # if not data:
    #             #     #     break
    #                 conn.sendall(b'%d',state)
    #                 print(b'%d',state)



# def socketsendfunc(state):
#         with connection:
#             connection.sendall(state)
#             print(state)

            #             connection.sendall(b'%d',state)
            # print(b'%d',state)

# Reads command and passes to main func.
                    
iv = eng.loadiv()
afe = eng.loadafe()

def predict_mic():
    audio = record_audio()
    tf = eng.checkUserCommand(iv, afe, audio, 48000)
    if not tf[2]:
        print("User or Command Unrecognized")
        if not tf[1]:
            print("No Command Found")
        if not tf[0]:
            print("Speaker Unrecognized")
        return "nothing", 0
    else:
        # spec = preprocess_audiobuffer(audio)
        # # We can put Keenan's preprocessing here ^
        # prediction = loaded_model(spec)
        #     #softmax
        # print(prediction)
        # label_pred = np.argmax(prediction, axis=1)
        # command = commands[label_pred[0]]
        # confidence = prediction[0][label_pred[0]]
        #     #print("Predicted label:", command)
        # return command, confidence
        return "nothing", 1

def predict_mic2():
    audio2 = record_audio2()
    tf = eng.checkUserCommand(iv, audio2, 48000)
    if not tf[2]:
        print("User or Command Unrecognized")
        if not tf[1]:
            print("No Command Found")
        if not tf[0]:
            print("Speaker Unrecognized")
        return "nothing", 0
    else:
        spec2 = preprocess_audiobuffer(audio2)
        prediction2 = loaded_model(spec2)
        print("Second Prediction", prediction2)
        label_pred2 = np.argmax(prediction2, axis=1)
        command2 = commands[label_pred2[0]]
        confidence2 = prediction2[0][label_pred2[0]]
        return command2, confidence2


def readopen():
    while True:
        command, confidence = predict_mic()
        if confidence > .5:
            print("Predicted label1:", command)
            print("Looking for stop")
        sys.stdout.flush()
        if command == "stop":
            # socketconnectfunc()
            #if close is detected, send signal to close hand, change state
            #pause to let hand change
            #terminate()
            break

        command2, confidence2 = predict_mic2()
        if confidence2 > .5:
            print("Predicted label2:", command2)
            print("Looking for stop")
        sys.stdout.flush()
        if command2 == "stop":
            # socketconnectfunc()
            #if close is detected, send signal to close hand, change state
            #pause to let hand change
            #terminate()
            break


def readclose():
    while True:
        command, confidence = predict_mic()
        if confidence > .5:
            print("Predicted label1:", command)
            print("Looking for left")
        sys.stdout.flush()
        if command == "left":
            # socketconnectfunc()
            #in the open models, if open is detected, send signal to open hand, change state
            #pause to let hand change
            break

        command2, confidence2 = predict_mic2()
        if confidence2 > .5:
            print("Predicted label2:", command2)
            print("Looking for left")
        sys.stdout.flush()
        if command2 == "left":
            # socketconnectfunc()
            #in the open models, if open is detected, send signal to open hand, change state
            #pause to let hand change
            break


#to change state, send signal to close hand (4X Digital I/O (what we have to worry about) and 4X PWM (pulse with modulation, shouldnt have to touch))

if __name__ == "__main__":
    #state = eng.readfromHOPEHand
    #setting a value would be easier than reading
    #reading encoder values is important at checkpoints
    while True:
        while state == 'open':
            # Loads model
            loaded_model = models.load_model("saved_model2")
            readopen()
            print("CHANGING STATE TO CLOSED")
            state = 'close'

        while state == 'close':
            # Loads model
                loaded_model = models.load_model("saved_model2")
                readclose()
                print("CHANGING STATE TO OPEN")
                state = 'open'