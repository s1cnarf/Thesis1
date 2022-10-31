
import pandas as pd
import numpy as np
import functools 
import csv

class chopin:


    @staticmethod

    # Instance method

    # Constraint 1.0 : Note Number Mismatch Detection 
    def Pitch_Verification():
        m_data = pd.read_csv("convertedTwink.csv",error_bad_lines=False) # Truth Data
        w_data = pd.read_csv("TwinkModified.csv",error_bad_lines=False)  # False Data


        #  df[df['ids'].str.contains("ball")]  --> Syntax for Data Query using String Pattern 

        filterData = m_data[m_data['event'].str.contains("Note")]
        filterData_F = w_data[w_data['event'].str.contains("Note")]
        filterData


        # Get the Data of Note Number 
        filterNote_T = filterData['note']
        filterNote_F = filterData_F['note']

        TrueNoteList = filterNote_T.tolist() 
        FalseNoteList =  filterNote_F.tolist() 

        #print(TrueNoteList)
        #print(FalseNoteList)

        # Check if Two CSVs in terms of Note Number Order are the same 
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,TrueNoteList,FalseNoteList), True): 
            print ("The lists True and False are the same") 
        else: 
            print ("The lists True and False are not the same") 
            
        # Extracting the Difference between two values
        DiffList = set(TrueNoteList) ^ set(FalseNoteList)
        print("These are the values that does not match the ground truth in terms of NOTE # ", DiffList)

        # But In order to make this efficient I need to mark the time / area where these difference occur 

        # Search for Multiple Values in CSV 
        # df_values = df[df['myvar'].isin(['element_1', 'element_2'])]
        queryVal = w_data[w_data['note'].isin(DiffList)]
        queryVal


# Checking the order of the Notes 
# Settings: 5 Note Number Comparison 

    # Constraint 2.0:  In Every Note on There is a Note Off with Same Note Number 
    # Constraint 2.1:  Match the distance between Note Off and Note On
    # Constraint 2.2:  Pairing of Velocity with NoteNumber
    def NoteMatching_Verification(self):
        df = pd.read_csv("convertedTwink.csv",error_bad_lines=False) 
        # df.fillna(0, inplace = True)

        # reader = csv.DictReader(open('convertedTwink.csv'))
        # dictobj = next(reader) 
        # dict_from_csv = pd.read_csv("convertedTwink.csv", index=0,   error_bad_lines=False)

        #LOAD CSV FILE TO DICTIONARY
        dictobj = df.to_dict('list')

        # print (dictobj)
        # TEST THE NOTE ON AND NOTE OFF PAIR

        # If note_on_c is True add the note number to the acc list
        # Else, If note_off_c is True
        #           find the note number from the acc list and remove the note number from the list
        #           else pass 
        acc = []
        index = []
        size = len(dictobj['event'])

        print('EVENT' + '\t     NOTE NUMBER' + '\tSTART TIME' + '\tEND TIME'+ '\tDISTANCE')
        for i in range(0, size):
            if dictobj['event'][i] == ' Note_on_c':
                event = dictobj['event'][i]
                time = dictobj['time'][i]
                note_num = dictobj['note'][i]
                acc.append(list((event,time,note_num)))
                index.append(i)
            elif dictobj['event'][i] == ' Note_off_c':
                for j in range(0, len(acc)):
                    if dictobj['note'][i] == acc[j][2]:
                        s = acc[j][1]
                        e = dictobj['time'][i]
                        dist = e - s
                        print('Note On/Off\t' + str(acc[j][2]) + '\t\t' + str(acc[j][1]) + '\t\t' + str(dictobj['time'][i])+ '\t\t' + str(dist))
                        acc.pop(j)
                        break
            

# Manual Terminal 
a = chopin()

a.Pitch_Verification()
