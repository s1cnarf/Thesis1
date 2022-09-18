from music21 import *
import csv

#initialize structure of csv
header = ['Measure', 'Beat', 'Chord Notes']



score = converter.parse('D:\Laptop\Documents\Python\sample.mid')
bChords = score.chordify()

data = []

for thisChord in bChords.recurse().getElementsByClass('Chord'):
        # file.write(str(thisChord.measureNumber) + ' ' + str(thisChord.beatStr) + ' '  + str(thisChord.pitchNames)) 
        strChord = ''
        for i in thisChord.pitchNames:
            strChord += i
        data.append([thisChord.measureNumber, thisChord.beatStr, strChord])

with open('Chords.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)

# score.show("text")
   

# import music21
# from music21 import *

# piece = converter.parse("D:\Laptop\Documents\Python\Blues-For-Piano-2.mid")
# all_parts = []
# for part in piece.parts:
#     part_tuples = []
#     for event in part:
#         for y in event.contextSites():
#             if y[0] is part:
#                 offset = y[1]
#             if getattr(event, 'isNote', None) and event.isNote:
#                 part_tuples.append((event.nameWithOctave, event.quarterLength, offset))
#             if getattr(event, 'isRest', None) and event.isRest:
#                 part_tuples.append(('Rest', event.quarterLength, offset))
#     all_parts.append(part_tuples)

# print(all_parts)