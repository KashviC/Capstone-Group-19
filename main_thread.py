import wave
import os
import time
import sys
#import Live
from collections import deque
from queue import Queue
import pyaudio
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import random
#from tkinter import * 
import madmom
#from numba import jit, cuda
import threading
import multiprocessing as mp
from multiprocessing import Process
FORMAT = pyaudio.paInt16
CHANNELS = 2#set this to the channel number of recording device can be found using pyaudio commands
RATE = 44100 #set this to the sampling rate of recording device can be found using pyaudio commands
CHUNK = int(2048)
q  = deque()
bytes_q  = []
try:
    audio = pyaudio.PyAudio()
except:
    print("audio failure")
    
############################################
def callback(in_data, frame_count, time_info,status):
    bytes_q.append(in_data)
    #data = np.frombuffer(in_data, dtype=np.int16)
    #data = data.tolist()
    #q.appendleft(data)
    
    if len([item for sublist in bytes_q for item in sublist])>250000:
        #print(len([item for sublist in bytes_q for item in sublist]))
        del bytes_q[0]
    return None, pyaudio.paContinue
stream = audio.open(
        format=pyaudio.paInt16,
			channels=2,
			rate=RATE,
			input=True,
            output=False,
            input_device_index=1,
            output_device_index=3,
			frames_per_buffer=CHUNK,
			stream_callback=callback)
feat_processor = madmom.features.chords.CNNChordFeatureProcessor()
recog_processor = madmom.features.chords.CRFChordRecognitionProcessor()
#@jit(target_backend='cuda')
chordsls= mp.Queue()
def calculatechords(save,chordsls):
    feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::2])
    chords = recog_processor(feats)
    #print("done")
    #print(chords)
    chordsls.put(chords)
    print(chords)
    return()

threads=[]        
if __name__ == '__main__':
    time.sleep(1)
    for i in range(1):
        save=bytes_q
        feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::2])
        chords = recog_processor(feats)
        threads.append(Process(target=calculatechords, args=(save,chordsls)))
        threads[i].start()
        time.sleep(.1)
    while stream.is_active():
        #print("===========================================")
        try:
            #save=bytes_q
            #print(process(save))
            #time.sleep(.01)
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    save=bytes_q
                    nthread=(Process(target=calculatechords, args=(save,chordsls)))
                    nthread.start()
                    #print("===========================================")
                    chordsls.get()
                    #time.sleep(.01)
    
        except:
            print("empty")
    audio.terminate()