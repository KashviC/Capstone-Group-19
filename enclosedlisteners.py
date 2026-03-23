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
from madmom.audio.chroma import DeepChromaProcessor
from scipy.io import wavfile
import scipy.signal as sps

# Read 48kHz file

#feat_processor = madmom.features.chords.CNNChordFeatureProcessor()
#recog_processor = madmom.features.chords.CRFChordRecognitionProcessor()
feat_processor=DeepChromaProcessor()
recog_processor=madmom.features.chords.DeepChromaChordRecognitionProcessor(fps=20)
FORMAT = pyaudio.paInt16
CHANNELS = 2#set this to the channel number of recording device can be found using pyaudio commands
RATE = 44100 #set this to the sampling rate of recording device can be found using pyaudio commands
CHUNK = int(2046)
q  = deque()
#bytes_q  = []
chordsls= mp.Queue()
sm=[]
samplesize=4
def create_shared_block():


    shm = shared_memory.SharedMemory(create=True, size=64)
    # # Now create a NumPy array backed by shared memory
    np_array = np.ndarray([64,64], dtype=np.str_, buffer=shm.buf)
    return shm, np_array
def calculatechords(save,chordsls):
    start_time= datetime.now()
    #    feats = feat_processor(((np.frombuffer(b''.join(save), dtype=np.int16)[::2] >> 8).astype(np.int8) + 128))

    feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16))
    chords = recog_processor(feats)
    print( datetime.now() - start_time)
    #print("done")
    #print(chords)
    print(chords)
    
    return()
def enclosedthread(chordsls, span): 
    #rate=44.1*10e3
    bytes_q  = []
    print("start")
    try:
        audio = pyaudio.PyAudio()
    except:
        print("audio failure")
        
    ############################################
    def callback(in_data, frame_count, time_info,status):
        
        bytes_q.append(in_data)
        if len([item for sublist in bytes_q for item in sublist])>(RATE*span*CHANNELS*samplesize):
            #print("chunksize:"+str(len(bytes_q[0])))
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

    print("here")
    time.sleep(span)
    while True:
        save=bytes_q
        start_time= datetime.now()
        feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::2])
        chords = recog_processor(feats)
        chords=[chords,datetime.now()]
        #print( datetime.now() - end1)
        #print( chords)
        sys.stdout.flush()
        #sm=chords
        #print(str(sm)+"sm")
        chordsls.put(chords)
#chordls=[]
def threadsim(chordsls):
    rate, data = wavfile.read("riptide.wav")
    # Calculate new number of samples
    new_rate = 44100
    new_samples = round(len(data) * new_rate / rate)
    # Resample
    new_data = (sps.resample(data, new_samples)).astype(np.int16).copy()
    datalen=len(new_data)
    new_data=np.concatenate((new_data, np.zeros([400000,2]))).astype(np.int16)
    cs=2048
    span=3
    sampspan=span*44.1*1000
    bytes_q  = []
    for i in range(int(datalen/2048)-2):
        #booly=1*(((i*cs)-sampspan)>0)
        #bytes_q=new_data[int(((i*cs)-sampspan)*booly):(i+3)*cs]
        bytes_q=new_data[int(i*cs):int(sampspan+i*cs)]
        time.sleep(cs/44100)
        save=bytes_q
        start_time= datetime.now()
        feats = feat_processor(np.frombuffer(b''.join(save), dtype=np.int16)[::])
        chords = recog_processor(feats)
        chords=[chords,datetime.now()]
        #print( datetime.now() - end1)
        #print( chords)
        sys.stdout.flush()
        #sm=chords
        #print(str(sm)+"sm")
        chordsls.put(chords)
#chordls=[]
#threadsim(chordls)
#enclosedthread(chordls,3)
