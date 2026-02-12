from enclosedlisteners import * 
#import multiprocessing as mp
#from multiprocessing import Process
rate,refaudio=wavfile.read("riptide.wav")
feats = feat_processor(np.frombuffer(refaudio, dtype=np.int16))
actual = recog_processor(feats)
threads=[]     
class record:
    chords=['n']
    
    lt=datetime.now().timestamp()
    times=[lt]
    def tx(self,send):
        print("new chord sent: "+str(send))
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
    rec=record()
    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls,)))
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
                    #print(sm)
                    #print(np_array)
    
        except:
            print("empty")
    audio.terminate()