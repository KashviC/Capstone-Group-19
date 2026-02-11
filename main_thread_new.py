from enclosedlisteners import * 
#import multiprocessing as mp
#from multiprocessing import Process
rate,refaudio=wavfile.read("riptide.wav")
feats = feat_processor(np.frombuffer(refaudio, dtype=np.int16))
actual = recog_processor(feats)
threads=[]       
if __name__ == '__main__':
    shr, np_array = create_shared_block()
    for i in range(1):
        #enclosedthread1()
        threads.append(Process(target=enclosedthread, args=(chordsls,shr.name)))
        threads[i].start()
        time.sleep(.1)
    while True:
        time.sleep(.01)
        try:
            if chordsls.qsize()>0:
                for i in range(chordsls.qsize()):
                    start_time= datetime.now()
                    print(start_time)
                    print(chordsls.get())
                    
                    #print(np_array)
    
        except:
            print("empty")
    audio.terminate()