'''
The purpose of this file is to take the chords identified from main_thread and send 2 bytes to the arduino. 
The first byte is the chord's 4 digit code that indicates which chord it is. The 2nd byte will be a delimiter (hex) 

That number will be used in the arduino chord to match with the arduino's internal look up table we designed.

This is meant ot be combined into sean's code

'''
from serial import Serial
import time
import re

#arduino = Serial(port='COM4', baudrate=115200, timeout=.1)  #LOL ASSUME
#Serial.begin(115200)

#The 2nd param in this dict indicates which strings should be left open
CHORDS = {
    'C#': 1,
    'Ab': 2,
    'Fm': 3,
    'Eb': 4,
    'G':  5,
    'C:maj':  6,
    'D:maj':  7,
    'E:maj':  8,
    'A:maj':  9,
    'A:min': 10,
    'E:min': 11,
    'D:min': 12,
	'F#:min': 13,
}
'''
def sendData(str): 
	arduino.write(bytes(str)) 
'''

def cleanInput(str): #isolate chords and clean it up
	chords = re.findall(r"""['"]([^'"]*)['"]""", str)#to isolate chord into tuples
	isolated_chords = []
	for c in chords: 
		if c != 'N': 
			isolated_chords.append(c)
	return isolated_chords
			

def checkChordguitarandfile(guitar, actual): #this is to check chord accuracy between guitar and file
	print('gucci flip flops')
	#if guitar != actual: #wrong chord
		#sendData()
		
	




# ---------------------------------- TESTING ----------------------------------------
'''
testsample = '[(0., 0.7, \'N\') (0.7, 1.6, \'E:min\')]'
testsample2 = '[(0., 1.5, \'A:maj\')]'
testsample3 = '[(0., 1.5, \'N\')]'
print(cleanInput(testsample))
print(cleanInput(testsample2))
print(cleanInput(testsample3))


'''