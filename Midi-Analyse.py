from music21 import converter, note, chord, corpus

# Parse a MIDI file
score = converter.parse('midifile.mid')
chordified_score = score.chordify()
chordified_score.show('text')
for thisChord in chordified_score.recurse().getElementsByClass(chord.Chord):
    print(f"Chord: {thisChord.pitchedCommonName}, Measure: {thisChord.measureNumber}")
