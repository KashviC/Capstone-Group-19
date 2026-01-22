# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 01:16:06 2025

@author: sbjoh
"""
from chord_extractor.extractors import Chordino
from pychord import Chord
import numpy as np
from mido import MidiFile


class instructions:
    timing=[]
    chords=[]
    def __init__ (self,timing,chords):
        self.timing=timing
        self.chords=chords
    
def geninstruct(midi,sf):
    # Setup Chordino with one of several parameters that can be passed
    chordino = Chordino(roll_on=1)  
    # Optional, only if we need to extract from a file that isn't accepted by librosa
    #conversion_file_path = chordino.preprocess(midi)
    chords_timestamps=[]
    chords_names=[]
    # Run extraction
    if(midi.find(".midi")):
        mid = MidiFile(midi)
        time=0

        for msg in mid:
            if msg.type == "note_on":
                time+=msg.time
                print(time,msg.note,msg.velocity)
                chords_timestamps.append(msg.note)
                chords_names.append(time)
        instruction=instructions(chords_timestamps,chords_names)
    else:
        chords = chordino.extract(midi)
        chords_names = [chord.chord for chord in chords]
        chords_timestamps = [chord.timestamp for chord in chords]
        instruction=instructions(chords_timestamps,chords_names)
    return instruction
