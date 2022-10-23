import mimetypes
from multiprocessing.synchronize import Condition
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

    notes_in_truth = []
    notes_in_user = []

    truth = []

    correct, partial, extra, missed = 0, 0, 0, 0
    # The p
    
    # notes = [i for i in range(0,len(pattern['event'])) if pattern['event'][i] == 'NOTE_ON']

    # If p - time note equals to t time and note
        # correct hit
    # Else if p time not equal t time
        # test 
    start, end = 0, 0
    for i in range (0, len(text['event'])):
        if text['end'][i] > end :
            end = text['end'][i]
            start = text['start'][i] 
            # line 14 1,17234,19000,Note_on,1,30,0
            print (f'start: {start} end: {end}')
            for p in range(0,size):
                if pattern['start'][p] >= start and pattern['end'][p] <= end:
                    notes_in_user.append([pattern['start'][p], # 0 , 1 , 2
                                        pattern['end'][p],
                                        pattern['note'][p]])

            for t in range(0,len(text['event'])):
                if text['start'][t] >= start and text['end'][t] <= end:
                    notes_in_truth.append([text['start'][t], # 0 , 1 , 2
                                        text['end'][t],
                                        text['note'][t]])

            
            print(f'truth: {notes_in_truth}')
            print(f'user: {notes_in_user}')
            
            truth = [0] * len(notes_in_truth)
            user = [0] * len(notes_in_user)

            #print(f'truth: {truth}')
            #print(f'user: {user}')
            for idx, i in enumerate(notes_in_truth): 
                
                if truth[idx] == 0:
                    for y in range(0, len(notes_in_user)):
                        #Time -> Notes:
                        # 0 = Start 1 = End 2 = Note
                        # Problem if tama yung time frame and napindot ulet like
                        # double pindot with true note
                        if user[y] == 0:
                            if notes_in_user[y][0] == i[0] and notes_in_user[y][1] == i[1]: #start end
                                if notes_in_user[y][2] == i[2]: #note number
                                    #print(f'Correct: {notes_in_user[y][2]} = {i[2]}, {y}')
                                    truth[idx] = 1
                                    user[y] = 1
                                    correct += 1
                                # elif notes_in_user[y][2] != i[2]:
                                #     #print(f'Extra: {notes_in_user[y][2]} = {i[2]}, {y}')
                                #     truth[idx] = 3
                                #     user[y] = 3
                                #     extra += 1
                            elif notes_in_user[y][0] >= i[0] and notes_in_user[y][1] <= i[1]:
                                if notes_in_user[y][2] == i[2]:
                                    #print(f'Partial: {notes_in_user[y][2]} = {i[2]}, {y}')
                                    partial += 1
                                    truth[idx] = 2
                                    user[y] = 2  
                                # elif notes_in_user[y][2] != i[2]:
                                #     #print(f'Extra: {notes_in_user[y][2]} = {i[2]}, {y}')
                                #     truth[idx] = 3 
                                #     user[y] = 3 
                                #     extra += 1
                                    
            #print (f'1 TABLE TRUTH: {truth}')
            #truth = Missed(truth, notes_in_truth, user, notes_in_user)
           

            notes_in_truth.clear()
            notes_in_user.clear()
            
            print (f'TABLE TRUTH: {truth}')
            print (f'TABLE USER: {user}')
            

            print (correct, partial, extra, missed)




def Dynamics(pattern,text):
    dynamics = 0
    for i in pattern['velocity']:
        if i == text['velocity']:
            dynamics += 1


def MelodyLR(pattern, text):
    condition = (pattern['track'] == 1) & (pattern['note'] > 0)
    pattern_Right = pattern[condition].note.tolist()

    condition = (text['track'] == 1) & (text['note'] > 0)
    text_Right = text[condition].note.tolist()

    #track the index of the the mismatch elements

    mismatch = [i for i, (a, b) in enumerate(zip(pattern_Right, text_Right)) if a != b]
    print(mismatch)


# dict parameter
def Rhythm(pattern_dict ,text_dict):
    '''
        Rhythm by Switches
        Switches is based on note on time

        Similarity between the note on time is processed
    '''
    Success, Failed = 0, 0
    
    pattern_dym = pattern_dict['start']
    text_dym = text_dict['start']
    index = 0
    for i in pattern_dym:
        if i == text_dym[index]:
            Success += 1
        else:
            Failed += 1
        index += 1

    print(f"Success : {Success} Failed : {Failed}")
    

def Articulation(pattern_dict, text_dict):
    Timed, Late, Early = 0,0,0

    pattern_articulation = pattern_dict['start']
    text_articulation = text_dict['start']

    index = 0
    for i in pattern_articulation:
        if i == text_articulation[index]:
            Timed += 1
        elif i < text_articulation[index]:
            Early += 1
        elif i > text_articulation[index]:
            Late += 1 
        index += 1

    print(f"Timed : {Timed} Late : {Late} Early : {Early}")

# DATA FRAME
def FingerPattern(pattern, text):
    rhits, rwrong = 0,0

    #Filter data for right hand pattern
    condition = (pattern['track'] == 1) & (pattern['note'] > 0)
    pattern_Right = pattern[condition]

    condition = (text['track'] == 1) & (text['note'] > 0)
    text_Right = text[condition]

    # Count match and mismatch value in right hand
    matched, un_matched = pattern_Right[pattern_Right['note']==text_Right['note']].shape[0], pattern_Right[pattern_Right['note']!=text_Right['note']].shape[0]
    print(f"Right Hand: Matched = {matched} Unmatched = {un_matched}")

    # Filter data for left hand pattern
    condition = (pattern['track'] == 2) & (pattern['note'] > 0)
    pattern_Left= pattern[condition]

    condition = (text['track'] == 2) & (text['note'] > 0)
    text_Left = text[condition]

    # Count match and mismatch in left hand 
    matched, un_matched = pattern_Left[pattern_Left['note']==text_Left['note']].shape[0], pattern_Left[pattern_Left['note']!=text_Left['note']].shape[0]
    print(f"Left Hand: Matched = {matched} Unmatched = {un_matched}")


   


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
    Pattern = pd.read_csv("csv\sample_perfect.csv",error_bad_lines=False) 

    #LOAD CSV FILE TO DICTIONARY
    pattern_dict = Pattern.to_dict('list')

    Truth = pd.read_csv("csv\sample.csv",error_bad_lines=False) 

    #LOAD CSV FILE TO DICTIONARY
    truth_dict = Truth.to_dict('list')

    #Notes(pattern_dict, truth_dict)

    # #DATA FRAME
    # MelodyLR(Pattern, Truth)

    # #Dictionary
    # Rhythm(pattern_dict, truth_dict)

    # Articulation(pattern_dict, truth_dict)



    