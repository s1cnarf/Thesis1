from cmath import e
from tkinter import E
import pandas as pd
import csv
import os

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
                                    elif notes_in_user[y][0] <= i[0] and notes_in_user[y][1] <= i[1]:
                                        if notes_in_user[y][2] == i[2]:
                                            #print(f'Partial: {notes_in_user[y][2]} = {i[2]}, {y}')
                                            truth[idx] = 2
                                            user[y] = 2 
                                            user_articulation['Early'] += 1
                                    
                                        
                #print (f'1 TABLE TRUTH: {truth}')
                #truth = Missed(truth, notes_in_truth, user, notes_in_user)
            

                notes_in_truth.clear()
                notes_in_user.clear()
                
                #print (f'TABLE TRUTH: {truth}')
                #print (f'TABLE USER: {user}')

                correct += truth.count(1)
                partial += truth.count(2)
                extra += user.count(0)
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
        
        mismatch = [i for i, (a, b) in enumerate(zip(pattern_Right, text_Right)) if a != b]

        percentage = (len(mismatch)/len(text_Right))*100
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
        index = 0
        for i in text_dym:
            if i == pattern_dym[index]:
                Success += 1
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

        L_miss = L[m][n]

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


    def Data_to_csv(self):

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
                'Early_Hit:':notes[6],
                'Truth_Dynamics': dynamics[0],
                'User_Dynamics': dynamics[1],
                'LH_Correct' : fingerpattern[0],
                'RH_Correct' :fingerpattern[1],
                'LH_Fail' : fingerpattern[2],
                'RH_Fail' :fingerpattern[3],
                'Melody' : melody}

        with open('csv\Result.csv', 'w') as f:
            for key in data.keys():
                f.write("%s, %s\n" % (key, data[key]))


    def read_csv(self, pathFileName):
        try:
            abspath = os.path.dirname(__file__)
            truth = os.path.join(abspath, (r"csv\truth\t_" + pathFileName))
            pattern = os.path.join(abspath, (r"csv\user\u_" + pathFileName))
            self.Truth = pd.read_csv(truth, on_bad_lines='skip')
            self.Pattern = pd.read_csv(pattern, on_bad_lines='skip')

            #Sort first the data frame
            self.Pattern.sort_values(['start', 'end', 'note'], ascending=[True, True, True], inplace=True)
            self.Truth.sort_values(['start', 'end', 'note'], ascending=[True, True, True], inplace=True)
            
            self.truth_data = self.Truth.to_dict('list')
            self.pattern_data = self.Pattern.to_dict('list')
        except e:
            print("File doesn't exist" + e)


if __name__ == '__main__':
    data = Data()
    data.read_csv('sample.csv')
    data.Data_to_csv()


    

    # Articulation(pattern_dict, truth_dict)



    