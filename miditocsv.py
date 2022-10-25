
from music21 import midi, note
import csv

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
            #print(y)
            if y.type == midi.ChannelVoiceMessages.NOTE_ON:
                
                # Get midi information
                start = x * seconds_per_tick

                for l, k in events_list:
                    if k.type == midi.ChannelVoiceMessages.NOTE_OFF and k.pitch == y.pitch and l > x:
                        end = l * seconds_per_tick
                        # track - start - end - event - channel - note - velocity
                        note_events.append([y.track.index , start, end, 'Note_on', y.channel, y.pitch, y.velocity, note.Note(y.pitch).nameWithOctave]) 
                        break


    # Load to CSV  File
    with open('csv\sample_perfect_in_seconds.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(note_events)
    return note_events    


if __name__ == '__main__':
    #score = converter.parse('sample_errors.mid')
    #midi_out = score.write('midi', fp='sample_errors1.mid')
    events = MidiInfo('midi\sample_perfect1.mid')
    
    #PatternMatch(events)