import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mticker


chosen_song = ""
user = ""

#chosen_song = "It's not living if its not with you"
#user = "ced"

def DisplayGraph():


    sqlite_file = 'userData.db'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    #c.execute("SELECT DateAndTime,Score FROM History WHERE Username = 'ced' ORDER BY date(DateAndTime) ASC")
    c.execute("SELECT DateAndTime,Score FROM History WHERE Username = ? AND Title = ? ", (user,chosen_song,))
    data = c.fetchall()

    x_axis = []
    score=[]


    print(len(data))
    count=0

    for row in data:
        count=count+1
        
        string = "Trial " + str(count)
        x_axis.append(string)
        score.append(int(row[1]))


    fig = plt.figure(figsize=(5,5),dpi=100)
    ax = fig.add_subplot(111)
    
    
    #print(len(data))

    #myLocator = mticker.MultipleLocator(len(date)/10)
    #ax.xaxis.set_major_locator(myLocator)
    #fig.autofmt_xdate()
    ax.plot(x_axis,score,'-o',color="#F8BA43")
    plt.xticks(rotation=45)
    plt.ylabel("Scores")
    plt.ylim(0,100)
    
    #plt.show()
    return ax,fig
    #print(x_axis)    




