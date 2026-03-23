from enclosedlisteners import * 
#import multiprocessing as mp
#from multiprocessing import Process
rate, data = wavfile.read("riptide.wav")
# Calculate new number of samples
new_rate = 44100
new_samples = round(len(data) * new_rate / rate)
# Resample
new_data = (sps.resample(data, new_samples)).astype(np.int16).copy()
feats = feat_processor(np.frombuffer(new_data, dtype=np.int16))
actual = recog_processor(feats)
threads=[]
span=3     
class record:
    span=3
    chords=['n']
    
    lt=datetime.now().timestamp()-span
    fixed=lt
    times=[0]
    timesstart=[0]
    def tx(self,send):
        print("new chord sent: "+str(send))
    def manage(self,chordsin):
        #print("ao")
        ct=chordsin[1].timestamp()-self.fixed
        chordsin=chordsin[0]
        print(ct)
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
if __name__ == '__main__':
    rec=record()
    rec.span=span
    time.sleep(1)
    #rec.manage([(0., 6.8, 'N')])
    #rec.manage([(0,2,'N'),(2,6.8,'A')])
    #rec.manage([(0,2,'N'),(2,6.8,'B')])
    #rec.manage([(0,2,'C'),(2,6.8,'B')])
    #rec.manage([(0,2,'N'),(2,6.8,'D')])

    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls, 3)))
        threads[i].start()
        time.sleep(.1)
    while True:
        #time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    #start_time= datetime.now()
                    #print(start_time)
                    newchord=(chordsls.get())
                    print(newchord[0])
                    print("time")
                    print(newchord[1].timestamp())
                    rec.manage(newchord)
                    #print(sm)
                    #print(np_array)
    
        except:
            print("empty")
    audio.terminate()
