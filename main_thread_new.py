from enclosedlisteners import * 
#import multiprocessing as mp
#from multiprocessing import Process
rate,refaudio=wavfile.read("riptide.wav")
feats = feat_processor(np.frombuffer(refaudio, dtype=np.int16))
actual = recog_processor(feats)
threads=[]     
class record:
    span=6.8
    chords=['n']
    
    lt=datetime.now().timestamp()-span
    fixed=lt
    times=[0]
    timesstart=[0]
    def tx(self,send):
        print("new chord sent: "+str(send))
    def manage(self,chordsin):
        #print("ao")
        ct=datetime.now().timestamp()-self.fixed
        #print("ng")
        for i in chordsin:
            #print(i[2])
            #print(self.chords[len(self.chords)-1])
            index=0
            while((ct-(self.span-i[0]))<self.times[len(self.chords)-1-index]):
                index+=1
            if ((i[2]==self.chords[len(self.chords)-1] and index!=0) or index>1):
                self.times[len(chordsin)-index]=ct
                #print(i[2])
            else:
                #print(i)
                self.tx(i[2])
                self.chords.append(i[2])
                self.times.append(ct-(self.span-i[1]))
                self.timesstart.append(ct-(self.span-i[0]))
        self.lt=ct
if __name__ == '__main__':
    rec=record()
    #rec.manage([(0., 3.4, 'N')])
    #rec.manage([(0,2,'N'),(2,3.4,'A')])

    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls,)))
        threads[i].start()
        time.sleep(.1)
    while True:
        #time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    start_time= datetime.now()
                    print(start_time)
                    newchord=(chordsls.get())
                    print(newchord)
                    rec.manage(newchord)
                    #print(sm)
                    #print(np_array)
    
        except:
            print("empty")
    audio.terminate()
