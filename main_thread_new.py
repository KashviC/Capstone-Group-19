from enclosedlisteners import * 
import send_data
#import multiprocessing as mp
#from multiprocessing import Process
rate,refaudio=wavfile.read("C:/Users/kashv/Capstone_Group19/Capstone-Group-19/riptide.wav") #THIS WILL HAVE TO BE CHANGED ON UR SYSTEM
feats = feat_processor(np.frombuffer(refaudio, dtype=np.int16))
actual = recog_processor(feats)
threads=[]     
correct = True

class record:
    chords=['n']
    actualchords =[]
    lt=datetime.now().timestamp()
    times=[lt]
    def tx(self,send):
        print("new chord sent: "+str(send))

    def check(self,chordin):
        chordin= "".join(send_data.cleanInput(chordin))
        actualsingle = rec.actualchords[0]
        if actualsingle == chordin: #correct
            print("correct chord. moving on")
            rec.actualchords.pop(0)
            return True
        else: 
            print("incorrect chord")
            return False

    def manage(self,chordsin):
        print("ao")
        ct=datetime.now().timestamp()
        print("ng")
        for i in chordsin:
            print(i[2])
            print(self.chords[len(self.chords)-1])
            if (i[2]==self.chords[len(self.chords)-1]):
                self.times[len(chordsin)-1]=self.times[len(chordsin)-1]+float(ct-self.lt)
                print(i[2])
            else:
                print(i)
                self.tx(i[2])
                self.chords.append(i[2])
                self.times.append(ct-self.lt)
            self.lt=ct

if __name__ == '__main__':
    from send_data import *
    rec=record()
    rec.actualchords=send_data.cleanInput(actual)
    for i in range(1):
        #enclosedthread1()
        threads.append(threading.Thread(target=enclosedthread, args=(chordsls,)))
        threads[i].start()
        time.sleep(.1)
    while True:
        time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    start_time= datetime.now()
                    print(start_time)
                    newchord=(chordsls.get())
                    rec.manage(newchord)
                    result = rec.check(newchord)
                    if result: #move onto next chord
                        print("move to next")
                        correct = True
                    else: 
                        print("try again")
                        correct = False
                    #---------------------------
                    
    
        except:
            print("empty")
    audio.terminate()