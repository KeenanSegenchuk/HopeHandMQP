# Modified from https://github.com/AssemblyAI-Examples/realtime-voice-command-recognition
import numpy as np
import sys
import wave
import time
import threading

# Tensorflow - expects model
from tensorflow.keras import models
import tensorflow as tf

from recording_helper import record_audio, terminate
from recording_helper2 import record_audio2, terminate
from tf_helper import preprocess_audiobuffer

import matlab.engine
eng = matlab.engine.start_matlab()

# Modify this in the correct order (follows folders)
commands = ['Notopen', 'open']

loaded_model = models.load_model("updated_open4.keras")

#variable state - open or close, then act a certain way, look at state machines
#make two different models, use one model for open and one for close. see if this is more accurate
#make a state variable
#read "from the hand" to see if open or closed at first
#then keep track of state and use that
#assume at first that hand is always open to start
#train with our data open and close

count = 0
log = open("log.txt", "w")

# Reads command and passes to main func.
def predict_mic():
    global count
    audio = record_audio()
    uncut = np.copy(audio)	

    #use detectspeech to find word indices
    st = time.time()
    wordidx = eng.cc2(audio,16000)
    et = time.time()
    print(f"Command Detection took {et - st} seconds.")
    wordidx = wordidx[0]
    #print(wordidx)
    #calculate buffer needed to make clip 1 second long
    buffer = (int)(16000 - wordidx[1])/2
    # cut audio to 1-second centered around the command
    audio = audio[(int)(wordidx[0] - buffer):(int)(wordidx[0] + wordidx[1] + buffer)]
    # We can put Keenan's preprocessing here ^

    st = time.time()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    et = time.time()
    print(f"took {et-st} seconds to predict command")

    #log confidence values
    log.write(f"{count},{prediction[0][0]},{prediction[0][1]}, 0\n")

    #print(count)
    #print(f"Start: {wordidx[0] - buffer}")
    print(prediction)

    #softmax
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]
    confidence = prediction[0][label_pred[0]]
    #print("Predicted label:", command)
    if confidence > -10:
        with wave.open(f"saved_audio/audio_{count}.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(uncut.tobytes())
        with wave.open(f"saved_audio/audio_clip_{count}.wav", "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(audio.tobytes())
	
    count = count + 1
    return command, confidence

def run():
    st = time.time()
    #print(st)
    command, confidence = predict_mic()
    #print(confidence)
    if confidence > .5:
        print("Predicted label:", command)
    sys.stdout.flush()
    et = time.time()
    #print(f"pid: {threading.get_ident()}")
    #print(f"elapsedtime: {et-st}")
    while et - st < 3:
        et = time.time()
    run()

if __name__ == "__main__":
    t1 = threading.Thread(name="1", target=run, daemon=True)
    t2 = threading.Thread(name="2", target=run, daemon=True)
    t3 = threading.Thread(name="3", target=run, daemon=True)
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()
    while True:
        time.sleep(1)
        

    
        
