import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mticker



sqlite_file = 'userData.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
style.use('fivethirtyeight')

sql_query ="SELECT DateAndTime,Score FROM History WHERE Username = 'ced' ORDER BY date(DateAndTime) ASC"

c.execute("SELECT DateAndTime,Score FROM History WHERE Username = 'ced' ORDER BY date(DateAndTime) ASC")
data = c.fetchall()
#print(data[1])



df = pd.DataFrame(data,columns=['DateAndTime','Score'])

#print(df.loc[:,'Score'])
print(df['DateAndTime'])
df.plot(x='DateAndTime',y='Score',kind='line')
plt.show()
#score = pd.DataFrame

'''
for row in data:
    date.append(row[1])
    score.append(row[3])
    #print(score)
sortedna = sorted(score)
#print(sortedna)

fig = plt.figure(figsize=(13,6))
ax = fig.add_subplot(111)
ax.xaxis_date()
#print(len(data))

myLocator = mticker.MultipleLocator(len(date)/10)
ax.xaxis.set_major_locator(myLocator)
fig.autofmt_xdate()
ax.plot(date,score,'-*')


plt.show()

#print(data)   '''
