from music21 import converter, tempo, midi, stream, note, instrument, pitch
import music21
import numpy as np
import pandas as pd

import csv

# picking out melody track
'''
midi_data = converter.parse('D:\Laptop\Documents\Python\silentnight.mid') #data_fn is the path to the .mid file I use
for part in midi_data.parts:
    print(part.partName)
    for measure in part.recurse().getElementsByClass('Note'):
        # print (measure.pitch, midi.translate.offsetToMidiTicks(measure.offset))
        print (midi.translate.noteToMidiEvents(measure))    
'''



def MidiInfo(midi_out):
    mf = midi.MidiFile()
    mf.open(midi_out)
    mf.read() 
    mf.close()
    events = mf.tracks

    # for tracks in events:
        # for event in tracks.events: 
            # DELTA TIME CORRESPONDS TO NOTE ON AND OFF

            # getTimeForEvents(miditrack) abs start time
            # print (midi.translate.getTimeForEvents(tracks))
            # if event.isNoteOn():
            #     print(event, midi.translate.midiEventsToNote(event)
    events_list = midi.translate.getTimeForEvents(events[1])
    note_events  = []
    header = ['track','start', 'end', 'event','channel','note','velocity']
    for x, y in events_list:
        # x - start , y - midi event
        if y.type == midi.ChannelVoiceMessages.NOTE_ON:
            # Get midi information
            start = x

        elif y.type == midi.ChannelVoiceMessages.NOTE_OFF:
            # track - start - end - event - channel - note - velocity
            note_events.append([1 , start, x, 'Note_on', y.channel, y.pitch, y.velocity]) 

    return note_events
    


def getMelodyPattern(note_events):
    # GETTING READY FOR THE ALGO
    # ALGO 1 (RIGHT HAND)

    # SORT THE NOTES (higher pitch priority)
    sort_by_pitch = sorted(note_events, key = lambda x:x[5])
    sort_by_pitch.reverse()
    melody = sort_by_pitch[0]
    melodyNotes = [melody]

    # FIND THE OCCURENCES OF TIME OF THE NEXT NOTES TO BE PROCESSED

    for i in range (0, len(note_events)):
        # note onset > melody offset or note pitch > melody pitch
        if note_events[i][1] >= melody[2] or note_events[i][5] > melody[5]:
            melodyNotes.append(note_events[i])

    print(len(note_events))

    # Need matransfer yung midi note number into note then make it an even
    for x in melodyNotes:
        print (x)
    # RETURN list 




def PatternMatch(note_events):
    #  Approximate Pattern Matching Algorithm

    # ts = score[music21.meter.TimeSignature][0] TIME SIGNATURE
    # print (ts)

    # Get Notes in the pattern
    notes = ''
    for i in range(0, len(note_events)):
        notes += str(pitch.Pitch(note_events[i][5]))


    # Pattern - G4A4G4E4G4A4G4E4D5D5B4C5C5G4A4A4C5B4A4G4A4G4E4A4A4C5B4A4G4A4G4E4D5D5F5D5B4C5E5C5G4E4G4D4B3C4
    # Text - G4A4G4E4G4A4G4E4D5D5B4C5C5G4A4A4C5B4A4G4A4G4E4A4A4C5B4A4G4A4G4E4D5D5F5D5B4C5E5C5G4E4G4D4B3C4

    # Load the C matrix with rows equal to Text and columns equal to Pattern
    Pattern = 'G4A4G4E4'
    Text = 'G4A4G4E4'
    rows, cols = len(Pattern) + 1, len(Text) + 1
    C = [[0 for i in range(cols)] for j in range(rows)]
    print (C)
    for i in range (len(C)):
        C[i][0] = i
    for j in range (len(C[0])):
        C[0][j] = j        

    # Iterate through the list
        # If Pi == Tj then value in [i][j] equals to the diagonal
        # Else, Add 1 to the minimum number in vertical, horizontal, diagonal side of the cell

    for m in range(1, rows):
        for n in range(1, cols):
            if Pattern[m-1] == Text[n-1]:
                C[m][n] = C[m-1][n-1]
            else:
                C[m][n] = 1 + min(C[m-1][n], C[m-1][n-1], C[m][n-1])

    for x in C:
        print (x)

    # Last value in the matrix will be the basis for the error detection  
    print (C[m][n])





if __name__ == '__main__':
    score = converter.parse('D:\Laptop\Documents\Python\silentnight.mid')
    midi_out = score.write('midi', fp='D:\Laptop\Documents\Python\silentnight1.mid')
    events = MidiInfo(midi_out)
    PatternMatch(events)

                
                