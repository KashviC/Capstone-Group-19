'''
The purpose of this file is to take the chords identified from main_thread and send 2 bytes to the arduino. 
That number will be used in the arduino chord to match with the arduino's internal look up table we designed.

'''
from serial import Serial
import time
import re
import datetime
import serial.tools.list_ports

#The 2nd param in this dict indicates which strings should be left open
CHORDS = {
    'Ab:maj':1, 
    'F:min':2,
    'Eb:maj':3,
    'G:maj':4,
    'C:maj':5,
    'D:maj':6,
    'E:maj':7,
    'A:maj':8,
    'A:min':9,
    'E:min':10,
    'D:min':11
}
serialinst = serial.Serial()
portsList = []
COM = 3 #change if needed 

def initialize():
    comports = serial.tools.list_ports.comports()
    for port in comports: 
        portsList.append(str(port)) #getallports 

    avalport = None
    for i in range(len(comports)):
        if portsList[i].startswith("COM"+str(COM)): #if selected port is avaible
            avalport = "COM"+str(COM)
    if avalport is None: 
        print("No ports available. Exiting")
    else:
        serialinst.baudrate = 9600
        serialinst.port = avalport
        serialinst.open()

def closePort(): 
    serialinst.close()


def cleanInput(chordin): #isolate chords and clean it up
    isolated_chords = []
    if len(chordin) == 2 and isinstance(chordin[1], datetime.datetime): #check to see if this is the actual chords or input chord from guitar
        isolated_chords.append(chordin[0][0][2]) #input chord from 
    else:
        for chord in chordin: 
            if chord[2] != 'N':
                isolated_chords.append(chord[2])
    return isolated_chords
		
def sendChord(newchord): 
    #sends the next chord
    value = CHORDS.get(newchord)
    if value is not None:
        serialinst.write(bytes([value]))
