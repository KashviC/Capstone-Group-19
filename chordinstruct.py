# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 01:06:37 2025

@author: sbjoh
"""

from gen import *
chords=geninstruct("output.wav",1000)
arr = np.array([chords.chords,chords.timing],dtype=object)
np.save('song.npy', arr)