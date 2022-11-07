from ast import Load
from cgitb import text
# from ast import *
from logging import root
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Progressbar
from typing import Counter
from PIL import ImageTk, Image
from datetime import datetime
from collections import deque
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import proll21 as pr
from threading import Thread
import pygame as pg
import csv
import sqlite3
import pyglet
import get_data 
import visualization
import GraphTest


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        pyglet.font.add_file('Fonts/Lemon Milk.otf')
        pyglet.font.add_file('Fonts/Lemon Milk Light.otf')
        pyglet.font.add_file('Fonts/Montserrat.ttf')
        pyglet.font.add_file('Fonts/Montserrat Italic.ttf')
        pyglet.font.add_file('Fonts/Montserrat Bold.ttf')

        self.title_font = tkfont.Font(family='Montserrat Italic', size=12, slant="italic")
        self.score_font = tkfont.Font(family='Montserrat Bold', size=78, weight="bold")
        self.song_font_after = tkfont.Font(family='Montserrat Bold', size=12, weight="bold")
        self.grade_font = tkfont.Font(family='Montserrat Bold', size=18, weight="bold")
        self.Mont_bold20 = tkfont.Font(family='Montserrat Bold', size=16, weight="bold")
        self.song = tkfont.Font(family='Montserrat Bold', size=13, weight="bold")

        self.title2_font = tkfont.Font(family='Lemon Milk', size=32, weight="bold")
        self.title3_font = tkfont.Font(family='Lemon Milk', size=20, weight="bold")
        self.button_font = tkfont.Font(family='Montserrat Bold', size=16)
        self.button2_font = tkfont.Font(family='Montserrat Italic', size=16)
        self.body_font = tkfont.Font(family='Lemon Milk Light', size=14)
        self.font_song = tkfont.Font(family='Montserrat', size=12)
        self.body2_font = tkfont.Font(family='Lemon Milk', size=16, weight="bold")
        self.body3_font = tkfont.Font(family='Lemon Milk', size=12)
        
        self.Mont_bold26 = tkfont.Font(family='Montserrat Bold', size=26, weight="bold")
        self.Mont_bold14 = tkfont.Font(family='Montserrat Bold', size=14, weight="bold")

        ttk.Style().configure("Treeview", background="black", foreground="white", fieldbackground="black")

        # D A T A   B A S E

        con = sqlite3.connect('userData.db')
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS record(
                        Username text,
                        Email text,
                        ContactNo number,
                        Password text
                        )
                    ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS History(
                        Username text,
                        DateAndTime text,
                        Title text,
                        Score text
                        )
                    ''')
        con.commit()
        con.close()

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (
        LoadingPage, LogIn, Register, StartPage, PlayPage, AfterPerformance, ScoreSummary, ErrorAnalysis, PerformanceReport, Statistics,
        History):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame("StartPage")
        self.show_frame("LogIn")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller
        # self.controller.state("zoomed")
        # self.update_idletasks()

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((386, 82))
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_label = tk.Label(self, image=logo_img, borderwidth=0)
        logo_label.image = logo_img
        logo_label.place(x=400, y=285)

        loading = tk.Frame(self, bg="#281801")
        loading.pack_propagate(False)
        loading.configure(width=10, height=3)
        loading.place(x=410, y=389)

        self.after(200)

        def comm():

            current = loading['width']

            if current == 365:
                self.destroy()
                # controller.show_frame("LogIn")

            if current < 365:
                loading.config(width=current + 71)
                self.after(500, comm)

        self.after(1000, comm)


class LogIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        # self.controller.state("zoomed")
        global ShowStartPage
        def ShowStartPage(e):
            UpdateDeviceStatus()
            controller.show_frame("StartPage")

        def login(e):
            try:
                global uname
                uname = label_entry.get()
                passw = label2_entry.get()
                counter = 0
                if uname == "":
                    warn = "Username can't be empty"
                else:
                    counter += 1

                if passw == "":
                    warn = "Password can't be empty"
                else:
                    counter += 1

                if counter == 2:
                    con = sqlite3.connect('userData.db')
                    c = con.cursor()
                    c.execute("Select * from record WHERE Username = ? AND PASSWORD = ?", (uname, passw))
                    # if (c.execute("Select * from record WHERE Username = '{uname}' AND PASSWORD = '{passw}'")):

                    if (c.fetchone()):
                        messagebox.showinfo('Login Status', 'Successfuly Login')

                        ShowStartPage(e)
                    else:
                        messagebox.showerror('Login Status', 'Invalid Username or Password')

                    c.close()
                else:
                    messagebox.showerror('', warn)

                # first try code (after closing the program the first user who register cant log in)
                # con = sqlite3.connect('userData.db')
                # c = con.cursor()
                # for row in c.execute("Select * from record"):
                #     Username = row[0]
                #     Password = row[3]
                # con = sqlite3.connect('userData.db')
                # c = con.cursor()
                # c.execute("Select * from record WHERE Username = '{uname} AND PASSWORD = '{passw}")

            except Exception as ep:
                messagebox.showerror('', ep)

            # ==================================================
            # global uname
            # uname = label_entry.get()
            # passw = label2_entry.get()
            # counter = 0
            # if uname == "":
            #     warn = "Username can't be empty"
            # else:
            #     counter += 1

            # if passw == "":
            #     warn = "Password can't be empty"
            # else:
            #     counter += 1

            # if counter == 2:
            #     if (uname == Username and passw == Password):
            #         messagebox.showinfo('Login Status', 'Successfuly Login')
            #         controller.show_frame("StartPage")
            #     else:
            #         messagebox.showerror('Login Status', 'Invalid Username or Password')
            # else:
            #     messagebox.showerror('',warn)

            # =========================================================

            # file = open ('registersheet.txt' ,'r')
            # d = file.read()
            # r = ast.literal_eval(d)
            # file.close()

            # print(r.keys())
            # print(r.values())
            # print(r)

            # if uname in r.keys() and passw==r[uname]:
            #     controller.show_frame("StartPage")

            # else:
            #     messagebox.showerror('Invalid', 'Invalid username and password')

        frame1 = tk.Frame(self, width=463, height=461, bg="#2A2B2C", border=0)
        label = tk.Label(self, text="Username", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label2 = tk.Label(self, text="Password", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        # sign_in = tk.Label(self, text="Sign In",fg="#F7BF50", bg="#2A2B2C", font=controller.title_font)

        line = tk.Frame(self, bg="#281801")
        line.configure(width=1, height=595)
        line.place(x=600, y=66)

        def on_enter(e):
            label_entry.delete(0, 'end')

        def on_leave(e):
            name = label_entry.get()
            if name == '':
                label_entry.insert(0, 'Enter Username')

        global label_entry
        label_entry = tk.Entry(self, width=28, font=controller.title_font)
        label_entry.insert(0, "Enter your username")
        label_entry.bind('<FocusIn>', on_enter)
        label_entry.bind('<FocusOut>', on_leave)
        label_entry.focus_set()

        def on_enter(e):
            label2_entry.delete(0, 'end')

        def on_leave(e):
            name = label2_entry.get()
            if name == '':
                label2_entry.insert(0, 'Password')

        label2_entry = tk.Entry(self, width=28, font=controller.title_font, show="*")
        label2_entry.insert(0, "Enter your password")
        label2_entry.bind('<FocusIn>', on_enter)
        label2_entry.bind('<FocusOut>', on_leave)
        label2_entry.bind('<Return>', login)

        logo_pic = Image.open("Pictures/Logo.png") #Resampling.LANCZOS   1Resampoling.LANCZOS
        logo_pic = logo_pic.resize((386, 82), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_pic = Image.open("Pictures/info.png")
        # logo_pic= logo_pic.resize((430,52),Image.Resampling.LANCZOS)
        info_img = ImageTk.PhotoImage(logo_pic)

        names_pic = Image.open("Pictures/names.png")
        names_img = ImageTk.PhotoImage(names_pic)

        img = Image.open("Pictures/LogIn.png")
        LogIn_img = ImageTk.PhotoImage(img)

        logo_label = tk.Label(self, image=logo_img, borderwidth=0)
        logo_label.image = logo_img

        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        names_label = tk.Label(self, image=names_img, borderwidth=0)
        names_label.image = names_img




        log_in = tk.Label(self, image=LogIn_img ,cursor="hand2", borderwidth=0)
        log_in.image = LogIn_img
        log_in.bind("<Button-1>", login)

        register = tk.Label(self, text="Register", fg="#F7BF50", bg="#2A2B2C", cursor="hand2", borderwidth=0,
                            font=controller.button2_font)
        register.bind("<Button-1>", lambda e: controller.show_frame("Register"))

        frame1.place(x=671, y=143)
        label.place(x=746, y=214)
        label2.place(x=746, y=322)
        # sign_in.place(x=540,y=220)

        label_entry.place(x=746, y=253)
        label2_entry.place(x=746, y=362)

        # logo_label.place(x=35,y=34)
        # info_label.place(x=728, y=57)
        # names_label.place(x=362, y=677)

        logo_label.place(x=123, y=270)
        info_label.place(x=98, y=416)
        names_label.place(x=660, y=660)

        log_in.place(x=821, y=471)
        register.place(x=859, y=510)


class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        def insertUser(e):
            counter = 0
            warn = ""
            # Getting the username input
            if labelReg_entry.get() == "":
                warn = "Name can't be empty"
            else:
                counter += 1
            # Getting the password input
            if label2Reg_entry.get() == "":
                warn = "Password can't be empty"
            else:
                counter += 1
            # Getting the contact number input
            if label3Reg_entry.get() == "":
                warn = "Contact Number can't be empty"
            else:
                counter += 1
            # Getting the email input
            if label4Reg_entry.get() == "":
                warn = "Email can't be empty"
            else:
                counter += 1

            if label2Reg_entry.get() != label5Reg_entry.get():
                warn = "Password didn't match!"
            else:
                counter += 1

            con = sqlite3.connect("userData.db")
            c = con.cursor()

            c.execute("SELECT * FROM record WHERE Username = ?",(labelReg_entry.get(),))
            if c.fetchall():
                warn = "Username is already taken!"
            else:
                counter +=1
            
            con.commit()
            con.close()

            if counter == 6:
                try:
                    con = sqlite3.connect('userData.db')
                    cur = con.cursor()
                    cur.execute("INSERT INTO record VALUES (:Username, :Email, :ContactNo, :Password) ", {
                        'Username': labelReg_entry.get(),
                        'Email': label4Reg_entry.get(),
                        'ContactNo': label3Reg_entry.get(),
                        'Password': label2Reg_entry.get()

                    })
                    con.commit()
                    con.close()
                    messagebox.showinfo('confirmation', 'Record Saved')
                    controller.show_frame("LogIn")

                except Exception as ep:
                    messagebox.showerror('', ep)
            else:
                messagebox.showerror('Error', warn)

        # def register(event):
        # username = labelReg_entry.get()
        # password = label2Reg_entry.get()
        # contactNo = label3Reg_entry.get()
        # email = label4Reg_entry.get()
        # confirmPass = label5Reg_entry.get()

        # if password == confirmPass:
        #     try:
        #         file = open('registersheet.txt','r+')
        #         d = file.read()
        #         r = ast.literal_eval(d)

        #         dict2 = {username:password ,contactNo:email}
        #         r.update(dict2)
        #         file.truncate(0)
        #         file.close()

        #         file = open('registersheet.txt','w')
        #         w = file.write(str(r))

        #         messagebox.showinfo('Signup','Sucessfully Sign Up')

        #     except:
        #         file = open('registersheet.txt','w')
        #         displayDict = str({'Username':'Password','Contact No.':'Email'})
        #         file.write(displayDict)
        #         file.close()

        # else:
        #     messagebox.showerror('Invalid',"Both Password Should Match")

        frame_reg = tk.Frame(self, width=860, height=480, bg="#2A2B2C", border=0)
        label_reg = tk.Label(self, text="CREATE ACCOUNT", fg="#F7BF50", bg="#2A2B2C", font=controller.body2_font)

        labelReg = tk.Label(self, text="USERNAME", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        labelReg_entry = tk.Entry(self, width=29, font=controller.title_font)

        label2Reg = tk.Label(self, text="PASSWORD", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label2Reg_entry = tk.Entry(self, width=29, font=controller.title_font, show="*")

        label3Reg = tk.Label(self, text="CONTACT NO.", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label3Reg_entry = tk.Entry(self, width=29, font=controller.title_font)
        label3Reg_entry.bind("<Return>", insertUser)

        label4Reg = tk.Label(self, text="EMAIL", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label4Reg_entry = tk.Entry(self, width=29, font=controller.title_font)

        label5Reg = tk.Label(self, text="CONFIRM PASSWORD", fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label5Reg_entry = tk.Entry(self, width=29, font=controller.title_font, show="*")
        label5Reg_entry.bind("<Return>", insertUser)

        label6Reg = tk.Label(self, text="I already have an account", fg="grey", bg="#2A2B2C", font=controller.font_song)
        label7Reg = tk.Label(self, text="Sign In", cursor="hand2", fg="#F7BF50", bg="#2A2B2C", borderwidth=0)
        label7Reg.bind("<Button-1>", lambda e: controller.show_frame("LogIn"))

        reg_button = tk.Label(self, text="REGISTER", bg="#F7BF50", fg="#2A2B2C", cursor="hand2", borderwidth=0,
                              width=13, height=2, font=controller.button_font)
        reg_button.bind("<Button-1>", insertUser)

        # reg_button = Button(self, text="REGISTER",bg="#F7BF50", fg="#2A2B2C", cursor ="hand2", borderwidth=0, width=13, height=2 ,font=controller.button_font)
        # reg_button.bind("<Button-1>",register)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((250, 55), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_pic = Image.open("Pictures/info.png")
        # logo_pic= logo_pic.resize((430,52),Image.Resampling.LANCZOS)
        info_img = ImageTk.PhotoImage(logo_pic)

        logo_label = tk.Label(self, image=logo_img, borderwidth=0)
        logo_label.image = logo_img

        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        frame_reg.place(x=180, y=134)
        label_reg.place(x=510, y=170)

        labelReg.place(x=220, y=220)
        labelReg_entry.place(x=223, y=255)

        label2Reg.place(x=220, y=320)
        label2Reg_entry.place(x=223, y=355)

        label3Reg.place(x=220, y=420)
        label3Reg_entry.place(x=223, y=455)

        label4Reg.place(x=650, y=220)
        label4Reg_entry.place(x=653, y=255)

        label5Reg.place(x=650, y=320)
        label5Reg_entry.place(x=653, y=355)

        reg_button.place(x=700, y=450)
        label6Reg.place(x=655, y=510)
        label7Reg.place(x=870, y=515)

        logo_label.place(x=35, y=34)
        info_label.place(x=728, y=57)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller
        self.controller.title("Chop-In")
        
        

        # self.controller.state("zoomed")
        
        def DisplayStatistics(e):
            UpdateValues()
            controller.show_frame("Statistics")

        def CombineFunctions(e):
            UpdateHistory()
            controller.show_frame("History")

        def _create_circle(self, x, y, r, **kwargs):
            return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        
        tk.Canvas.create_circle = _create_circle

       
        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((386, 82), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        image = Image.open("Pictures/menu1.png")
        # image = image.resize((40,49), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu2.png")
        # image = image.resize((67,53), Image.Resampling.LANCZOS)
        img2 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu3.png")
        # image = image.resize((88,53), Image.Resampling.LANCZOS)
        img3 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu4.png")
        # image = image.resize((69,53), Image.Resampling.LANCZOS)
        img4 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/DeviceDetect.png")
        # image = image.resize((69,53), Image.Resampling.LANCZOS)
        img5 = ImageTk.PhotoImage(image)

        logo_label = tk.Label(self, image=logo_img, borderwidth=0)
        logo_label.image = logo_img

        play_label = tk.Label(self, image=img, cursor="hand2", borderwidth=0)
        play_label.bind("<Button-1>", lambda e: controller.show_frame("PlayPage"))
        play_label.image = img

        play_label2 = tk.Label(self, image=img2, cursor="hand2", borderwidth=0)
        play_label2.bind("<Button-1>", DisplayStatistics)
        play_label2.image = img2

        play_label3 = tk.Label(self, image=img3, cursor="hand2", borderwidth=0)
        play_label3.bind("<Button-1>", CombineFunctions)
        play_label3.image = img3

        play_label4 = tk.Label(self, image=img4, cursor="hand2", borderwidth=0)
        play_label4.bind("<Button-1>", lambda e: controller.show_frame("LogIn"))
        play_label4.image = img4

        DetectDevice_label = tk.Label(self, image=img5, borderwidth=0,cursor="hand2")
        DetectDevice_label.image = img5
        
        canvas = tk.Canvas(self, width=20, height=20, bg="#2A2B2C",highlightthickness=0)
        
        global UpdateDeviceStatus
        def UpdateDeviceStatus():
            canvas.delete('all')
            pg.midi.init()
            global device_id
            device_id=pg.midi.get_default_input_id()
            
                
            if (device_id == 1):
                canvas.create_circle(10, 10, 8, fill="#75CE9F", outline="")
                
                
            else:
                canvas.create_circle(10, 10, 8, fill="#ED695E", outline="")
                print(id)
                
            #device_id=-1
            pg.midi.quit()

        UpdateDeviceStatus()

        def ClickUpdate(e):
            UpdateDeviceStatus()
        
        DetectDevice_label.bind("<Button-1>", ClickUpdate)

        logo_label.place(x=400, y=200)
        play_label.place(x=364, y=375)
        play_label2.place(x=490, y=375)
        play_label3.place(x=644, y=374)
        play_label4.place(x=792, y=375)
        DetectDevice_label.place(x=919, y=26)
        canvas.place(x=955, y=47)


class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        flag = True
        

        def update(task, flag):
            listbox_songs.delete(0, END)

            for item in task:

                item = item[:-4]
                if flag:
                    PlayCount_Dictionary[item] = 0  # the 0 is the play count
                listbox_songs.insert(END, item)
            flag = False

        def GetSongList(e):
            song = listbox_songs.get(ANCHOR)
            search_entry.delete(0, END)

            search_entry.insert(0, song)
            # tree_histo.selection_clear()

        def GetSongList2(e):
            song2 = listbox.get(ANCHOR)

            search_entry.delete(0, END)
            search_entry.insert(0, "")
            search_entry.insert(0, song2)
            return None

        global infos

        def infos(e):
            app.withdraw()
            print("ACCESS INFOS")

            if __name__ == '__main__':
                p = pr.pRoll()

                # print ('start ', tm.time())

                # print("TIME IN TICKS/S: ", pg.time.get_ticks() / 1000)
                # Start playing midi File in separate Thread

                thread = Thread(target=p.play_notes)

                font = pg.font.SysFont('Calibri', 40)
                # display = pg.display.set_mode((1248, 500))

                display = pg.display.set_mode((1540, 800))

                wait = True
                fps = 120

                p.running = True

                p.launch()
                #thread.start()
                # thread.start()
                p.piano.create_key_surfaces(display)

                while p.running:
                    # print("LOOP BACK: ", pr.lp)
                    p.lp = p.lp + 1

                    # print(pr.clock.get_fps())
                    # print(f'FPS : {pr.clock.get_fps()}')
                    # print(f'Ticks: {pg.time.get_ticks()}')

                    # Calculate piano roll offset

                    offset = p.time * 100 + 600
                    # update keys
                    p.display.blit(p.background, (0, 0))
                    p.draw(p.display, offset)
                    pg.display.update(0, 0, 1540, 600)

                    # pr.piano.draw_keys(display)

                    # # pg.display.flip()
                    if wait:
                        pg.time.delay(5000)
                        # print("BOOOL",pg.midi.get_init())
                        wait = False
                        thread.start()

                    p.input_main(display)
                    '''
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            p.running = False  ''' 

                    p.clock.tick(fps)

                if p.threadFalse:

                    print("INFO  DATA: ", "TRACK--TIME--EVENT--NOTE--VELOCITY")
                    for i in p.list_a:
                        print("INPUT DATA: ", i)

                    fields = ['track', 'time', 'event', 'note', 'velocity']
                    csvPath = p.sMusic + '.csv'
                    path = "../csv/" + csvPath

                    with open(path, 'w', encoding='UTF8', newline='') as f:
                        # using csv.writer method from CSV package
                        write = csv.writer(f)
                        write.writerow(fields)
                        write.writerows(p.list_a)
                        print("SUCCESFULLY ENCODED TO CSV!")

                # Makes sure thread has stopped before ending program
                if thread.is_alive():
                    thread.join()

                if p.running == False:
                    print("QUIT ACCESS")
                    pg.midi.quit()
                    # print("MIDI STATUS: ", pg.midi.get_init(), "CURRENT TIME: ",pg.midi.time())
                    pg.midi.init()
                    print("MIDI STATUS: ", pg.midi.get_init())
                    print("CURRENT TIME: ", pg.midi.time())
                    p.acc = True
                    pg.quit()
                    pg.display.quit()
                    p.threadFalse = False
                    p.start = 0
                    p.midiStart = 0
                    p.sMusic = ""

                app.deiconify()
                DisplayAfterPerf(e)
                




            # controller.show_frame("PianoRoll")

        def search(e):
            typed = search_entry.get()
            length_of_typed = len(typed)

            if typed == '':
                task = songs
            else:
                task = []
                for item in songs:
                    if typed.lower() in item.lower()[0:length_of_typed]:
                        task.append(item)

            update(task, flag)

        # Create Stack For Recents
        stack = deque()
        stack2 = deque()
        index_stack = 0

        # Create Dictionary for Most Played
        PlayCount_Dictionary = {}

        def callback(event):
            selection = search_entry.get()
            if selection:
                print("goods")
                # search_entry.delete(0, END)
                # listbox2.insert("end",x)
                # print(x)
            else:
                listbox.get(ANCHOR)

        global PushSongInStack

        def PushSongInStack(event):

            data = search_entry.get()
            pr.getSong = data

            print("MUSIC DATA: ", data)
            dt = datetime.now()
            dt_string = dt.strftime(" %d-%m-%Y %H:%M:%S")

            stack.append(data)
            stack2.append(data)

            song = stack2.pop()

            listbox.insert(index_stack, song)
            index_stack + 1
            song_label.configure(text=data)
            #df = pd.read_csv('Result_jrd.csv', on_bad_lines='skip')
            #df_dict = df.to_dict('list')

            #fail = df_dict['Data'][15]
            #total = correct + fail
            #percent = (correct/total) * 100
            con = sqlite3.connect('userData.db')
            cur = con.cursor()
            cur.execute("INSERT INTO History VALUES (:Username, :DateAndTime, :Title, :Score) ", {
                'Username': uname,
                'DateAndTime': dt_string,
                'Title': song,
                'Score': '0'#round(percent)

            })
            con.commit()
            con.close()
            print("INSERTED")

        global infos2

        def infos2(e):
            selectedItem = tree_histo.focus()
            search_entry.delete(0, END)
            try:
                data2 = tree_histo.item(selectedItem)['values'][1] 
                score = tree_histo.item(selectedItem)['values'][2] 

                ScoreToRating(score)

                song_label.config(text=data2)
                score_label.config(text = score)
                #grade_label.config(text=str(level))

                
                
                controller.show_frame("AfterPerformance")
                show_csv()
            except IndexError:
                print("ayos lang")

        global combinedFunc

        def combinedFunc(e):
            '''
            if device_id == 1:
                PushSongInStack(e)
                infos(e)
            else:
                messagebox.showerror('', "Please Connect a Device!")
            '''

            PushSongInStack(e)
            infos(e)
            


        image = Image.open("Pictures/recents.png")
        # image = image.resize((40,49), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/songs.png")
        # image = image.resize((10,30), Image.Resampling.LANCZOS)
        img2 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/searchIcon.png")
        # image = image.resize((25,28), Image.Resampling.LANCZOS)
        img4 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/playButton.png")
        # image = image.resize((25,28), Image.Resampling.LANCZOS)
        img5 = ImageTk.PhotoImage(image)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((250, 55), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img, borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", ShowStartPage)
        logo_label.image = logo_img

        img6 = Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img6)
        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        # search_frame = tk.Frame(self,width=259,height=30,bg="#2A2B2C",border=0)

        # black rectangle
        frame2_play = tk.Frame(self, width=1028, height=447, bg="#2A2B2C", border=0)

        # song label
        label_play = tk.Label(self, image=img2, border=0)
        label_play.image = img2

        frame3 = tk.Frame(self, width=262, height=51, border=0, bg="#2A2B2C")
        frame3.place(x=450, y=190)

        global search_entry
        search_entry = tk.Entry(frame3, width=16, border=0, font=controller.title_font, bg="#ffffff", fg="#000000")

        label_search = tk.Label(frame3, image=img4, border=0)
        label_search.image = img4

        label_search.pack(side=LEFT, padx=2)
        search_entry.pack(side=LEFT)

        line = tk.Frame(self, width=1, height=386, border=0, bg="#F8BA43")
        line.place(x=750, y=175)

        play_Button = tk.Label(self, image=img5, border=0, cursor="hand2")
        play_Button.image = img5

        label_recent = tk.Label(self, image=img, border=0)
        label_recent.image = img

        frame1 = tk.Frame(self, width=226, height=306, border=0, bg="#2A2B2C")
        frame1.place(x=831, y=256)

        listbox = tk.Listbox(frame1, width=19, height=13, fg="#FFFFFF", bg="#2A2B2C", borderwidth=0,
                             font=controller.font_song)
        scrollbar = tk.Scrollbar(frame1, orient=VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        # listbox.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        # scrollbar.place(x=365,y=259)
        listbox.pack(pady=1)

        listbox.bind("<<ListboxSelect>>", GetSongList2)

        # listbox.bind("<<ListboxSelect>>", PushSongInStack)

        frame2 = tk.Frame(self, width=549, height=294, border=0, bg="#2A2B2C")
        frame2.place(x=136, y=256)

        listbox_songs = tk.Listbox(frame2, width=46, height=13, fg="#FFFFFF", bg="#2A2B2C", borderwidth=0,
                                   font=controller.font_song)
        scrollbar2 = tk.Scrollbar(frame2, orient=VERTICAL)
        listbox_songs.config(yscrollcommand=scrollbar2.set)
        # listbox.pack(side="top", fill="both", expand=True)
        scrollbar2.config(command=listbox_songs.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)
        # scrollbar.place(x=365,y=259)
        listbox_songs.pack(pady=1)

        # POPULAR

        with open('songs.txt', 'r') as f:
            songs = [line.strip() for line in f]

        update(songs, flag)

        # listbox2.bind("<<ListboxSelect>>",IncrementPlayCount)

        # listbox2.bind("<<ListboxSelect>>", fillout)

        search_entry.bind("<KeyRelease>", search)

        listbox_songs.bind("<<ListboxSelect>>", GetSongList)

        play_Button.bind("<Button-1>", combinedFunc)
        # play_Button.bind("<<ListboxSelect>>", CombineFunctions)

        '''
        img = Image.open("Pictures/practice.png")
        practice_img = ImageTk.PhotoImage(img)
        practice_label = tk.Label(self, image=practice_img, borderwidth=0,cursor='hand2')
        practice_label.image = practice_img

        img = Image.open("Pictures/listen.png")
        listen_img = ImageTk.PhotoImage(img)
        listen_label = tk.Label(self, image=listen_img, borderwidth=0,cursor='hand2')
        listen_label.image = listen_img
        
        
        practice_label.place(x=115,y=635)
        listen_label.place(x=344,y=635)
        '''

        play_Button.place(x=1013, y=635)

        logo_label.place(x=35, y=34)
        info_label.place(x=728, y=57)
        label_recent.place(x=831, y=179)

        frame2_play.place(x=90, y=148)
        label_play.place(x=138, y=179)
        # label2_play.place(x=550, y=180)


class AfterPerformance(tk.Frame):

    def __init__(self, parent, controller):
        print("after")
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller
        self.controller.title("Chop-In")
        
        def CombineFunError(event):
            show_data()
            controller.show_frame("ErrorAnalysis")
            

        global DisplayAfterPerf
        def DisplayAfterPerf(e):
            show_csv()
            controller.show_frame("AfterPerformance")

        def show_scoreSummary(e):
            controller.show_frame("ScoreSummary")
            show_summary()
            
        def DisplayPerfReport(e):
            lastna()
            controller.show_frame("PerformanceReport")
        
        


        global show_csv
        def show_csv():
            score_label.config(text="")
            grade_label.configure(text="")
            song_label.configure(text="")
            

            getsong = search_entry.get() + '.csv'
            
            d = get_data.Data()
            d.modifycsv(getsong)
            d.read_csv(getsong)
            d.Data_to_csv(getsong)

            pathh = r'../csv/Result_' + getsong
            try:
                dff = pd.read_csv(pathh, on_bad_lines='skip')
            except FileNotFoundError:
                print('File doesnt exist!')

            #Notes
            correctHits = dff.loc[dff["Element"] == "Correct", "Data"].iloc[0]
            partialHits = dff.loc[dff["Element"] == "Partial", "Data"].iloc[0]
            extraHits = dff.loc[dff["Element"] == "Extra", "Data"].iloc[0]
            missedHits = dff.loc[dff["Element"] == "Missed", "Data"].iloc[0]
            global total_notes
            total_notes = correctHits + partialHits + missedHits
            semiTotal_notes = correctHits + partialHits
            percent_notes = semiTotal_notes/total_notes *100
            global total_percentNotes
            total_percentNotes = float(percent_notes * 0.25)
            print(total_percentNotes,"eto ang percentNotes")

            #Rhythm
            sswitchHits = dff.loc[dff["Element"] == "Success_Switch", "Data"].iloc[0]
            fswitchHits = dff.loc[dff["Element"] == "Failed_Switch", "Data"].iloc[0]
            total_rhythm = sswitchHits + fswitchHits
            percent_rhythm = (sswitchHits/total_rhythm)*100
            global total_percentRhythm
            total_percentRhythm = float(percent_rhythm * 0.20)
            print(total_percentRhythm,"eto ang percentrhythms")

            #Articulation
            timedHits = dff.loc[dff["Element"] == "Timed_Hit", "Data"].iloc[0]
            lateHits = dff.loc[dff["Element"] == "Late_Hit", "Data"].iloc[0]
            earlyHits = dff.loc[dff["Element"] == "Early_Hit", "Data"].iloc[0]
            percent_articulation = (timedHits/total_notes)*100
            global total_percentArticulation
            total_percentArticulation = float(percent_articulation * 0.15)
            print(total_percentArticulation,"eto ang articulation")

            #Dynamics
            truthDynamicHits = dff.loc[dff["Element"] == "Truth_Dynamics", "Data"].iloc[0]
            userDynamicHits = dff.loc[dff["Element"] == "User_Dynamics", "Data"].iloc[0]
            percent_dynamics = (userDynamicHits/truthDynamicHits)*100
            global total_percentDynamics
            total_percentDynamics = float(percent_dynamics * 0.10)
            print(total_percentDynamics,"eto ang percentdynamics")

            #Melody
            melodyHits = dff.loc[dff["Element"] == "Melody", "Data"].iloc[0]
            percent_melody = melodyHits
            global total_percentMelody
            total_percentMelody = float(percent_melody*0.30)
            print(total_percentMelody,"Eto ang melody")

            #LeftHand
            leftcorrectHits = dff.loc[dff["Element"] == "LH_Correct", "Data"].iloc[0]
            leftfailtHits = dff.loc[dff["Element"] == "LH_Fail", "Data"].iloc[0]
            total_left = leftcorrectHits + leftfailtHits
            percent_left = (leftcorrectHits/total_left)*100
            global total_percentLeft
            total_percentLeft = float(percent_left * 0.05)
            print(total_left,"eto ang percentleft")

            #RightHand
            rightcorrectHits = dff.loc[dff["Element"] == "RH_Correct", "Data"].iloc[0]
            rightfailHits = dff.loc[dff["Element"] == "RH_Fail", "Data"].iloc[0]
            total_right = rightcorrectHits + rightfailHits
            percent_right = (rightcorrectHits/total_right)*100
            global total_percentRight
            total_percentRight = float(percent_right * 0.10)
            print(total_percentRight,"eto ang perceentright")


            
            global percentScore
            percentScore = float(total_percentNotes + total_percentRhythm + total_percentArticulation + total_percentDynamics + total_percentMelody)
            percentScore = round(percentScore)
            score_label.configure(text=str(percentScore))
            print(percentScore,"ETO ANG SCORE")

            con = sqlite3.connect('userData.db')
            cur = con.cursor()
            cur.execute("UPDATE History Set Score = ? WHERE Score = 0",(str(percentScore),))
            print("TAENA MO")

            con.commit()
            con.close()

            rating=ScoreToRating(percentScore)
            
    
            grade_label.configure(text=str(rating))
            song_label.configure(text=search_entry.get())
            

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((250, 55), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img, borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", ShowStartPage)
        logo_label.image = logo_img

        img = Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img)
        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        main_frame = tk.Frame(self, width=988, height=545, bg="#2A2B2C", border=0)

        img = Image.open("Pictures/ScoreSum.png")
        scoreSum_img = ImageTk.PhotoImage(img)
        ScoreSummary_label = tk.Label(self, image=scoreSum_img, cursor="hand2", borderwidth=0)
        ScoreSummary_label.bind("<Button-1>", show_scoreSummary)
        ScoreSummary_label.image = scoreSum_img

        img = Image.open("Pictures/Perf_Report.png")
        PerfReport_img = ImageTk.PhotoImage(img)
        PerfReport_label = tk.Label(self, image=PerfReport_img, cursor="hand2", borderwidth=0)
        PerfReport_label.bind("<Button-1>", DisplayPerfReport)
        PerfReport_label.image = PerfReport_img
          
        img = Image.open("Pictures/ErrAnal.png")
        ErrorAnal_img = ImageTk.PhotoImage(img)
        ErrorAnal_label = tk.Label(self, image=ErrorAnal_img, cursor="hand2", borderwidth=0)
        ErrorAnal_label.bind("<Button-1>", CombineFunError)
        ErrorAnal_label.image = ErrorAnal_img

        img = Image.open("Pictures/circle.png")
        circle_img = ImageTk.PhotoImage(img)
        circle_label = tk.Label(self, image=circle_img, borderwidth=0)
        circle_label.image = circle_img

        img = Image.open("Pictures/BackToHome.png")
        back_img = ImageTk.PhotoImage(img)
        back_label = tk.Label(self, image=back_img, borderwidth=0,cursor='hand2')
        back_label.bind("<Button-1>", ShowStartPage)
        back_label.image = back_img
        
        global song_label
        global score_label
        global grade_label

        score_frame = tk.Frame(self, width=254, height=95, border=0, bg="#2A2B2C")
        score_frame.pack_propagate(False)
        score_label = tk.Label(score_frame, text="", borderwidth=0, bg="#2A2B2C", fg="white", font=controller.score_font)
        score_label.pack(anchor=CENTER)

        song_frame = tk.Frame(self, width=308, height=30, border=0, bg="#2A2B2C")
        song_frame.pack_propagate(False)
        song_label = tk.Label(song_frame, text="", borderwidth=0, bg="#2A2B2C", fg="white",
                              font=controller.song_font_after)
        song_label.pack(anchor=CENTER, pady=5)

        grade_frame = tk.Frame(self, width=308, height=30, bg="#2A2B2C", border=0)
        grade_frame.pack_propagate(False)
        
        global grade_label
        grade_label = tk.Label(grade_frame, text="", borderwidth=0, bg="#2A2B2C", fg="#F8BA43",
                               font=controller.grade_font)
        grade_label.pack(anchor=CENTER)

        logo_label.place(x=35, y=34)
        info_label.place(x=728, y=57)
        main_frame.place(x=105, y=124)
        back_label.place(x=752,y=615)

        ScoreSummary_label.place(x=613, y=209)
        PerfReport_label.place(x=679, y=354)
        ErrorAnal_label.place(x=613, y=499)

        circle_label.place(x=182, y=192)
        score_frame.place(x=208, y=286)
        song_frame.place(x=182, y=520)
        grade_frame.place(x=182, y=570)

class ScoreSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller
        

        img = Image.open("Pictures/ScoreSummary.png")
        scoreSum_title_img = ImageTk.PhotoImage(img)
        scoreSum_title_label = tk.Label(self, image=scoreSum_title_img, borderwidth=0)
        scoreSum_title_label.image = scoreSum_title_img
    
        back_pic = Image.open("Pictures/back.png")
        back_img = ImageTk.PhotoImage(back_pic)
        back_label = tk.Label(self, image=back_img, borderwidth=0, cursor="hand2")
        back_label.bind("<Button-1>", DisplayAfterPerf)
        back_label.image = back_img


        main_frame = tk.Frame(self, width=988, height=563, bg="#2A2B2C", border=0)

        notes_label = tk.Label(self, text="Played the right note correctly [NOTES - 25%]: ", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=38,
                          height=1, font=controller.title3_font)

        notes_score = tk.Label(self, text="", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=5,
                          height=1, font=controller.title3_font)

        rhythm_label = tk.Label(self, text="Followed the corerct rhythm pattern [RHYTHM - 20%]: ", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=43,
                          height=1, font=controller.title3_font)

        rhythm_score = tk.Label(self, text="", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=5,
                          height=1, font=controller.title3_font)

        articulation_label = tk.Label(self, text="Hold each note to it's corresponding duration [ARTICULATION - 15%]: ", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=54,
                          height=1, font=controller.title3_font)

        articulation_score = tk.Label(self, text="", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=5,
                          height=1, font=controller.title3_font)

        dynamics_label = tk.Label(self, text="Controlled the loudness of each note [DYNAMICS - 10%]: ", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=45,
                          height=1, font=controller.title3_font)

        dynamics_score = tk.Label(self, text="", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=5,
                          height=1, font=controller.title3_font)

        melody_label = tk.Label(self, text="Performed the Melody correctly [MELODY - 30%]: ", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=40,
                          height=1, font=controller.title3_font)

        melody_score = tk.Label(self, text="", bg="#2A2B2C", fg="#F7BF50", cursor="hand2", borderwidth=0, width=5,
                          height=1, font=controller.title3_font)

        global show_summary
        def show_summary():
            notes_score.configure(text=str(round(total_percentNotes)),anchor=CENTER)
            rhythm_score.configure(text=str(round(total_percentRhythm)),anchor=CENTER)
            articulation_score.configure(text=str(round(total_percentArticulation)),anchor=CENTER)
            dynamics_score.configure(text=str(round(total_percentDynamics)),anchor=CENTER)
            melody_score.configure(text=str(round(total_percentMelody)),anchor=CENTER)



        main_frame.place(x=105, y=124)
        back_label.place(x=57, y=36)
        scoreSum_title_label.place(x=930,y=45)
        notes_label.place(x=110, y=270)
        notes_score.place(x=595, y=270)
        rhythm_label.place(x=110, y=340)
        rhythm_score.place(x=665, y=340)
        articulation_label.place(x=110, y=410)
        articulation_score.place(x=815, y=410)
        dynamics_label.place(x=110, y=480)
        dynamics_score.place(x=695, y=480)
        melody_label.place(x=110, y=550)
        melody_score.place(x=665, y=550)


class ErrorAnalysis(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        back_pic = Image.open("Pictures/back.png")
        back_img = ImageTk.PhotoImage(back_pic)
        back_label = tk.Label(self, image=back_img, borderwidth=0, cursor="hand2")
        back_label.bind("<Button-1>", DisplayAfterPerf)
        back_label.image = back_img

        img = Image.open("Pictures/ErrorAnalysis.png")
        errAnal_title_img = ImageTk.PhotoImage(img)
        errAnal_title_label = tk.Label(self, image=errAnal_title_img, borderwidth=0)
        errAnal_title_label.image = errAnal_title_img

        main_frame = tk.Frame(self, width=988, height=563, bg="#2A2B2C", border=0)
        main_frame.pack_propagate(False)
    
        global show_data
        def show_data():
            for widget in main_frame.winfo_children():
                widget.destroy()

            v = visualization.Visual()
            song = search_entry.get() + '.csv'
            print ("DATA HAS BEEN SHOWNED")
            v.read_csv(song)

            ax, fig = v.plot_rect()

            kino = FigureCanvasTkAgg(fig, main_frame)
            kino.get_tk_widget().pack(side=LEFT, anchor=W)

            ax.set_xlabel('Time(s)')
            ax.set_ylabel('Notes')
            ax.set_facecolor('#2A2B2C')
            fig.set_facecolor('#2A2B2C')

            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['right'].set_color('white')

            '''
                fig = Figure(figsize=(5,5),dpi=100)
                subplot = fig.add_subplot(111)
                subplot.bar(x,y,color=['#F7BF50','#ED695E'])

                subplot.xaxis.label.set_color("white")
                subplot.tick_params(axis='x', colors='white') 
                subplot.tick_params(axis='y', colors='#2A2B2C') 
                subplot.spines['left'].set_color('#2A2B2C') 
                subplot.spines['top'].set_color('#2A2B2C') 
                subplot.spines['bottom'].set_color('#2A2B2C') 
                subplot.spines['right'].set_color('#2A2B2C')
                subplot.set_facecolor('#2A2B2C')
                fig.set_facecolor('#2A2B2C')

                for i in range(len(y)):
                    subplot.annotate(str(y[i]), xy=(x[i],y[i]), ha='center', va='bottom',color="white")

                #subplot.axis('off')
                barL = FigureCanvasTkAgg(fig, LeftHand_Frame)
                barL.get_tk_widget().pack(side=LEFT,anchor=W,padx=(0,150))
            '''

            main_frame.place(x=105, y=124)
            back_label.place(x=57, y=36)
            errAnal_title_label.place(x=930, y=45)


class PerformanceReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        
        
        def ReadCSVtoVariable(category):
            song = search_entry.get() + '.csv'
            d = get_data.Data()
            d.modifycsv(song)
            d.read_csv(song)
            d.Data_to_csv(song)
            path = r'../csv/Result_' + song
            try:
                df = pd.read_csv(path, on_bad_lines='skip')
            except FileNotFoundError:
                print('File doesnt exist!')
            data = df.loc[df["Element"] == category, "Data"].iloc[0]
            return data

        
        #global DisplayNote
        def DisplayNote(event):

            notes_label.config(height=70, bg="#2A2B2C", cursor="")
            notes_frame.config(height=70, bg="#2A2B2C", cursor="")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            try:
                #place_forget

                rhythmData_frame.destroy()
                articulationData_frame.destroy()
                dynamicsData_frame.destroy()
                melodyData_frame.destroy()
                fingerData_frame.destroy()

                '''
                for widgets in rhythmData_frame.winfo_children():
                    widgets.destroy()
                
                for widgets in articulationData_frame.winfo_children():
                    widgets.destroy()

                for widgets in dynamicsData_frame.winfo_children():
                    widgets.destroy()

                for widgets in melodyData_frame.winfo_children():
                    widgets.destroy()

                for widgets in fingerData_frame.winfo_children():
                    widgets.destroy()'''

               
                

                

                
            except NameError:
                print("okay lang")
               
            correct_hits = int(ReadCSVtoVariable("Correct"))
            partial_hits = int(ReadCSVtoVariable("Partial"))
            extra_hits = int(ReadCSVtoVariable("Extra"))
            missed_hits = int(ReadCSVtoVariable("Missed"))
            total_expected_hits = correct_hits + partial_hits + extra_hits + missed_hits

            global notesData_frame
            notesData_frame = tk.Frame(self, width=734, height=414, bg="#2A2B2C")
            notesData_frame.place(x=313, y=191)

            #   CORRECT HITS
            correctHits_frame = tk.Frame(notesData_frame, bg="#2A2B2C")
            correctHits_frame.pack(side=TOP, anchor=NW, pady=15)

            correctHits_label = tk.Label(correctHits_frame, text="Perfect Hits:", fg="#F7BF50", bg="#2A2B2C",
                                         font=controller.song_font_after)
            correctHits_label.pack(side=TOP)

            correct_bar = correct_hits / total_expected_hits
            correctHits_bar = tk.LabelFrame(correctHits_frame, text=total_expected_hits, bg="#3a3a3c", fg="#F7BF50",
                                            border=0, width=654, height=16, labelanchor=E, font=controller.title_font)
            correctHits_bar.pack(side=RIGHT, pady=5)

            correct_bar2 = correct_bar * 654

            global correctHits_bar2
            correctHits_bar2 = tk.LabelFrame(self, text=correct_hits, bg="#F7BF50", fg="#2A2B2C", border=0,
                                             width=correct_bar2, height=16, labelanchor=E, font=controller.title_font)
            correctHits_bar2.place(x=313, y=237)
            #######################################

            #   PARTIAL HITS

            partialHits_frame = tk.Frame(notesData_frame, bg="#2A2B2C")
            partialHits_frame.pack(side=TOP, pady=15)

            partialHits_label = tk.Label(partialHits_frame, text="Correct Played Notes:", fg="#F7BF50", bg="#2A2B2C",
                                         font=controller.song_font_after)
            partialHits_label.pack(side=TOP)

            partial_bar = partial_hits / total_expected_hits
            partialHits_bar = tk.LabelFrame(partialHits_frame, text=total_expected_hits, bg="#3a3a3c", fg="#F7BF50",
                                            border=0, width=654, height=16, labelanchor=E, font=controller.title_font)
            partialHits_bar.pack(side=TOP, pady=5)

            global partialHits_bar2
            partial_bar2 = partial_bar * 654
            partialHits_bar2 = tk.LabelFrame(self, text=partial_hits, bg="#F7BF50", fg="#2A2B2C", border=0,
                                             width=partial_bar2, height=16, labelanchor=E, font=controller.title_font)
            partialHits_bar2.place(x=313, y=320)
            ####################################

            #   EXTRA HITS

            extraHits_frame = tk.Frame(notesData_frame, bg="#2A2B2C")
            extraHits_frame.pack(side=TOP, pady=15)

            extraHits_label = tk.Label(extraHits_frame, text="Extra Hits:", fg="#F7BF50", bg="#2A2B2C",
                                       font=controller.song_font_after)
            extraHits_label.pack(side=TOP)

            extra_bar = extra_hits / total_expected_hits
            extraHits_bar = tk.LabelFrame(extraHits_frame, text=total_expected_hits, bg="#3a3a3c", fg="#F7BF50",
                                          border=0, width=654, height=16, labelanchor=E, font=controller.title_font)
            extraHits_bar.pack(side=TOP, pady=5)

            global extraHits_bar2
            extra_bar2 = extra_bar * 654
            extraHits_bar2 = tk.LabelFrame(self, text=extra_hits, bg="#F7BF50", fg="#2A2B2C", border=0,
                                           width=extra_bar2, height=16, labelanchor=E, font=controller.title_font)
            extraHits_bar2.place(x=313, y=403)
            #####################################

            #   MISSED HITS

            missedHits_frame = tk.Frame(notesData_frame, bg="#2A2B2C")
            missedHits_frame.pack(side=TOP, pady=15)

            missedHits_label = tk.Label(missedHits_frame, text="Missed Hits:", fg="#F7BF50", bg="#2A2B2C",
                                        font=controller.song_font_after)
            missedHits_label.pack(side=TOP)

            missed_bar = missed_hits / total_expected_hits
            missedHits_bar = tk.LabelFrame(missedHits_frame, text=total_expected_hits, bg="#3a3a3c", fg="#F7BF50",
                                           border=0, width=654, height=16, labelanchor=E, font=controller.title_font)
            missedHits_bar.pack(side=TOP, pady=5)

            global missedHits_bar2
            missed_bar2 = missed_bar * 654
            missedHits_bar2 = tk.LabelFrame(self, text=missed_hits, bg="#F7BF50", fg="#2A2B2C", border=0,
                                            width=missed_bar2, height=16, labelanchor=E, font=controller.title_font)
            missedHits_bar2.place(x=313, y=487)

            
        #global DisplayRhythm
        def DisplayRhythm(event):

            success_switch = int(ReadCSVtoVariable("Success_Switch"))
            failed_switch = int(ReadCSVtoVariable("Failed_Switch"))

            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=70, bg="#2A2B2C", cursor="")
            rhythm_frame.config(height=70, bg="#2A2B2C", cursor="")

            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()
                articulationData_frame.destroy()

                dynamicsData_frame.destroy()
                melodyData_frame.destroy()
                fingerData_frame.destroy()
                
            except NameError:
                print("okay lang")

            global rhythmData_frame
            rhythmData_frame = tk.Frame(self, width=655, height=89, bg="#2A2B2C")
            rhythmData_frame.place(x=312, y=280)
            rhythmData_frame.pack_propagate(False)

            switches_frame = tk.Frame(rhythmData_frame, bg="#2A2B2C", width=655, height=26)
            switches_frame.pack(side=TOP)
            switches_frame.pack_propagate(0)

            succesSwitch_label = tk.Label(switches_frame, text="Successful Switch", fg="#F7BF50", bg="#2A2B2C",
                                          font=controller.song_font_after)
            succesSwitch_label.pack(side=LEFT, anchor=NW)

            failedSwitch_label = tk.Label(switches_frame, text="Failed", fg="#EB483F", bg="#2A2B2C",
                                          font=controller.song_font_after)
            failedSwitch_label.pack(side=RIGHT, anchor=NE)

            total = success_switch / (success_switch + failed_switch) * 655
            success_bar = tk.LabelFrame(rhythmData_frame, text=success_switch, bg="#F7BF50", fg="#2A2B2C", border=0,
                                        width=total, height=16, labelanchor=E, font=controller.title_font)
            success_bar.pack(pady=5, side=LEFT)

            failed_bar = tk.LabelFrame(rhythmData_frame, text=failed_switch, bg="#3a3a3c", fg="#EB483F", border=0,
                                       width=655, height=16, labelanchor=E, font=controller.title_font)
            failed_bar.pack(pady=5, side=RIGHT)
            
        #global DisplayArticulation
        def DisplayArticulation(event):

            artic_label.config(height=70, bg="#2A2B2C", cursor="")
            artic_frame.config(height=70, bg="#2A2B2C", cursor="")
            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()

                rhythmData_frame.destroy()
                dynamicsData_frame.destroy()
                melodyData_frame.destroy()
                fingerData_frame.destroy()
            except NameError:
                print("okay lang")

            ontime_hits = int(ReadCSVtoVariable("Timed_Hit"))
            late_hits = int(ReadCSVtoVariable("Late_Hit"))
            early_hits = int(ReadCSVtoVariable("Early_Hit"))

            def autopct_format(values):
                def my_format(pct):
                    total = sum(values)
                    val = int(round(pct * total / 100.0))
                    return '{:.1f}%\n({v:d})'.format(pct, v=val)

                return my_format

            global articulationData_frame
            articulationData_frame = tk.Frame(self, width=713, height=425, bg="#2A2B2C")
            articulationData_frame.place(x=312, y=180)
            articulationData_frame.pack_propagate(False)

            hits = [ontime_hits, late_hits, early_hits]
            legend = ['On-Time Hits', 'Late Hits', 'Early Hits']
            colors = ['#4F6272', '#B7C3F3', '#DD7596', '#8EB897']

            fig = Figure(figsize=(5, 5), dpi=100)
            subplot = fig.add_subplot(111)
            subplot.pie(hits, labels=legend, autopct=autopct_format(hits), labeldistance=1.15,
                        textprops={'color': "white"}, wedgeprops={'linewidth': 1, 'edgecolor': 'white'}, colors=colors)
            fig.set_facecolor('#2A2B2C')
            pie2 = FigureCanvasTkAgg(fig, articulationData_frame)
            pie2.get_tk_widget().pack(side=TOP, anchor=CENTER)

            
        #global DisplayDynamics
        def DisplayDynamics(event):

            dynamics_label.config(height=70, bg="#2A2B2C", cursor="")
            dynamics_frame.config(height=70, bg="#2A2B2C", cursor="")

            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()

                rhythmData_frame.destroy()
                articulationData_frame.destroy()
                melodyData_frame.destroy()
                fingerData_frame.destroy()
            except NameError:
                print("okay lang")

            loud_hits = int(ReadCSVtoVariable("Truth_Dynamics"))
            expected_loud_hits = 60
            soft_hits = int(ReadCSVtoVariable("User_Dynamics"))
            expected_soft_hits = 40

            global dynamicsData_frame
            dynamicsData_frame = tk.Frame(self, width=713, height=425, bg="#2A2B2C")
            dynamicsData_frame.place(x=312, y=180)
            dynamicsData_frame.pack_propagate(False)

            LoudHits_frame = tk.Frame(dynamicsData_frame, bg="#2A2B2C", width=713, height=26)
            LoudHits_frame.pack(side=TOP)
            LoudHits_frame.pack_propagate(0)

            LoudHits_label = tk.Label(LoudHits_frame, text="Loud Hits", fg="#F7BF50", bg="#2A2B2C",
                                      font=controller.song_font_after)
            LoudHits_label.pack(side=LEFT)

            to = loud_hits / (loud_hits + expected_loud_hits)
            actual_loud_bar = to * 713
            actualLoud_bar = tk.LabelFrame(dynamicsData_frame, text="Actual:     " + str(loud_hits), bg="#F7BF50",
                                           fg="#2A2B2C", border=0, width=actual_loud_bar, height=24, labelanchor=E,
                                           font=controller.title_font)
            actualLoud_bar.pack(pady=10, side=TOP, anchor=NW)

            to = expected_loud_hits / (loud_hits + expected_loud_hits)
            expected_loud_bar = to * 713
            expectedLoud_bar = tk.LabelFrame(dynamicsData_frame, text="Expected:     " + str(expected_loud_hits),
                                             bg="#A5A5A5", fg="black", border=0, width=expected_loud_bar, height=24,
                                             labelanchor=E, font=controller.title_font)
            expectedLoud_bar.pack(side=TOP, anchor=NW)

            SoftHits_frame = tk.Frame(dynamicsData_frame, bg="#2A2B2C", width=713, height=26)
            SoftHits_frame.pack(pady=(70, 0), side=TOP)
            SoftHits_frame.pack_propagate(0)

            SoftHits_label = tk.Label(SoftHits_frame, text="Soft Hits", fg="#F7BF50", bg="#2A2B2C",
                                      font=controller.song_font_after)
            SoftHits_label.pack(side=LEFT)

            to = soft_hits / (soft_hits + expected_soft_hits)
            actual_soft_bar = to * 713
            actualSoft_bar = tk.LabelFrame(dynamicsData_frame, text="Actual:     " + str(soft_hits), bg="#F7BF50",
                                           fg="#2A2B2C", border=0, width=actual_soft_bar, height=24, labelanchor=E,
                                           font=controller.title_font)
            actualSoft_bar.pack(pady=10, side=TOP, anchor=NW)

            to = expected_soft_hits / (soft_hits + expected_soft_hits)
            expected_soft_bar = to * 713
            expectedSoft_bar = tk.LabelFrame(dynamicsData_frame, text="Expected:     " + str(expected_soft_hits),
                                             bg="#A5A5A5", fg="black", border=0, width=expected_soft_bar, height=24,
                                             labelanchor=E, font=controller.title_font)
            expectedSoft_bar.pack(side=TOP, anchor=NW)

            
        #global DisplayMelody
        def DisplayMelody(event):
            melody_label.config(height=70, bg="#2A2B2C", cursor="")
            melody_frame.config(height=70, bg="#2A2B2C", cursor="")

            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()

                rhythmData_frame.destroy()
                articulationData_frame.destroy()
                dynamicsData_frame.destroy()
                fingerData_frame.destroy()
            except NameError:
                print("okay lang")

            melodyRate = int(ReadCSVtoVariable("Melody"))

            global melodyData_frame
            melodyData_frame = tk.Frame(self, width=713, height=425, bg="#2A2B2C")
            melodyData_frame.place(x=312, y=180)
            melodyData_frame.pack_propagate(False)

            MelodyRate_frame = tk.Frame(melodyData_frame, bg="#2A2B2C", width=713, height=26)
            MelodyRate_frame.pack(side=TOP)
            MelodyRate_frame.pack_propagate(0)

            MelodyRate_label = tk.Label(MelodyRate_frame, text="Melody Rate:", fg="#F7BF50", bg="#2A2B2C",
                                        font=controller.song_font_after)
            MelodyRate_label.pack(side=LEFT)

            MelodyRate_bar2 = tk.LabelFrame(melodyData_frame, bg="#3a3a3c", fg="#2A2B2C", border=0, width=713,
                                            height=24, labelanchor=E, font=controller.title_font)
            MelodyRate_bar2.place(y=36)

            melodyrate_bar = melodyRate * 0.01 * 713
            MelodyRate_bar = tk.LabelFrame(melodyData_frame, text=str(melodyRate) + "%", bg="#F7BF50", fg="#2A2B2C",
                                           border=0, width=melodyrate_bar, height=24, labelanchor=E,
                                           font=controller.title_font)
            MelodyRate_bar.pack(pady=(10, 0), side=TOP, anchor=NW)

            
        #global DisplayFinger
        def DisplayFinger(event):
            finger_label.config(height=70, bg="#2A2B2C", cursor="")
            finger_frame.config(height=70, bg="#2A2B2C", cursor="")

            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()

                rhythmData_frame.destroy()
                articulationData_frame.destroy()
                dynamicsData_frame.destroy()
                melodyData_frame.destroy()
            except NameError:
                print("okay lang")

            correct_left = int(ReadCSVtoVariable("LH_Correct"))
            incorrect_left = int(ReadCSVtoVariable("LH_Fail"))

            correct_right = int(ReadCSVtoVariable("RH_Correct"))
            incorrect_right = int(ReadCSVtoVariable("RH_Fail"))

            global fingerData_frame
            fingerData_frame = tk.Frame(self, width=713, height=425, bg="#2A2B2C")
            fingerData_frame.place(x=312, y=180)
            fingerData_frame.pack_propagate(False)

            LeftHand_Frame = tk.Frame(fingerData_frame, bg="#2A2B2C", width=356, height=425)
            LeftHand_Frame.pack_propagate(False)
            LeftHand_Frame.pack(side=LEFT)

            LeftHand_label = tk.Label(LeftHand_Frame, text="Left Hand", fg="#F7BF50", bg="#2A2B2C",
                                      font=controller.song_font_after)
            LeftHand_label.pack(side=TOP, anchor=NW)

            RightHand_Frame = tk.Frame(fingerData_frame, bg="#2A2B2C", width=356, height=425)
            RightHand_Frame.pack_propagate(False)
            RightHand_Frame.pack(side=RIGHT)

            RightHand_label = tk.Label(RightHand_Frame, text="Right Hand", fg="#F7BF50", bg="#2A2B2C",
                                       font=controller.song_font_after)
            RightHand_label.pack(side=TOP, anchor=NE)

            x = ['Correct\nHits', 'Incorrect\nHits']
            y = [correct_left, incorrect_left]

            fig = Figure(figsize=(5, 5), dpi=100)
            subplot = fig.add_subplot(111)
            subplot.bar(x, y, color=['#F7BF50', '#ED695E'])

            subplot.xaxis.label.set_color("white")
            subplot.tick_params(axis='x', colors='white')
            subplot.tick_params(axis='y', colors='#2A2B2C')
            subplot.spines['left'].set_color('#2A2B2C')
            subplot.spines['top'].set_color('#2A2B2C')
            subplot.spines['bottom'].set_color('#2A2B2C')
            subplot.spines['right'].set_color('#2A2B2C')
            subplot.set_facecolor('#2A2B2C')
            fig.set_facecolor('#2A2B2C')

            for i in range(len(y)):
                subplot.annotate(str(y[i]), xy=(x[i], y[i]), ha='center', va='bottom', color="white")

            # subplot.axis('off')
            barL = FigureCanvasTkAgg(fig, LeftHand_Frame)
            barL.get_tk_widget().pack(side=LEFT, anchor=W, padx=(0, 150))

            ######################## RIGHT HAND ##############
            x = ['Incorrect\nHits', 'Correct\nHits']
            y = [incorrect_right, correct_right]
            fig = Figure(figsize=(5, 5), dpi=100)
            subplot = fig.add_subplot(111)
            subplot.bar(x, y, color=['#ED695E', '#F7BF50'])

            subplot.xaxis.label.set_color("white")
            subplot.tick_params(axis='x', colors='white')
            subplot.tick_params(axis='y', colors='#2A2B2C')
            subplot.spines['left'].set_color('#2A2B2C')
            subplot.spines['top'].set_color('#2A2B2C')
            subplot.spines['bottom'].set_color('#2A2B2C')
            subplot.spines['right'].set_color('#2A2B2C')
            subplot.set_facecolor('#2A2B2C')
            fig.set_facecolor('#2A2B2C')

            for i in range(len(y)):
                subplot.annotate(str(y[i]), xy=(x[i], y[i]), ha='center', va='bottom', color="white")

            # subplot.axis('off')
            barR = FigureCanvasTkAgg(fig, RightHand_Frame)
            barR.get_tk_widget().pack(side=RIGHT, anchor=E, padx=(150, 0))

            

        # notesData_frame = tk.Frame(self)
        # rhythmData_frame = tk.Frame(self)
        #global ClearData
        global lastna
        def lastna():
            #Initialize()
            ClearData()
            print("eme")

        back_pic = Image.open("Pictures/back.png")
        back_img = ImageTk.PhotoImage(back_pic)
        back_label = tk.Label(self, image=back_img, borderwidth=0, cursor="hand2")
        back_label.bind("<Button-1>", DisplayAfterPerf)
        back_label.image = back_img

        img = Image.open("Pictures/PerfReport.png")
        perfTitle_img = ImageTk.PhotoImage(img)
        perfTitle_label = tk.Label(self, image=perfTitle_img, borderwidth=0)
        perfTitle_label.image = perfTitle_img

        main_frame = tk.Frame(self, width=988, height=563, bg="#2A2B2C", border=0)
        main_frame.place(x=105, y=124)
        back_label.place(x=57, y=36)
        perfTitle_label.place(x=840, y=49)

        global dash_frame
        dash_frame = tk.Frame(self, width=139, height=563, bg="#3A3A3C", border=0)
        dash_frame.pack_propagate(0)

        notes_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0)
        notes_label = tk.Label(notes_frame, width=139, height=51, text="Notes", fg="#F7BF50", bg="#3A3A3C",
                                cursor="hand2", font=controller.Mont_bold20)
        notes_frame.pack_propagate(0)
        notes_label.bind("<Button-1>", DisplayNote)
            # notes_label.pack_propagate(0)

        rhythm_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0, cursor="hand2")
        rhythm_label = tk.Label(rhythm_frame, width=139, height=51, text="Rhythm", fg="#F7BF50", bg="#3a3a3c",
                                    font=controller.Mont_bold20)
        rhythm_frame.pack_propagate(0)
        rhythm_label.bind("<Button-1>", DisplayRhythm)

        artic_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0, cursor="hand2")
        artic_label = tk.Label(artic_frame, width=139, height=51, text="Articulation", fg="#F7BF50", bg="#3a3a3c",
                                font=controller.Mont_bold20)
        artic_frame.pack_propagate(0)
        artic_label.bind("<Button-1>", DisplayArticulation)

        dynamics_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0, cursor='hand2')
        dynamics_label = tk.Label(dynamics_frame, width=139, height=51, text="Dynamics", fg="#F7BF50", bg="#3a3a3c",
                                    font=controller.Mont_bold20)
        dynamics_frame.pack_propagate(0)
        dynamics_label.bind("<Button-1>", DisplayDynamics)

        melody_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0, cursor='hand2')
        melody_label = tk.Label(melody_frame, width=139, height=51, text="Melody", fg="#F7BF50", bg="#3a3a3c",
                            font=controller.Mont_bold20)
        melody_frame.pack_propagate(0)
        melody_label.bind("<Button-1>", DisplayMelody)

        finger_frame = tk.Frame(dash_frame, width=139, height=51, bg="#3A3A3C", border=0, cursor="hand2")
        finger_label = tk.Label(finger_frame, width=139, height=51, text="Finger\nPattern", fg="#F7BF50", bg="#3a3a3c",
                                    font=controller.Mont_bold20)
        finger_frame.pack_propagate(0)
        finger_label.bind("<Button-1>", DisplayFinger)

        #####################################

            

        dash_frame.place(x=105, y=124)

        notes_frame.pack(anchor=CENTER, pady=35)
        notes_label.pack(anchor=CENTER)

        rhythm_frame.pack(anchor=CENTER, pady=0)
        rhythm_label.pack(anchor=CENTER)

        artic_frame.pack(anchor=CENTER, pady=35)
        artic_label.pack(anchor=CENTER)

        dynamics_frame.pack(anchor=CENTER, pady=0)
        dynamics_label.pack(anchor=CENTER)

        melody_frame.pack(anchor=CENTER, pady=35)
        melody_label.pack(anchor=CENTER)

        finger_frame.pack(anchor=CENTER, pady=0)
        finger_label.pack(anchor=CENTER)
        
        
        
        
        

        
            
            

        def ClearData():

            #for widgets in dash_frame.winfo_children():
            #        widgets.destroy()
            #dash_frame.destroy()
            
            finger_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            finger_frame.config(height=51, bg="#3A3A3C", cursor="hand2")

            notes_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            notes_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            rhythm_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            artic_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            dynamics_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_label.config(height=51, bg="#3A3A3C", cursor="hand2")
            melody_frame.config(height=51, bg="#3A3A3C", cursor="hand2")
            
            try:
                notesData_frame.destroy()
                correctHits_bar2.destroy()
                partialHits_bar2.destroy()
                extraHits_bar2.destroy()
                missedHits_bar2.destroy()
                
                fingerData_frame.destroy()
                rhythmData_frame.destroy()
                articulationData_frame.destroy()
                dynamicsData_frame.destroy()
                melodyData_frame.destroy()
            except NameError:
                print("okay lang")
       

            



class Statistics(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        global getSkillLevel
        def getSkillLevel(Score):
            if (Score >= 0 and Score <= 25):
                avglevel = "Beginner"
            elif(Score >= 26 and Score <= 50):
                avglevel = "Amateur"
            elif(Score >= 51 and Score <= 75):
                avglevel = "Proficient"
            elif(Score >= 76 and Score <= 100):
                avglevel = "Expert"
            else:
                avglevel = "Cant determine"
            
            return avglevel

        global ScoreToRating
        def ScoreToRating(score):
            if (score >= 0 and score <= 25):
                levelStats = "Worst Performance"

            elif(score >= 26 and score <= 50):
                levelStats = "Poor Performance"

            elif(score >= 51 and score <= 75):
                levelStats = "Good Performance"
                
            elif(score >= 76 and score <= 100):
                levelStats = "Excellent Performance"

            else:
                levelStats = "Cant determine"

            return levelStats
            

        def GetSongTrack(e):
            for widget in frame_Graph.winfo_children():
                widget.destroy()

            song_track = listbox_stat.get(ANCHOR)

            GraphTest.chosen_song = song_track
            GraphTest.user = label_entry.get()

            ax,fig = GraphTest.DisplayGraph()

            graph = FigureCanvasTkAgg(fig, frame_Graph)
            graph.get_tk_widget().pack(side=LEFT, anchor=W)

            
            ax.set_facecolor('#2A2B2C')
            fig.set_facecolor('#2A2B2C')

            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['right'].set_color('white')


        global UpdateValues
        def UpdateValues():

            for widget in frame_Graph.winfo_children():
                widget.destroy()

            listbox_stat.delete(0, END)

            score_label_stat.configure(text="")
            rating_label_stat.configure(text="")
            skillLevel_label_stat.configure(text="")

            con = sqlite3.connect('userData.db')
            cu = con.cursor()
         
            cu.execute("SELECT avg(Score) FROM History WHERE Username = ? LIMIT 1", (uname,))

            AvgScore = cu.fetchone()[0]
            print(AvgScore)
            if AvgScore == None:
                AvgScore=int(0)
                rating = None
                skill_Level = None
            else:

                rating = ScoreToRating(AvgScore)
                rating = rating.replace(" ","")
            #print("Rating: ",rating)
                rating = rating.replace("Performance","")
                skill_Level = getSkillLevel(AvgScore)
            
            score_label_stat.configure(text=str("%.2f" % AvgScore),anchor=CENTER)
            rating_label_stat.configure(text=rating,anchor=CENTER)
            skillLevel_label_stat.configure(text=skill_Level,anchor=CENTER)

            cu.execute("SELECT Title FROM History WHERE Username = ? GROUP BY Title ORDER BY count(*) DESC", (uname,))
            ListSongs = cu.fetchall()

            if len(ListSongs) > 0:
                listbox_stat.delete(0, END)

                for song in ListSongs:
                    listbox_stat.insert(END, song[0])
            
            '''
            cu.execute("SELECT Title FROM History WHERE Username = ? AND Score = (SELECT MAX(Score) FROM History) LIMIT 1", (label_entry.get(),))
            TopSong = cu.fetchone()[0]
            print(TopSong)
            topsong.configure(text=str(TopSong),anchor=CENTER)
            '''

            con.commit()
            con.close()

            # if (AvgScore >= 0 and AvgScore <= 25):
            #     avglevel = "Worst Performance"
            # elif(AvgScore >= 26 and AvgScore <= 50):
            #     avglevel = "Poor Performance"
            # elif(AvgScore >= 51 and AvgScore <= 75):
            #     avglevel = "Good Performance"
            # elif(AvgScore >= 76 and AvgScore <= 100):
            #     avglevel = "Excellent Performance"
            # else:
            #     avglevel = "Cant determine"

            # AvgRating_label.configure(text=str(avglevel),anchor=CENTER)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((250, 55), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img, borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", ShowStartPage)
        logo_label.image = logo_img

        img6 = Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img6)
        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        frame_stat = tk.Frame(self, width=979, height=509, bg="#2A2B2C", border=0)

        img = Image.open("Pictures/CurrSkill.png")
        CurrSkill_img = ImageTk.PhotoImage(img)
        CurrSkill_label = tk.Label(self, image=CurrSkill_img, borderwidth=0)
        CurrSkill_label.image = CurrSkill_img

        skillLevel_label_stat = tk.Label(self,width=23,height=1, bg="#F8BA43",borderwidth=0,font=controller.Mont_bold20)
        

        img = Image.open("Pictures/AvgRating.png")
        AvgRating_img = ImageTk.PhotoImage(img)
        AvgRating_label = tk.Label(self, image=AvgRating_img, borderwidth=0)
        AvgRating_label.image = AvgRating_img

        rating_label_stat = tk.Label(self,width=10,height=1, bg="#F8BA43",borderwidth=0,font=controller.Mont_bold20)
        
        img = Image.open("Pictures/AvgScore.png")
        AvgScore_img = ImageTk.PhotoImage(img)
        AvgScore_label = tk.Label(self, image=AvgScore_img, borderwidth=0)
        AvgScore_label.image = AvgScore_img

        score_label_stat = tk.Label(self,width=6,height=1, bg="#F8BA43",borderwidth=0,font=controller.Mont_bold20)
       
        img = Image.open("Pictures/TrackTitle.png")
        Track_img = ImageTk.PhotoImage(img)
        Track_label = tk.Label(self, image=Track_img, borderwidth=0)
        Track_label.image = Track_img

        frame_list = tk.Frame(self, width=226, height=306, border=0, bg="#2A2B2C")
        frame_list.place(x=619, y=471)

        listbox_stat = tk.Listbox(frame_list, width=37, height=7, fg="#FFFFFF", bg="#2A2B2C", borderwidth=0,
                             font=controller.font_song)
        scrollbar = tk.Scrollbar(frame_list, orient=VERTICAL)
        listbox_stat.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=listbox_stat.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox_stat.pack(pady=1)

        listbox_stat.bind("<<ListboxSelect>>", GetSongTrack)

        frame_Graph = tk.Frame(self, width=459, height=459, border=0, bg="#2A2B2C")
        frame_Graph.place(x=138, y=143)
        frame_Graph.pack_propagate(0)



        logo_label.place(x=35, y=34)
        info_label.place(x=728, y=57)
        
        frame_stat.place(x=113,y=143)
        CurrSkill_label.place(x=619,y=168)
        AvgRating_label.place(x=813,y=289)
        AvgScore_label.place(x=619,y=289)
        
        Track_label.place(x=619,y=410)

        score_label_stat.place(x=698,y=332)
        rating_label_stat.place(x=912,y=332)
        skillLevel_label_stat.place(x=720,y=214)




# History

class History(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller
        # label = tk.Label(self, text="Statistics",bg="#F7BF50", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Home",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic = logo_pic.resize((250, 55), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img, borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", ShowStartPage)
        logo_label.image = logo_img

        img6 = Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img6)
        info_label = tk.Label(self, image=info_img, borderwidth=0)
        info_label.image = info_img

        frame_histo = tk.Frame(self, width=988, height=545, bg="#2A2B2C", border=0)
        frame_histoList = tk.Frame(self, width=880, height=400, bg="#2A2B2C", border=0)
        frame_histoList.pack_propagate(0)

        image = Image.open("Pictures/menuHisto.png")
        image = image.resize((950, 100), Image.Resampling.LANCZOS)
        imgMenu = ImageTk.PhotoImage(image)

        labelhisto_menu = tk.Label(self, image=imgMenu, border=0)
        labelhisto_menu.image = imgMenu

        # global listbox_songs2
        # listbox_songs2 = tk.Listbox(frame_histoList,width=80,height=20,fg="#FFFFFF",bg="#2A2B2C",borderwidth=0,font=controller.font_song)
        # scrollbar2 = tk.Scrollbar(frame_histoList,orient=VERTICAL)
        # listbox_songs2.config(yscrollcommand=scrollbar2.set)
        # #listbox.pack(side="top", fill="both", expand=True)
        # scrollbar2.config(command=listbox_songs2.yview)
        # scrollbar2.pack(side=RIGHT,fill=Y)
        # #scrollbar.place(x=365,y=259)
        # listbox_songs2.pack(pady=1)

        # listbox_songs2.bind("<<ListboxSelect>>", infos)

        global tree_histo
        ttk.Style().theme_use('clam')
        ttk.Style().configure("Treeview", background="#2A2B2", foreground="white", fieldbackground="#2A2B2C")
        tree_histo = ttk.Treeview(frame_histoList, column=("c1", "c2", "c3"), show="headings", height=293)

        tree_histo["columns"] = ("date&time", "title", "score")
        tree_histo.column("date&time", width=293, stretch=NO, anchor=CENTER)
        tree_histo.column("title", width=293, stretch=NO, anchor=CENTER)
        tree_histo.column("score", width=293, stretch=NO, anchor=CENTER)

        scrollbar2 = tk.Scrollbar(frame_histoList, orient=VERTICAL)
        tree_histo.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=tree_histo.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)

        global UpdateHistory

        def UpdateHistory():

            for item in tree_histo.get_children():
                tree_histo.delete(item)

            con = sqlite3.connect('userData.db')
            cu = con.cursor()

            cu.execute("SELECT * FROM History WHERE Username = ? ORDER BY datetime(DateAndTime) DESC", (label_entry.get(),))
            
            historyData = cu.fetchall()

            for histo in historyData:
            
                tree_histo.insert("", 'end', values=(histo[1], histo[2], histo[3]))
            

            cu.execute("SELECT * FROM History WHERE Username = ?", (label_entry.get(),))
            
            count = []
            i = len(count)
            historyData = cu.fetchall()

            for histo in historyData:
              
                count.append(tree_histo.insert("", 'end', values=(histo[1], histo[2], histo[3])))
                tree_histo.see(count[-1])
           
            con.commit()
            con.close()

            print("FLAGG")

        tree_histo.bind('<Motion>', 'break')

        #tree_histo.bind('<<TreeviewSelect>>', infos2)

        # scrollbar2 = tk.Scrollbar(frame_histoList,orient=VERTICAL)
        # tree_histo.config(yscrollcommand=scrollbar2.set)
        # scrollbar2.config(command=tree_histo.yview)

        # scrollbar2.pack(side=RIGHT,fill=Y)

        tree_histo.pack(side=LEFT)

        frame_histo.place(x=105, y=124)
        labelhisto_menu.place(x=120, y=128)
        frame_histoList.place(x=150, y=235)
        logo_label.place(x=35, y=34)
        info_label.place(x=728, y=57)




if __name__ == "__main__":
    global app
    app = SampleApp()


    def close_window():
        app.quit()


    app.protocol("WM_DELETE_WINDOW", close_window)

    window_width = 1206
    window_height = 730

    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    app.attributes('-fullscreen', False)
    app.resizable(False, False)
    app.mainloop()