'''
Author: KashviC

Input: GP file  OR npy array 
Output: CSV with fret and binary 6 digit code to represet which strings are being pressed
        ex: G chord is represented with [2, 010000]
                                        [3, 100001]

Row: Low E, A, D, G, B, High E
0 1 2 3 4 5

potentially to mark a new chord it snds a packet of [0,000000]

'''
import numpy as np
import re 
import csv

#The 2nd param in this dict indicates which strings should be left open
CHORDS = {
    'C#': ('011111', [(1,'000101'), (2,'000010'), (3,'001000'), (4,'010000')]),
    'Ab': ('001111', [(1,'001110'), (4,'000001')]),
    'Fm': ('111111', [(1,'111111'), (3,'011000')]),
    'Eb': ('001111', [(1,'001000'), (3,'000101'), (4,'000010')]),
    'G':  ('111111', [(2,'100000'), (3,'100001')]),
    'C':  ('011111', [(1,'000010'), (2,'001000'), (3,'010000')]),
    'D':  ('001111', [(2,'000101'), (3,'000010')]),
    'E':  ('111111', [(1,'000100'), (2,'011000')]),
    'A':  ('011111', [(2,'001110')]),
    'Am': ('011111', [(1,'000010'), (2,'001100')]),
    'Em': ('111111', [(2,'011000')]),
    'Dm': ('001111', [(1,'000001'), (2,'000100'), (3,'000010')]),
}

#unfinished
def writetoCSV(key):
        with open('LED_Matrix.csv', 'a', newline = '') as csvfile: 
            writer = csv.writer(csvfile)
            stringlist, fretlist = CHORDS[key]
            for fret, string in fretlist:
                writer.writerow([fret, string])
            writer.writerow([0, '000000']) #end the chord
            

def npyFile(input): 
    arr = np.load(input, allow_pickle=True)
    for chord in arr[0]: #ASSUMING 2D ARRAY CUZ THAT'S HOW THE SONG.NPY IS be careful....
        print(chord)
        for key in CHORDS.keys():
                if(chord == key): 
                      writetoCSV(key)
                     
    
    
