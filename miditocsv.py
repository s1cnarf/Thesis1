
from music21 import midi, note
import csv
import pandas as pd

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

    for e in events:
        for y in e.events:
            if y.type == midi.MetaEvents.SET_TEMPO: 
                data = y.data

    mspq = midi.getNumber(data, len(data))[0]
    bpm = round(60_000_000 / mspq, 1)
    tempo = round((60 * 1000000) / bpm)
    print(f'MSPQ {mspq}')
    print(F'true bpm {bpm}') 
    print(F'true tempo {tempo}')  

    ticks_per_quarter = mf.ticksPerQuarterNote
    µs_per_quarter = mspq
    µs_per_tick = µs_per_quarter / ticks_per_quarter
    seconds_per_tick = µs_per_tick / 1_000_000     
    
    note_events  = []
    header = ['track','start', 'end', 'event','channel','note','velocity','name']
    for i in events:
        events_list = midi.translate.getTimeForEvents(i)
        for x, y in events_list:
            # x - start , y - midi event
            
            if y.type == midi.ChannelVoiceMessages.NOTE_ON and y.velocity != 0:
                
                # Get midi information
                start = x #* seconds_per_tick

                for l, k in events_list:
                    if k.type == midi.ChannelVoiceMessages.NOTE_OFF:
                        if k.pitch == y.pitch and l > x:
                            end = l #* seconds_per_tick
                            # track - start - end - event - channel - note - velocity
                            note_events.append([y.track.index , start, end, 'Note_on', y.channel, y.pitch, y.velocity, note.Note(y.pitch).nameWithOctave]) 
                            break
                    elif k.type == midi.ChannelVoiceMessages.NOTE_ON and k.velocity == 0:
                        if k.pitch == y.pitch and l > x:
                            end = l #* seconds_per_tick
                            # track - start - end - event - channel - note - velocity
                            note_events.append([y.track.index , start, end, 'Note_on', y.channel, y.pitch, y.velocity, note.Note(y.pitch).nameWithOctave]) 
                            break


    #Load to CSV  File
    with open(r'csv\truth\t_frj.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(note_events)
    return note_events    


def modifycsv():
    df = pd.read_csv("csv\encoded.csv",error_bad_lines=False) 
    dictobj = df.to_dict('list')
    note_events  = []
    header = ['track','start', 'end', 'event','channel','note','velocity','name']
    acc = []
    index = []
    size = len(dictobj['Event'])

    print('EVENT' + '\t     NOTE NUMBER' + '\tSTART TIME' + '\tEND TIME'+ '\tDISTANCE')
    for i in range(0, size):
        if dictobj['Event'][i] == 'Note_on':
            event = dictobj['Event'][i]
            time = dictobj['Time'][i]
            note_num = dictobj['Note'][i]
            acc.append(list((event,time,note_num)))
            index.append(i)
        elif dictobj['Event'][i] == 'Note_off':
            for j in range(0, len(acc)):
                if dictobj['Note'][i] == acc[j][2]:
                    s = acc[j][1]
                    e = dictobj['Time'][i]
                    n = acc[j][2]
                    dist = e - s
                    # note - start - end 
                    #print('Note On/Off\t' + str(acc[j][2]) + '\t\t' + str(acc[j][1]) + '\t\t' + str(dictobj['Time'][i])+ '\t\t' + str(dist))
                    note_events.append([1, s, e, 'Note_on', 1, n, dictobj['Velocity'][i], note.Note(n).nameWithOctave])
                    acc.pop(j)
                    break
    
    with open(r'csv\u_frj.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(note_events)



if __name__ == '__main__':
    #score = converter.parse('sample_errors.mid')
    #midi_out = score.write('midi', fp='sample_errors1.mid')
    events = MidiInfo('midi\frj.mid')
    #modifycsv()
    #PatternMatch(events)