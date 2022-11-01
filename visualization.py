import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os
from music21 import note

class Visual:
    def __init__(self) -> None:
        self.Truth = pd.DataFrame()
        self.User = pd.DataFrame()
        self.truth_data = {}
        self.user_data = {}

    def plot_rect(self, delta=0.5):
        """truth_data is a dictionary, {"Label":(low,hi), ... }
        return a drawing that you can manipulate, show, save etc"""
        truth_data = self.truth_data
        user_data = self.user_data
        yspan = len(truth_data)
        yplaces = [.5+i for i in range(yspan)]
        #print(yplaces)
        ylabels = truth_data.keys()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_yticks(yplaces)
        ax.set_yticklabels(ylabels)
        ax.set_ylim((0,yspan))

        # later we'll need the min and max in the union of intervals
        for keys in ylabels:
            try:
                if truth_data[keys] != None:
                    low, hi =  truth_data[keys][0]
                    break
            except:
                pass

        
        for pos, label in zip(yplaces,ylabels):
            if truth_data[label] != None:
                for l in truth_data[label]:
                    #print (f'pos: {pos} label: {label}')
                    start, end = l
                    #print (f'start: {start} end: {end}')
                    t_legend = ax.add_patch(patches.Rectangle((start,pos-delta/2.0),
                                            end-start,delta, linewidth=1, 
                                            edgecolor='r', facecolor='none', label='Truth'))
                    if start<low : low=start
                    if end>hi : hi=end

            if user_data[label] != None:
                for u in user_data[label]:
                    start, end = u
                    #print (f'start: {start} end: {end}')
                    u_legend = ax.add_patch(patches.Rectangle((start,pos-delta/2.0),end-start,0.25, facecolor='b', edgecolor ='black', linewidth = 1,label='User'))

        # little small trick, draw an invisible line so that the x axis
        # limits are automatically adjusted...
        ax.plot((0,hi),(0,0))
        plt.legend(handles=[t_legend,u_legend])
        # now get the limits as automatically computed
        #xmin, xmax = ax.get_xlim()
        # and use them to draw the hlines in your example
        #ax.hlines(range(1,yspan),xmin,xmax)
        # the vlines are simply the x grid lines
        #ax.grid(axis='x')
        # eventually return what we have done
        ax.set_xlabel('Time(s)')
        ax.set_ylabel('Notes')
        # finally save or show what we have
        plt.tight_layout()
        plt.show()


    def Convert(self, df):
        
        #df['note'][0]: [[df['start'][0],df['end'][0]]]}
        midi_note = {}
        low, hi = df['note'].min(), df['note'].max()
        for i in range(low, hi):
            n = note.Note(i).nameWithOctave
            midi_note[n] = None

        # Adding values to the key 
        for x in range(len(df)):
            currentid = note.Note(df.iloc[x,5]).nameWithOctave
            c1, c2 = df.iloc[x,1], df.iloc[x,2]
            try:
                midi_note[currentid].append((c1,c2))
            except:
                midi_note[currentid] = [(c1,c2)]

        return midi_note




    def plot_dynamics(self):
        user = self.User
        condition = (user['track'] == 1)
        time = user[condition].end.to_list()
        velocity = user[condition].velocity.to_list()

        time2 = user[user['track']==2].end.to_list()
        velocity2 = user[user['track']==2].velocity.to_list()
    
        plt.plot(time, velocity, color='red', marker='o')
        plt.plot(time2, velocity2, color='blue', marker='o')
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Year', fontsize=14)
        plt.grid(True)
        plt.show()

    def read_csv(self, pathFileName):
        try:
            abspath = os.path.dirname(__file__)
            truth = os.path.join(abspath, (r"csv\truth\t_" + pathFileName))
            user = os.path.join(abspath, (r"csv\user\u_" + pathFileName))
            self.Truth = pd.read_csv(truth, on_bad_lines='skip')
            self.User = pd.read_csv(user, on_bad_lines='skip') 
            self.truth_data = self.Convert(self.Truth)
            self.user_data = self.Convert(self.User) 
        except:
            print("File doesn't exist")
        

    def data_to_score(self, scores):
        print('TITE')
        pass
    

if __name__ == '__main__':
    v  = Visual()
    v.read_csv('sample.csv')
    v.plot_rect()
    v.plot_dynamics()

    #LOAD CSV FILE TO DICTIONARY
    

    
    # this is the main script, note that we have imported pyplot as plt
    # the data, inspired by your example, 
    # data = {'A':[(1901,1921), (400, 500)] ,
    #         'B':[(1917,1935)],
    #         'C':[(1929,1948)],
    #         'D':[(1943,1963)],
    #         'E':[(1957,1983)],
    #         'F':[(1975,1991)],
    #         'G':[(1989,2007)]}

    # call the function and give its result a name
    # so that we can further manipulate it using the `axes` methods, e.g.
    