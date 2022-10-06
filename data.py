import pandas as pd
import csv

def Notes(pattern, text):
    '''
        pattern < text
    - Get the notes with note_on
    Cases: 
        IF
        Correct Hit
        Partial Key Hit (Early, Late)
        Extra Hit
            - Set an interval
            - Check whether there is a note that is greater than start and less than
              the end of the current note
            - If there are notes less than the current note end time
                check if the note is the next note of the current note in MIDI file
        ELSE
        Missed Hit
            - Timing 
    '''
    # PROBLEM : BASE CASE

    size = len(pattern['event'])

    correct, partial, extra, missed = 0, 0, 0, 0
    # The p
    # notes = [i for i in range(0,len(pattern['event'])) if pattern['event'][i] == 'NOTE_ON']

    # If p - time note equals to t time and note
        # correct hit
    # Else if p time not equal t time
        # test 
    for i in range(0, size):
        if pattern['event'][i] == 'Note_on':
            if pattern['start'][i] == text['start'][i]: # 0 0
                correct += 1

            elif pattern['start'][i] < text['start'][i]: # early
                partial += 1
            elif pattern['start'][i] > text['start'][i]: # late
                partial += 1

            else:
                missed += 1

            j = i
            for j in range (i, size):
                if pattern['start'][j] < pattern['end'][i]: # end - 1536
                    if pattern['start'][j] == text['start'][j]: # 0 1536
                        pass
                    elif pattern['start'][j] != text['start'][j]:
                        extra += 1



    print (correct, partial, extra, missed)



        









    




def ModifyEvents(dictobj):
    acc = []
    size = len(dictobj['event'])

    print('EVENT' + '\t     NOTE NUMBER' + '\tSTART TIME' + '\tEND TIME')
    for i in range(0, size):
        if dictobj['event'][i] == 'NOTE_ON':
            event = dictobj['event'][i]
            time = dictobj['time'][i]
            note_num = dictobj['note'][i]
            acc.append(list((event,time,note_num)))
        elif dictobj['event'][i] == 'NOTE_OFF':
            for j in range(0, len(acc)):
                if dictobj['note'][i] == acc[j][2]:
                    print('Note On/Off\t' + str(acc[j][2]) + '\t\t' + str(acc[j][1]) + '\t\t' + str(dictobj['time'][i]))
                    acc.pop(j)
                    break

    return acc











if __name__ == '__main__':
    Pattern = pd.read_csv("csv\silentnight.csv",error_bad_lines=False) 

    #LOAD CSV FILE TO DICTIONARY
    pattern_object = Pattern.to_dict('list')

    Truth = pd.read_csv("csv\silentnight.csv",error_bad_lines=False) 

    #LOAD CSV FILE TO DICTIONARY
    truth_object = Truth.to_dict('list')

    Notes(pattern_object, truth_object)




    