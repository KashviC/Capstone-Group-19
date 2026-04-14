from music21 import converter, note, chord, corpus

def midianalyze():
    # Parse a MIDI file
    score = converter.parse('C:/Users/kashv/Capstone_Group19/Capstone-Group-19/audios/Triads.mid')
    chordified_score = score.chordify()
    chordified_score.show('text')
    for thisChord in chordified_score.recurse().getElementsByClass(chord.Chord):
        print(f"Chord: {thisChord.pitchedCommonName}, Measure: {thisChord.measureNumber}, ")
     #   with open("score.txt",'a') as f:
      #      f.append(thisChord.)
        
     #   return chordified_score
    
#def simplify(chord): 
  #  if chord.

def miditimeanalyze():
    score = converter.parse('C:/Users/kashv/Capstone_Group19/Capstone-Group-19/audios/Triads.mid')
    chordified_score = score.chordify()
    print("in miditimeanalyze")

    flattenotes = chordified_score.flatten().notes.stream() # flatten n clean to isolate only chord/note data
    for item in flattenotes.secondsMap:
        print("in flat map secs ")
        itemel = item["element"]
        if isinstance(itemel, chord.Chord): #if the elemtn in item is a chord obj not just a plain note unless we want a plain note? 
            start = item["offsetSeconds"]
            end = item["endTimeSeconds"]
            duration = item["durationSeconds"]

            print(f"Chord: {itemel.pitchedCommonName}, Start: {start}, End: {end}, Duration: {duration}")
            with open("score.txt", 'a') as f:
                f.write(f"Chord: {itemel.pitchedCommonName}, Start: {start}, End: {end}, Duration: {duration}\n")



miditimeanalyze()