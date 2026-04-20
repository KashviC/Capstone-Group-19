from enclosedlisteners import *
import send_data
import multiprocessing as mp
from multiprocessing import shared_memory, Process, Lock
#import multiprocessing as mp
#from multiprocessing import Process
chordsls= mp.Queue()
rate, data = wavfile.read(("riptide.wav"))
new_rate = 44100
new_samples = round(len(data) * new_rate / rate)
# Resample
new_data = (sps.resample(data, new_samples)).astype(np.int16).copy()
feats = feat_processor(np.frombuffer(new_data, dtype=np.int16))
#sig=madmom.audio.signal.Signal(np.frombuffer(new_data, dtype=np.int16))
#sig.sample_rate=44100

#feats=feat_processor.process(sig)
#feats=feats
actual = recog_processor(feats*(feats>.7)*1)
threads=[]
span=.2
#actual=["C:maj","E:min","G:maj","A:min","C:maj","G:maj","N"]
actual=["G:maj","D:maj","G:maj","G:maj","D:maj","G:maj","G:maj","D:maj","N"]
#actual=["G:maj","G:maj","G:maj","G:maj","G:maj","N"]
#actual=["A:maj","A:maj","A:maj","A:maj","A:maj","N"]
actual=list(np.repeat(['E:maj','A:maj','A:min','E:min','D:min',"N"],3))
actual=["C:maj","E:min","C:maj","E:min","C:maj","E:min","F:maj","A:min","G:maj","D:min","A:min","C:maj","F:maj","G:maj","N"]
#actual=list(np.repeat(['E:min',"N"],3))
correct = True
breakfree = False

#send_data.closePort()
class record:
    span=.2
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
        

        correct = True
        if result[1]: #move onto next chord
            print("move to next")
            send_data.sendChord(result[0])
            correct = True
        else: 
            #print("try again")
            #send_data.sendChord(result[0])
            correct = False
        if len(rec.actualchords) == 0: 
            print("DONE YOURE DONE UR FREE YAYYY")
            breakfree = True
            send_data.closePort()
    def check(self,chordin):
        #chordin= "".join(send_data.cleanInput(chordin))
        
        #chordin= "".join(send_data.cleanInput(chordin))
        actualsingle = rec.actualchords[0]
        if actualsingle == chordin: #correct
            print("correct chord. moving on")
            rec.actualchords.pop(0)
            self.chordSend = rec.actualchords[0]
            return self.chordSend, True
        else: 
           # print("incorrect chord")
            return actualsingle, False

    def manage(self,chordsin):
        #print("ao")
        ct=chordsin[1].timestamp()-self.fixed
        chordsin=chordsin[0]
        #print(ct)
        pos=0
        for i in chordsin:
            pos+=1
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
          #  if (pos==len(chordsin) and (i[2]!=self.chords[len(self.chords)-1])):
           #     self.tx(i[2])
            #    self.chords.append(i[2])
             #   self.times.append(ct-(self.span-i[1]))
              #  self.timesstart.append(ct-(self.span-i[0]))
        self.lt=ct
if __name__ == '__main__':
    from send_data import *
    rec=record()
    #send_data.initialize() #initialize the arduino connection 

    rec.actualchords=actual#send_data.cleanInput(actual)
    rec.span=span
    time.sleep(1)
    #rec.manage([(0., 6.8, 'N')])
    #rec.manage([(0,2,'N'),(2,6.8,'A')])
    #rec.manage([(0,2,'N'),(2,6.8,'B')])
    #rec.manage([(0,2,'C'),(2,6.8,'B')])
    #rec.manage([(0,2,'N'),(2,6.8,'D')])

    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls, span)))
        threads[i].start()
        time.sleep(.1)
        send_data.closePort()
        send_data.initialize()
        send_data.sendChord(actual[0])
        
    while True:
        if breakfree == True: break #SEE IF THIS ACTUALLY WORKS LOL I DIDNT TEST IT IM LAZY 
        #time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    # start_time= datetime.now()
                    #print(start_time)
                    newchord=(chordsls.get())
                    print("Chord detected:")
                    print(newchord[0])
                    print("time")
                    #print(newchord[1].timestamp())
                    if(newchord[0][0][2]=="G:maj"):
                        print()
                    if(newchord[0][0][2]=="E:min"):
                        print()
                    rec.manage(newchord)


    
        except:
            print("empty")
            audio.terminate()
