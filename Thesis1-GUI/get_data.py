from cgitb import text
import pandas as pd
import csv
import os
from music21 import midi, note
import sys

class Data:
    def __init__(self):
        self.Truth = pd.DataFrame()
        self.Pattern = pd.DataFrame()
        self.truth_data = {}
        self.pattern_data = {}
    def Notes(self):
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
        pattern = self.Pattern
        text = self.Truth
        size = len(pattern['event'])

        notes_in_truth = []
        notes_in_user = []
        
        correct, partial, extra, missed = 0, 0, 0, 0

        user_articulation = {'Timed': 0, 'Late': 0, 'Early': 0}

        # The p
        
        # notes = [i for i in range(0,len(pattern['event'])) if pattern['event'][i] == 'NOTE_ON']

        # If p - time note equals to t time and note
            # correct hit
        # Else if p time not equal t time
            # test 
        
        # Get the data in the start index
        start_elements = []
        keys = list(text['note'].to_list())
        start, end = 0, 0
        for i in range (0, len(text['event'])):
            if text['end'][i] > end:
                end = text['end'][i]
                start = text['start'][i] 
                # line 14 1,17234,19000,Note_on,1,30,0
                # print (f'start: {start} end: {end}')
                for t in range(0,len(text['event'])):
                    if text['start'][t] >= start and text['end'][t] <= end:
                        t_data = [text['start'][t], # 0 , 1 , 2
                                            text['end'][t],
                                            text['note'][t]]

                        if t_data != start_elements:
                            notes_in_truth.append(t_data)

                for p in range(0,size):
                    if pattern['start'][p] >= start and pattern['end'][p] <= end:
                        p_data = [pattern['start'][p], # 0 , 1 , 2
                                            pattern['end'][p],
                                            pattern['note'][p]]

                        if p_data != start_elements:
                            notes_in_user.append(p_data)

                # value of the start basis index
                start_elements = notes_in_truth[0]

                
                #print(f'truth: {notes_in_truth}')
                #print(f'user: {notes_in_user}')
                
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
                                        user_articulation['Timed'] += 1
                                    # elif notes_in_user[y][2] != i[2]:
                                    #     #print(f'Extra: {notes_in_user[y][2]} = {i[2]}, {y}')
                                    #     truth[idx] = 3
                                    #     user[y] = 3
                                    #     extra += 1
                                else:
                                    if notes_in_user[y][0] >= i[0] and notes_in_user[y][1] <= i[1]:
                                        if notes_in_user[y][2] == i[2]:
                                            #print(f'Partial: {notes_in_user[y][2]} = {i[2]}, {y}')
                                            truth[idx] = 2
                                            user[y] = 2
                                            user_articulation['Late'] += 1
                                    elif notes_in_user[y][0] <= i[0] and notes_in_user[y][1] >= i[1]:
                                        if notes_in_user[y][2] == i[2]:
                                            #print(f'Partial: {notes_in_user[y][2]} = {i[2]}, {y}')
                                            truth[idx] = 2
                                            user[y] = 2 
                                            user_articulation['Early'] += 1
                                    
                                        
                #print (f'1 TABLE TRUTH: {truth}')
                #truth = Missed(truth, notes_in_truth, user, notes_in_user)
            
                for i in range (len(user)):
                    if user[i] == 0: 
                        if notes_in_user[i][2] not in keys:
                            extra += 1

                # print('Truth Table: ', truth, ' User Table:', user)
                # print ('Notes in truth: ', notes_in_truth, ' Notes in user: ', notes_in_user, ' Extra: ', extra)
                # print ('\n')

                notes_in_truth.clear()
                notes_in_user.clear()
                
                #print (f'TABLE TRUTH: {truth}')
                #print (f'TABLE USER: {user}')

                correct += truth.count(1)
                partial += truth.count(2)
                missed += truth.count(0)
                

        return [correct, partial, extra, missed] + list(user_articulation.values())




    def Dynamics(self):
        '''
        Loudness and Softness of Velocity
        Get the Mean/Average of the velocities in the MIDI
        '''
        pattern, text = self.Pattern, self.Truth
        dynamics = [127,112,96,80,64,49,33,16]
        term = ['extremely loud', 'very loud', 'loud', 'moderately loud', 'moderately soft', 
                'soft', 'very soft', 'extremely soft']

        t_mean = sum(text['velocity']) / len(text['velocity'])
        p_mean = sum(pattern['velocity']) / len(pattern['velocity'])

        for i in range(len(dynamics)):
            if t_mean > dynamics[i]:
                print(term[i])
                break

        return [t_mean, p_mean]



    def MelodyLR(self):
        ''' 
        Linear Matching 
        If note p is not equal to note t then the melody is not right
        '''
        pattern, text = self.Pattern, self.Truth
        condition = (pattern['track'] == 1) & (pattern['note'] > 0)
        pattern_Right = pattern[condition].note.tolist()

        condition = (text['track'] == 1) & (text['note'] > 0)
        text_Right = text[condition].note.tolist()

        #track the index of the the mismatch elements
        print ('pattern: ', len(pattern_Right), ' text: ', len(text_Right))
        mismatch = [i for i, (a, b) in enumerate(zip(text_Right, pattern_Right)) if a != b]
        # mismatch = 0   
        match =  len(pattern_Right) - len(mismatch)
        percentage = (match/len(text_Right))*100
        return percentage


    # dict parameter
    def Rhythm(self):
        '''
            Rhythm by Switches
            Switches is based on note on time

            Similarity between the note on time is processed
        '''
        pattern_dict, text_dict = self.pattern_data, self.truth_data
        Success, Failed = 0, 0
        
        pattern_dym = pattern_dict['start']
        text_dym = text_dict['start']
        print (len(text_dym))
        print (len(pattern_dym))
        index = 0
        for i in text_dym:
            if index < len(pattern_dym):
                if i == pattern_dym[index]:
                    Success += 1
                else:
                    Failed += 1
            else:
                Failed += 1
            index += 1

        return [Success,Failed]
        
    '''
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
    '''
    # DATA FRAME
    def FingerPattern(self):
        pattern, truth = self.Pattern, self.Truth
        Truth_R = truth[truth['track'] == 1].name.to_list()
        Pattern_R = pattern[pattern['track'] == 1].name.to_list()

        Truth_L = truth[truth['track'] == 2].name.to_list()
        Pattern_L = pattern[pattern['track'] == 2].name.to_list()

        R_rows, R_cols = len(Pattern_R) + 1, len(Truth_R) + 1
        L_rows, L_cols = len(Pattern_L) + 1, len(Truth_L) + 1

        # Matrix for Approx Match
        R = [[0 for i in range(R_cols)] for j in range(R_rows)]
        for i in range (len(R)):
            R[i][0] = i
        for j in range (len(R[0])):
            R[0][j] = j      

        L = [[0 for i in range(L_cols)] for j in range(L_rows)]
        for i in range (len(L)):
            L[i][0] = i
        for j in range (len(L[0])):
            L[0][j] = j      

        # Iterate through the list
            # If Pi == Tj then value in [i][j] equals to the diagonal
            # Else, Add 1 to the minimum number in vertical, horizontal, diagonal side of the cell

        for m in range(1, R_rows):
            for n in range(1, R_cols):
                if Pattern_R[m-1] == Truth_R[n-1]:
                    R[m][n] = R[m-1][n-1]
                else:
                    R[m][n] = 1 + min(R[m-1][n], R[m-1][n-1], R[m][n-1])
        
        R_miss = R[m][n]

        for m in range(1, L_rows):
            for n in range(1, L_cols):
                if Pattern_L[m-1] == Truth_L[n-1]:
                    L[m][n] = L[m-1][n-1]
                else:
                    L[m][n] = 1 + min(L[m-1][n], L[m-1][n-1], L[m][n-1])

        L_miss = L[L_rows- 1][L_cols - 1]

        L_Correct = len(Truth_L) - L_miss
        R_Correct = len(Truth_R) - R_miss

        return [L_Correct, R_Correct, L_miss,R_miss]

    


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


    def Data_to_csv(self, pathFile):
        header = ['Element', 'Data']
        # #DATA FRAME
        melody = self.MelodyLR()
        dynamics = self.Dynamics()
        fingerpattern = self.FingerPattern()
        # #Dictionary
        rhythm = self.Rhythm()
        notes = self.Notes()

        data = {'Correct':notes[0], 
                'Partial':notes[1],
                'Extra':notes[2],
                'Missed':notes[3],
                'Success_Switch':rhythm[0],
                'Failed_Switch':rhythm[1],
                'Timed_Hit':notes[4],
                'Late_Hit':notes[5],
                'Early_Hit':notes[6],
                'Truth_Dynamics': dynamics[0],
                'User_Dynamics': dynamics[1],
                'LH_Correct' : fingerpattern[0],
                'RH_Correct' :fingerpattern[1],
                'LH_Fail' : fingerpattern[2],
                'RH_Fail' :fingerpattern[3],
                'Melody' : melody}
        try:
            path = '../csv/Result_' + pathFile
            print (path)
            with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in data.items():
                    writer.writerow(row)
        except FileNotFoundError:
            print('File doesnt exist from Data_to_csv')

    def read_csv(self, pathFileName):
        try:
            truth = r"..\csv\truth\t_" + pathFileName
            pattern = r"..\csv\user\u_" + pathFileName
            self.Truth = pd.read_csv(truth, on_bad_lines='skip')
            self.Pattern = pd.read_csv(pattern, on_bad_lines='skip')

            #Sort first the data frame
            self.Pattern.sort_values(['start', 'end', 'note'], ascending=[True, True, True], inplace=True)
            self.Truth.sort_values(['start', 'end', 'note'], ascending=[True, True, True], inplace=True)
            print (self.Truth)
            self.truth_data = self.Truth.to_dict('list')
            self.pattern_data = self.Pattern.to_dict('list')
        except FileNotFoundError:
            print("File doesn't exist from read_csv")


    
    def miditocsv(self, midiPath):
        try:
            path = "../midi/" + midiPath +'.mid'
            mf = midi.MidiFile()
            mf.open(path)
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
                        start = x * seconds_per_tick

                        for l, k in events_list:
                            if k.type == midi.ChannelVoiceMessages.NOTE_OFF:
                                if k.pitch == y.pitch and l > x:
                                    end = l * seconds_per_tick
                                    # track - start - end - event - channel - note - velocity
                                    note_events.append([y.track.index , round(start), round(end), 'Note_on', y.channel, y.pitch, y.velocity, note.Note(y.pitch).nameWithOctave])
                                    break
                            # note on with 0 velocity considered as note off
                            elif k.type == midi.ChannelVoiceMessages.NOTE_ON and k.velocity == 0:
                                if k.pitch == y.pitch and l > x:
                                    end = l * seconds_per_tick
                                    # track - start - end - event - channel - note - velocity
                                    note_events.append([y.track.index , round(start), round(end), 'Note_on', y.channel, y.pitch, y.velocity, note.Note(y.pitch).nameWithOctave])
                                    break


            #Load to CSV  File
            csvPath = "../csv/truth/new_t_" + midiPath + '.csv'
            with open(csvPath, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                # write multiple rows
                writer.writerows(note_events)

        except FileNotFoundError:
            print("File doesn't exist miditocsv")
    
    def modifycsv(self, csvPath):
        try:
            c = '../csv/' + csvPath
            print (c)
            df = pd.read_csv(c , on_bad_lines='skip') 
            dictobj = df.to_dict('list')
            note_events  = []
            header = ['track','start', 'end', 'event','channel','note','velocity','name']
            acc = []
            index = []
            size = len(dictobj['event'])

            print('EVENT' + '\t     NOTE NUMBER' + '\tSTART TIME' + '\tEND TIME'+ '\tDISTANCE')
            for i in range(0, size):
                if dictobj['event'][i] == 'Note_on':
                    event = dictobj['event'][i]
                    time = dictobj['time'][i]
                    note_num = dictobj['note'][i]
                    acc.append(list((event,time,note_num)))
                    index.append(i)
                elif dictobj['event'][i] == 'Note_off':
                    for j in range(0, len(acc)):
                        if dictobj['note'][i] == acc[j][2]:
                            s = acc[j][1]
                            e = dictobj['time'][i]
                            n = acc[j][2]
                            dist = e - s
                            # note - start - end 
                            #print('Note On/Off\t' + str(acc[j][2]) + '\t\t' + str(acc[j][1]) + '\t\t' + str(dictobj['Time'][i])+ '\t\t' + str(dist))
                            note_events.append([1, s, e, 'Note_on', 1, n, dictobj['velocity'][i], note.Note(n).nameWithOctave])
                            acc.pop(j)
                            break
            path = "../csv/user/u_" + csvPath
            print (note_events)
            with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                # write multiple rows
                writer.writerows(note_events)
        except FileNotFoundError:
            print ('File doesnt exist from modifycsv')

    # MODIFY TRUTH DATA BASED on pROLL TIME
    def modifyTruth(csvPath):
        try:
            print ('TRUTH MODIFIED DONE!!!!')
            c = '../csv/truth/new_t_' + csvPath
            print (c)
            df = pd.read_csv(c , on_bad_lines='skip') 
            dictobj = df.to_dict('list')
            note_events  = []
            header = ['track','start', 'end', 'event','channel','note','velocity','name']
            acc = []
            index = []
            size = len(dictobj['event'])

            print('EVENT' + '\t     NOTE NUMBER' + '\tSTART TIME' + '\tEND TIME'+ '\tDISTANCE')
            for i in range(0, size):
                if dictobj['event'][i] == 'Note_on':
                    event = dictobj['event'][i]
                    time = dictobj['time'][i]
                    note_num = dictobj['note'][i]
                    acc.append(list((event,time,note_num)))
                    index.append(i)
                elif dictobj['event'][i] == 'Note_off':
                    for j in range(0, len(acc)):
                        if dictobj['note'][i] == acc[j][2]:
                            s = acc[j][1]
                            e = dictobj['time'][i]
                            n = acc[j][2]
                            dist = e - s
                            # note - start - end 
                            #print('Note On/Off\t' + str(acc[j][2]) + '\t\t' + str(acc[j][1]) + '\t\t' + str(dictobj['Time'][i])+ '\t\t' + str(dist))
                            note_events.append([1, s, e, 'Note_on', 1, n, dictobj['velocity'][i], note.Note(n).nameWithOctave])
                            acc.pop(j)
                            break
            path = "../csv/truth/t_" + csvPath
            print (note_events)
            with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                # write multiple rows
                writer.writerows(note_events)
        except FileNotFoundError:
            print ('File doesnt exist from modifytruth')

if __name__ == '__main__':
    data = Data()
    #data.modifycsv('jrd.csv')
    # data.read_csv('frj.csv')
    # data.Data_to_csv('frj.csv')
    Data.modifyTruth('jrd.csv')


    

    # Articulation(pattern_dict, truth_dict)



    