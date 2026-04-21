from enclosedlisteners import *
import send_data
import multiprocessing as mp
from multiprocessing import shared_memory, Process, Lock
import intempomode as temp
import asyncio

#import multiprocessing as mp
#from multiprocessing import Process
chordsls= mp.Queue()
rate, data = wavfile.read(("C:/Users/kashv/Capstone_Group19/Capstone-Group-19/audios/SZA.wav"))
new_rate = 44100
new_samples = round(len(data) * new_rate / rate)
# Resample
new_data = (sps.resample(data, new_samples)).astype(np.int16).copy()
feats = feat_processor(np.frombuffer(new_data, dtype=np.int16))
actual = recog_processor(feats)
threads=[]
span=3     
actual=["C:maj","F:min","G:maj","A:min"]
correct = True
breakfree = False
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
loop = None


#---------------------------
#   WEBSOCKET SHI
#-----------------------------
app = FastAPI()
connnections = []

app = FastAPI()
connected = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Unity is trying to connect...")
    await websocket.accept()
    connected.append(websocket)
    print("ACCEPTED!")
    try:
        while True:
            await websocket.send_text("i love lesbians")
            data = await websocket.receive_text()
            print(f"Received from Unity: {data}")
    except WebSocketDisconnect:
            print("Unity disconnected")

async def sendUnity(chord): 
    for client in connected:
        try: 
            await client.send(chord)
        except:
            pass

#send_data.closePort()

class record:
    span=3
    chords=['n']
    actualchords =[]
    chordSend = ''

    lt=datetime.now().timestamp()-span
    fixed=lt
    times=[0]
    timesstart=[0]

    def tx(self,send):
        print("new chord sent: "+str(send))
        result = self.check(send)
        #test all chords on LED display
        loop = asyncio.get_event_loop()
        loop.create_task(sendUnity(result[0]))

        #correct = True
       # if result[1]: #move onto next chord
        #    print("move to next")
           # send_data.sendChord(result[0]) ------------TEMPORARILY COMMENTING OUT TO TEST INTEMPO MODE -----------
         #   correct = True
        #else: 
            #print("try again")
            #send_data.sendChord(result[0])
       #     correct = False
       # if len(rec.actualchords) == 0: 
        #    print("DONE YOURE DONE UR FREE YAYYY")
         #   breakfree = True
            #send_data.closePort()------------TEMPORARILY COMMENTING OUT TO TEST INTEMPO MODE -----------

    def check(self,chordin):
        #chordin= "".join(send_data.cleanInput(chordin))
        #chordin= "".join(send_data.cleanInput(chordin))
        actualsingle = self.actualchords[0]
        if actualsingle == chordin: #correct
            print("correct chord. moving on")
            self.actualchords.pop(0)
            self.chordSend = self.actualchords[0]
            return self.chordSend, True
        else: 
            # print("incorrect chord")
            return actualsingle, False

    def manage(self,chordsin):
        #print("ao")
        ct=chordsin[1].timestamp()-self.fixed
        chordsin=chordsin[0]
        #print(ct)
        for i in chordsin:
            #print(i[2])
            #print(self.chords[len(self.chords)-1])
            index=0
            while((ct-(self.span-i[0]))<self.times[len(self.chords)-1-index]):
                index+=1
            if ((i[2]==self.chords[len(self.chords)-1] and index==1)):
                if index==1:
                    self.times[len(self.chords)-1]=ct-(self.span-i[1])
                #print(i[2])
            elif(index==0):
                #print(i)
                self.tx(i[2])
                self.chords.append(i[2])
                self.times.append(ct-(self.span-i[1]))
                self.timesstart.append(ct-(self.span-i[0]))
        self.lt=ct


def listener(): 
    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls, 3)))
        threads[i].start()
        time.sleep(.1)
      #  send_data.closePort()
      #  send_data.initialize()
      #  send_data.sendChord(actual[0]) ------------TEMPORARILY COMMENTING OUT TO TEST INTEMPO MODE -----------
    rec = record() 
    while True:
        if breakfree == True: break
        #time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    # start_time= datetime.now()
                    # print(start_time)
                    newchord=(chordsls.get())
                    #print("Chord detected:")
                    print(newchord[0])
                    print("time")
                    # print(newchord[1].timestamp())
                    #temp.tempoMain(newchord) #TEMPO MODE
                    rec.manage(newchord) 
        except:
            print("empty")
            audio.terminate()

import threading
@app.on_event("startup")
async def startlistening():
    loop = asyncio.get_running_loop()
    threading.Thread(target=listener, daemon=True).start()

    
