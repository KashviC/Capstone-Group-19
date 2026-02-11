# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 19:06:00 2026

@author: sbjoh
"""
import wave
import os
import time
import sys
#import Live
from collections import deque
from queue import Queue
import pyaudio
import numpy as np
import random
#from tkinter import * 
import madmom
#from numba import jit, cuda
import threading
import multiprocessing as mp
from multiprocessing import shared_memory, Process, Lock
from scipy.io import wavfile
from datetime import datetime
feat_processor = madmom.features.chords.CNNChordFeatureProcessor()
recog_processor = madmom.features.chords.CRFChordRecognitionProcessor()
FORMAT = pyaudio.paInt16
CHANNELS = 2#set this to the channel number of recording device can be found using pyaudio commands
RATE = 44100 #set this to the sampling rate of recording device can be found using pyaudio commands
CHUNK = int(2048)
q  = deque()
#bytes_q  = []
chordsls= mp.Queue()
def create_shared_block():


    shm = shared_memory.SharedMemory(create=True, size=64)
    # # Now create a NumPy array backed by shared memory
    np_array = np.ndarray([64,64], dtype=np.str_, buffer=shm.buf)
    return shm, np_array
def calculatechords(save,chordsls):
    start_time= datetime.now()
    feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::2])
    chords = recog_processor(feats)
    print( datetime.now() - start_time)
    #print("done")
    #print(chords)
    print(chords)
    
    return()
def enclosedthread(chordsls,shr_name):    
    #lock = Lock()
    #existing_shm = shared_memory.SharedMemory(name=shr_name)
    #np_array = np.ndarray((64, 64,), dtype=np.str_, buffer=existing_shm.buf)
    #lock.acquire()
    #np_array[0] = "s"
    #lock.release()
    #existing_shm.close()

    bytes_q  = []
    print("start")
    try:
        audio = pyaudio.PyAudio()
    except:
        print("audio failure")
        
    ############################################
    def callback(in_data, frame_count, time_info,status):
        bytes_q.append(in_data)
        
        if len([item for sublist in bytes_q for item in sublist])>150000:
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
    time.sleep(2)
    print("here")
    while True:
        save=bytes_q
        #print(len(save))
        #sys.stdout.flush()
        #start_time= datetime.now()
        feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::])
        #end1=datetime.now()
        #print(  start_time)
        chords = recog_processor(feats)
        #print( datetime.now() - end1)
        #print( chords)
        #sys.stdout.flush()

        chordsls.put(chords)

