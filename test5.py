import ast
from ast import Load
from cgitb import text
#from ast import *
from logging import root
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import *
from tkinter import messagebox,ttk
from tkinter.ttk import Progressbar
from turtle import bgcolor, circle, color, title, width
from PIL import ImageTk, Image
from collections import deque
import time



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Montserrat', size=16,slant="italic")
        self.score_font = tkfont.Font(family='Montserrat', size=96,weight="bold")
        self.song_font_after = tkfont.Font(family='Montserrat', size=18,weight="bold")
        self.grade_font = tkfont.Font(family='Montserrat', size=24,weight="bold")
        self.Mont_bold20 = tkfont.Font(family='Montserrat', size=20,weight="bold")

        self.title2_font = tkfont.Font(family='Lemon Milk', size=32, weight="bold")
        self.title3_font = tkfont.Font(family='Lemon Milk', size=20, weight="bold")
        self.button_font = tkfont.Font(family='Lemon Milk', size=16, weight="bold")
        self.button2_font = tkfont.Font(family='Lemon Milk Regular Italic', size=16, weight="bold", slant="italic")
        self.body_font = tkfont.Font(family='Lemon Milk', size=16)
        self.font_song = tkfont.Font(family='Montserrat',size=16)
        self.body2_font = tkfont.Font(family='Lemon Milk', size=16, weight="bold")
        self.body3_font = tkfont.Font(family='Lemon Milk', size=12)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoadingPage, LogIn, Register, StartPage, PlayPage, AfterPerformance,PerformanceReport,PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
<<<<<<< HEAD
        self.show_frame("LoadingPage")
        #self.show_frame("StartPage")
=======
<<<<<<< HEAD
        #self.show_frame("LoadingPage")
=======
>>>>>>> 5c351dc399f52e25c858073ba0e4e2fb29fe980d
        # LoadingPage dapat
        # self.show_frame("LoadingPage")
       
        #try lang to
<<<<<<< HEAD
        #self.show_frame("PerformanceReport")
        self.show_frame("StartPage")
=======
        self.show_frame("PerformanceReport")
>>>>>>> parent of 52d8259 (Revert "Merge branch 'GUI' of https://github.com/s1cnarf/Thesis1 into GUI")
        #self.show_frame("StartPage")
        self.show_frame("PerformanceReport")
>>>>>>> 5c351dc399f52e25c858073ba0e4e2fb29fe980d
        

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        #self.controller.state("zoomed")
        #self.update_idletasks()

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((386,82))
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_label = tk.Label(self, image=logo_img,borderwidth=0)
        logo_label.image = logo_img
        logo_label.place(x=400,y=285)

        loading = tk.Frame(self, bg="#281801")
        loading.pack_propagate(False)
        loading.configure(width=10,height=3)
        loading.place(x=410,y=389)
        
        self.after(200)

        def comm():
            
            current = loading['width']
            
            if current == 365:
                self.destroy()
                #controller.show_frame("LogIn")
            
            if current < 365:
                loading.config(width=current+71)
                self.after(500,comm)
        self.after(1000,comm)


class LogIn(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        #self.controller.state("zoomed")

        def login(e):
            uname = label_entry.get()
            passw = label2_entry.get()

            file = open ('registersheet.txt' ,'r')
            d = file.read()
            r = ast.literal_eval(d)
            file.close()

            print(r.keys())
            print(r.values())
            print(r)

            if uname in r.keys() and passw==r[uname]:
                controller.show_frame("StartPage")

            else:
                messagebox.showerror('Invalid', 'Invalid username and password')
        
        frame1 = tk.Frame(self,width=463,height=461,bg="#2A2B2C",border=0)
        label = tk.Label(self, text="USERNAME",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label2 = tk.Label(self, text="PASSWORD",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        #sign_in = tk.Label(self, text="Sign In",fg="#F7BF50", bg="#2A2B2C", font=controller.title_font)

        line = tk.Frame(self, bg="#281801")
        line.configure(width=1,height=595)
        line.place(x=600,y=66)

        def on_enter(e):
            label_entry.delete(0,'end')

        def on_leave(e):
            name=label_entry.get()
            if name == '':
                label_entry.insert(0,'Username')
        
        label_entry = tk.Entry(self,width=29,font=controller.title_font)
        label_entry.insert(0,"Enter your username")
        label_entry.bind('<FocusIn>', on_enter)
        label_entry.bind('<FocusOut>', on_leave)
        label_entry.focus()



        def on_enter(e):
            label2_entry.delete(0,'end')

        def on_leave(e):
            name=label2_entry.get()
            if name == '':
                label2_entry.insert(0,'Password')

        label2_entry = tk.Entry(self,width=29,font=controller.title_font,show="*")
        label2_entry.insert(0,"Enter your password")
        label2_entry.bind('<FocusIn>', on_enter)
        label2_entry.bind('<FocusOut>', on_leave)
        label2_entry.bind('<Return>',login)
        
        

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((386,82),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_pic = Image.open("Pictures/info.png")
        #logo_pic= logo_pic.resize((430,52),Image.ANTIALIAS)
        info_img = ImageTk.PhotoImage(logo_pic)

        names_pic = Image.open("Pictures/names.png")
        names_img = ImageTk.PhotoImage(names_pic)

        logo_label = tk.Label(self, image=logo_img,borderwidth=0)
        logo_label.image = logo_img

        info_label = tk.Label(self, image=info_img,borderwidth=0)
        info_label.image = info_img

        names_label= tk.Label(self, image=names_img,borderwidth=0)
        names_label.image = names_img

        log_in = tk.Label(self, text="Log In",bg="#F7BF50", fg="#2A2B2C", cursor ="hand2", borderwidth=0, width=15, height=1, font=controller.button_font)
        log_in.bind("<Button-1>",login)
        register= tk.Label(self, text="Register",fg="#F7BF50", bg="#2A2B2C", cursor ="hand2", borderwidth=0,font=controller.button2_font)
        register.bind("<Button-1>", lambda e: controller.show_frame("Register"))
        
        frame1.place(x=671,y=143)
        label.place(x=746, y=214)
        label2.place(x=746, y=322)
        #sign_in.place(x=540,y=220)

        label_entry.place(x=746,y=243)
        label2_entry.place(x=746,y=352)

        #logo_label.place(x=35,y=34)
        #info_label.place(x=738, y=57)
        #names_label.place(x=362, y=677)

        logo_label.place(x=123,y=270)
        info_label.place(x=98, y=416)
        names_label.place(x=660, y=660)

        log_in.place(x=810,y=465)
        register.place(x=862, y=510)

class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F7BF50")
        self.controller = controller

        def register(event):
            username = labelReg_entry.get()
            password = label2Reg_entry.get()
            contactNo = label3Reg_entry.get()
            email = label4Reg_entry.get()
            confirmPass = label5Reg_entry.get()

            if password == confirmPass:
                try:
                    file = open('registersheet.txt','r+')
                    d = file.read()
                    r = ast.literal_eval(d)

                    dict2 = {username:password ,contactNo:email}
                    r.update(dict2)
                    file.truncate(0)
                    file.close()

                    file = open('registersheet.txt','w')
                    w = file.write(str(r))

                    messagebox.showinfo('Signup','Sucessfully Sign Up')

                except:
                    file = open('registersheet.txt','w')
                    displayDict = str({'Username':'Password','Contact No.':'Email'})
                    file.write(displayDict)
                    file.close()

            else:
                messagebox.showerror('Invalid',"Both Password Should Match")
    
        frame_reg = tk.Frame(self,width=860,height=480,bg="#2A2B2C",border=0)
        label_reg = tk.Label(self, text="CREATE ACCOUNT",fg="#F7BF50", bg="#2A2B2C", font=controller.body2_font)

        
        labelReg = tk.Label(self, text="USERNAME",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        labelReg_entry = tk.Entry(self,width=29,font=controller.title_font)

        label2Reg = tk.Label(self, text="PASSWORD",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label2Reg_entry = tk.Entry(self,width=29,font=controller.title_font,show="*")

        label3Reg = tk.Label(self, text="CONTACT NO.",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label3Reg_entry = tk.Entry(self,width=29,font=controller.title_font)
        label3Reg_entry.bind("<Return>",register)
        
        label4Reg = tk.Label(self, text="EMAIL",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label4Reg_entry = tk.Entry(self,width=29,font=controller.title_font)

        label5Reg = tk.Label(self, text="CONFIRM PASSWORD",fg="#F7BF50", bg="#2A2B2C", font=controller.body_font)
        label5Reg_entry = tk.Entry(self,width=29,font=controller.title_font,show="*")
        label5Reg_entry.bind("<Return>",register)

        label6Reg = tk.Label(self, text="I already have an account",fg="grey", bg="#2A2B2C", font=controller.body3_font)
        label7Reg = tk.Label(self, text="Sign In", cursor ="hand2", fg="#F7BF50", bg="#2A2B2C", borderwidth=0)
        label7Reg.bind("<Button-1>", lambda e: controller.show_frame("LogIn"))

        reg_button = tk.Label(self, text="REGISTER",bg="#F7BF50", fg="#2A2B2C", cursor ="hand2", borderwidth=0, width=13, height=2 ,font=controller.button_font)
        reg_button.bind("<Button-1>",register)

        #reg_button = Button(self, text="REGISTER",bg="#F7BF50", fg="#2A2B2C", cursor ="hand2", borderwidth=0, width=13, height=2 ,font=controller.button_font)
        #reg_button.bind("<Button-1>",register)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_pic = Image.open("Pictures/info.png")
        #logo_pic= logo_pic.resize((430,52),Image.ANTIALIAS)
        info_img = ImageTk.PhotoImage(logo_pic)

        logo_label = tk.Label(self, image=logo_img,borderwidth=0)
        logo_label.image = logo_img

        info_label = tk.Label(self, image=info_img,borderwidth=0)
        info_label.image = info_img


        frame_reg.place(x=180,y=134)
        label_reg.place(x=510,y=170)
        labelReg.place(x=220,y=220)
        labelReg_entry.place(x=223, y=245)
        label2Reg.place(x=220, y=320)
        label2Reg_entry.place(x=223, y=345)
        label3Reg.place(x=220, y=420)
        label3Reg_entry.place(x=223, y=445)
        label4Reg.place(x=650, y=220)
        label4Reg_entry.place(x=653, y=245)
        label5Reg.place(x=650, y=320)
        label5Reg_entry.place(x=653, y=345)
        reg_button.place(x=700, y=450)
        label6Reg.place(x=675, y=510)
        label7Reg.place(x=830, y=510)

        logo_label.place(x=35,y=34)
        info_label.place(x=738, y=57)
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        self.controller.title("Chop-In")
        #self.controller.state("zoomed")

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((386,82),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)

       
        image = Image.open("Pictures/menu1.png")
        #image = image.resize((40,49), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu2.png")
        #image = image.resize((67,53), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu3.png")
        #image = image.resize((88,53), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu4.png")
        #image = image.resize((69,53), Image.ANTIALIAS)
        img4 = ImageTk.PhotoImage(image)

        logo_label = tk.Label(self, image=logo_img,borderwidth=0)
        logo_label.image = logo_img

        play_label = tk.Label(self,image=img, cursor="hand2", borderwidth=0)
        play_label.bind("<Button-1>", lambda e: controller.show_frame("PlayPage"))
        play_label.image = img

        play_label2 = tk.Label(self, image=img2, cursor ="hand2", borderwidth=0)
        play_label2.bind("<Button-1>", lambda e: controller.show_frame("PageTwo"))
        play_label2.image = img2

        play_label3 = tk.Label(self, image=img3, cursor ="hand2", borderwidth=0)
        play_label3.bind("<Button-1>", lambda e: controller.show_frame("PageThree"))
        play_label3.image = img3

        play_label4 = tk.Label(self, image=img4, cursor ="hand2", borderwidth=0)
        play_label4.bind("<Button-1>", lambda e: controller.show_frame("LogIn"))
        play_label4.image = img4
    
        logo_label.place(x=400,y=200)
        play_label.place(x=364, y=375)
        play_label2.place(x=490, y=375)
        play_label3.place(x=644, y=374)
        play_label4.place(x=792, y=375)


class PlayPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        
        flag=True

        def update(task,flag):
            listbox_songs.delete(0,END)
            
            for item in task:
                
                item = item[:-4]
                if flag:
                    PlayCount_Dictionary[item]=0 # the 0 is the play count
                listbox_songs.insert(END, item)
            flag=False

        def GetSongList(e):
            song = listbox_songs.get(ANCHOR)
            search_entry.delete(0, END)

            search_entry.insert(0,song)

        def GetSongList2(e):
            song2 = listbox.get(ANCHOR)
            
            search_entry.delete(0,END)
            search_entry.insert(0,"")
            search_entry.insert(0,song2)
            return None

        global infos
        def infos(e):
            controller.show_frame("AfterPerformance")

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

            update(task,flag)


        # Create Stack For Recents
        stack = deque()
        stack2 = deque()
        index_stack=0

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
            
            #data = label.cget("text")
            data = search_entry.get()
            stack.append(data)
            stack2.append(data)

            song=stack2.pop()
            listbox_songs2.insert(index_stack,song)
            listbox.insert(index_stack,song)
            index_stack+1
            song_label.configure(text=data)
            #controller.show_frame("AfterPerformance")

        global combinedFunc
        def combinedFunc(e):
            PushSongInStack(e)
            infos(e)

            
        def IncrementPlayCount(event):
            selection = event.widget.curselection()
            
            index = selection[0]
            data = event.widget.get(index)
            listbox3.delete(0,END)
            print("data",data)
            
            



            if data in PlayCount_Dictionary:
                PlayCount_Dictionary[data] = PlayCount_Dictionary.get(data)+1
                print (PlayCount_Dictionary)
                
            for w in sorted(PlayCount_Dictionary, key = PlayCount_Dictionary.get):
                if(PlayCount_Dictionary[w]>0):
                    print("w = "+ w)
                    listbox3.insert(0,w)
                    
                   

        def CombineFunctions(event):
            #PushSongInStack(event)
            #IncrementPlayCount(event)
            fillout(event)
            #callback(event)

        
                        

        
        image = Image.open("Pictures/recents.png")
        #image = image.resize((40,49), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/songs.png")
        #image = image.resize((10,30), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/searchIcon.png")
        #image = image.resize((25,28), Image.ANTIALIAS)
        img4 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/playButton.png")
        #image = image.resize((25,28), Image.ANTIALIAS)
        img5= ImageTk.PhotoImage(image)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img,borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        logo_label.image = logo_img

        img6= Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img6)
        info_label = tk.Label(self, image=info_img,borderwidth=0)
        info_label.image = info_img

        #search_frame = tk.Frame(self,width=259,height=30,bg="#2A2B2C",border=0)
        
        # black rectangle
        frame2_play = tk.Frame(self,width=1028,height=447,bg="#2A2B2C",border=0)
        
        # song label
        label_play = tk.Label(self, image=img2,border=0)
        label_play.image = img2

        frame3 = tk.Frame(self,width=262,height=51,border=0,bg="#2A2B2C")
        frame3.place(x=450,y=190)

        global search_entry
        search_entry = tk.Entry(frame3,width=16,border=0,font=controller.title_font,bg="#ffffff",fg="#000000")
        
        label_search = tk.Label(frame3, image=img4,border=0)
        label_search.image = img4


        label_search.pack(side=LEFT,padx=2)
        search_entry.pack(side=LEFT)

        line = tk.Frame(self,width=1,height=386,border=0,bg="#F8BA43")
        line.place(x=750,y=175)

        play_Button = tk.Label(self, image=img5,border=0,cursor="hand2")
        play_Button.image = img5


        label_recent = tk.Label(self, image=img,border=0)
        label_recent.image = img
               
        frame1 = tk.Frame(self,width=226,height=306,border=0,bg="#2A2B2C")
        frame1.place(x=831,y=256)

        listbox = tk.Listbox(frame1,width=22,height=15,fg="#FFFFFF",bg="#2A2B2C",borderwidth=0,font=controller.font_song)
        scrollbar = tk.Scrollbar(frame1,orient=VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        #listbox.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=RIGHT,fill=Y)
        #scrollbar.place(x=365,y=259)
        listbox.pack(pady=1)

        listbox.bind("<<ListboxSelect>>", GetSongList2)

        #listbox.bind("<<ListboxSelect>>", PushSongInStack)

        frame2 = tk.Frame(self,width=549,height=294,border=0,bg="#2A2B2C")
        frame2.place(x=136,y=256)

        listbox_songs = tk.Listbox(frame2,width=50,height=15,fg="#FFFFFF",bg="#2A2B2C",borderwidth=0,font=controller.font_song)
        scrollbar2 = tk.Scrollbar(frame2,orient=VERTICAL)
        listbox_songs.config(yscrollcommand=scrollbar2.set)
        #listbox.pack(side="top", fill="both", expand=True)
        scrollbar2.config(command=listbox_songs.yview)
        scrollbar2.pack(side=RIGHT,fill=Y)
        #scrollbar.place(x=365,y=259)
        listbox_songs.pack(pady=1)
        
        #POPULAR 

        

        with open('songs.txt', 'r') as f:
            songs = [line.strip() for line in f]

        update(songs,flag)

        #listbox2.bind("<<ListboxSelect>>",IncrementPlayCount)

        #listbox2.bind("<<ListboxSelect>>", fillout)
        
        search_entry.bind("<KeyRelease>",search)

        listbox_songs.bind("<<ListboxSelect>>", GetSongList)

        play_Button.bind("<Button-1>", combinedFunc)
        #play_Button.bind("<<ListboxSelect>>", CombineFunctions)

        #frame3_play = tk.Frame(self,width=259,height=480,bg="#2A2B2C",border=0)
        #sframe3_play = tk.Frame(self,width=220,height=100,bg="#F8BA43",border=0)
        #label3_play = tk.Label(self, text="MOST PLAYED",bg="#F8BA43",fg="#2A2B2C", font=controller.title3_font)

        
        play_Button.place(x=1013, y=635)

        logo_label.place(x=35,y=34)
        info_label.place(x=738,y=57)
        label_recent.place(x=831,y=179)

        
        frame2_play.place(x=90,y=148)
        label_play.place(x=138, y=179)
        #label2_play.place(x=550, y=180)
        

class AfterPerformance(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        self.controller.title("Chop-In")

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img,borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        logo_label.image = logo_img

        img= Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img)
        info_label = tk.Label(self, image=info_img,borderwidth=0)
        info_label.image = info_img

        
        main_frame = tk.Frame(self,width=988,height=545,bg="#2A2B2C",border=0)

        img= Image.open("Pictures/ScoreSum.png")
        scoreSum_img = ImageTk.PhotoImage(img)
        ScoreSummary_label =  tk.Label(self, image=scoreSum_img,cursor="hand2",borderwidth=0)
        ScoreSummary_label.image = scoreSum_img

        img= Image.open("Pictures/Perf_Report.png")
        PerfReport_img = ImageTk.PhotoImage(img)
        PerfReport_label =  tk.Label(self, image=PerfReport_img,cursor="hand2",borderwidth=0)
        PerfReport_label.image = PerfReport_img

        img= Image.open("Pictures/ErrAnal.png")
        ErrorAnal_img = ImageTk.PhotoImage(img)
        ErrorAnal_label =  tk.Label(self, image=ErrorAnal_img,cursor="hand2",borderwidth=0)
        ErrorAnal_label.image = ErrorAnal_img

        img= Image.open("Pictures/circle.png")
        circle_img = ImageTk.PhotoImage(img)
        circle_label =  tk.Label(self, image=circle_img,cursor="hand2",borderwidth=0)
        circle_label.image = circle_img

        print("afdter")
        global song_label
        score_label =  tk.Label(self, text="80%",borderwidth=0,bg="#2A2B2C",font=controller.score_font)
        song_label = tk.Label(self, text="Call Me Maybe",borderwidth=0,bg="#2A2B2C",font=controller.song_font_after)
        
        grade_frame = tk.Frame(self,width=308,height=30,bg="#2A2B2C",border=0)
        grade_label = tk.Label(grade_frame, text="GOOD PERFORMANCE!",borderwidth=0,bg="#2A2B2C",fg="#F8BA43",font=controller.grade_font)
        grade_label.pack(anchor=CENTER)

        logo_label.place(x=35,y=34)
        info_label.place(x=738,y=57)
        main_frame.place(x=105,y=124)

        ScoreSummary_label.place(x=613,y=209)
        PerfReport_label.place(x=679,y=354)
        ErrorAnal_label.place(x=613,y=499)

        circle_label.place(x=182,y=192)
        score_label.place(x=229,y=275)
        song_label.place(x=276,y=523)
        grade_frame.place(x=215,y=570)

class PerformanceReport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller

        def DisplayNote(event):
            
            notes_label.config(height=70,bg="#2A2B2C",cursor="")
            notes_frame.config(height=70,bg="#2A2B2C",cursor="")
            rhythm_frame.config(height=51,bg="#3A3A3C",cursor="hand2")
            rhythm_label.config(height=51,bg="#3A3A3C",cursor="hand2")

            total_expected_hits = 110
            correct_hits = 85
            partial_hits = 15
            extra_hits = 5 
            missed_hits = 10

            global notesData_frame
            notesData_frame = tk.Frame(self,width=734,height=414,bg="#2A2B2C")
            notesData_frame.place(x=313,y=191)

            #   CORRECT HITS
            correctHits_frame = tk.Frame(notesData_frame,bg="#2A2B2C")
            correctHits_frame.pack(side=TOP,anchor=NW,pady=15)

            correctHits_label = tk.Label(correctHits_frame,text="Correct Hits:",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            correctHits_label.pack(side=TOP)

            correct_bar = correct_hits/total_expected_hits
            correctHits_bar = tk.LabelFrame(correctHits_frame,text=total_expected_hits,bg="#3a3a3c",fg="#F7BF50",border=0,width=654,height=16,labelanchor=E,font=controller.title_font)
            correctHits_bar.pack(side=RIGHT,pady=5)
            
            correct_bar2 = correct_bar*654
            
            global correctHits_bar2
            correctHits_bar2 = tk.LabelFrame(self,text=correct_hits,bg="#F7BF50",fg="#2A2B2C",border=0,width=correct_bar2,height=16,labelanchor=E,font=controller.title_font)
            correctHits_bar2.place(x=313,y=237)
            #######################################

            #   PARTIAL HITS

            partialHits_frame =  tk.Frame(notesData_frame,bg="#2A2B2C")
            partialHits_frame.pack(side=TOP,pady=15)

            partialHits_label = tk.Label(partialHits_frame,text="Partial Hits:",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            partialHits_label.pack(side=TOP)

            partial_bar = partial_hits/total_expected_hits
            partialHits_bar = tk.LabelFrame(partialHits_frame,text=total_expected_hits,bg="#3a3a3c",fg="#F7BF50",border=0,width=654,height=16,labelanchor=E,font=controller.title_font)
            partialHits_bar.pack(side=TOP,pady=5)
            
            global partialHits_bar2
            partial_bar2 = partial_bar*654
            partialHits_bar2 = tk.LabelFrame(self,text=partial_hits,bg="#F7BF50",fg="#2A2B2C",border=0,width=partial_bar2,height=16,labelanchor=E,font=controller.title_font)
            partialHits_bar2.place(x=313,y=320)
            ####################################

            #   EXTRA HITS
            
            extraHits_frame =  tk.Frame(notesData_frame,bg="#2A2B2C")
            extraHits_frame.pack(side=TOP,pady=15)

            extraHits_label = tk.Label(extraHits_frame,text="Extra Hits:",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            extraHits_label.pack(side=TOP)

            extra_bar = extra_hits/total_expected_hits
            extraHits_bar = tk.LabelFrame(extraHits_frame,text=total_expected_hits,bg="#3a3a3c",fg="#F7BF50",border=0,width=654,height=16,labelanchor=E,font=controller.title_font)
            extraHits_bar.pack(side=TOP,pady=5)

            global extraHits_bar2
            extra_bar2 = extra_bar*654
            extraHits_bar2 = tk.LabelFrame(self,text=extra_hits,bg="#F7BF50",fg="#2A2B2C",border=0,width=extra_bar2,height=16,labelanchor=E,font=controller.title_font)
            extraHits_bar2.place(x=313,y=403)
            #####################################

            #   MISSED HITS

            missedHits_frame =  tk.Frame(notesData_frame,bg="#2A2B2C")
            missedHits_frame.pack(side=TOP,pady=15)

            missedHits_label = tk.Label(missedHits_frame,text="Missed Hits:",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            missedHits_label.pack(side=TOP)

            missed_bar = missed_hits/total_expected_hits
            missedHits_bar = tk.LabelFrame(missedHits_frame,text=total_expected_hits,bg="#3a3a3c",fg="#F7BF50",border=0,width=654,height=16,labelanchor=E,font=controller.title_font)
            missedHits_bar.pack(side=TOP,pady=5)

            global missedHits_bar2
            missed_bar2 = missed_bar*654
            missedHits_bar2 = tk.LabelFrame(self,text=missed_hits,bg="#F7BF50",fg="#2A2B2C",border=0,width=missed_bar2,height=16,labelanchor=E,font=controller.title_font)
            missedHits_bar2.place(x=313,y=487)

<<<<<<< HEAD
            try:
                rhythmData_frame.place_forget()
            except NameError:
                print("okay lang")
=======
            rhythmData_frame.place_forget()
>>>>>>> parent of 52d8259 (Revert "Merge branch 'GUI' of https://github.com/s1cnarf/Thesis1 into GUI")



        def DisplayRhythm(event):

            success_switch = 75
            failed_switch = 35

            notes_label.config(height=51,bg="#3A3A3C",cursor="hand2")
            notes_frame.config(height=51,bg="#3A3A3C",cursor="hand2")
            rhythm_label.config(height=70,bg="#2A2B2C",cursor="")
            rhythm_frame.config(height=70,bg="#2A2B2C",cursor="")

            global rhythmData_frame
            rhythmData_frame = tk.Frame(self,width=655,height=89,bg="#2A2B2C")
            rhythmData_frame.place(x=312,y=280)
            rhythmData_frame.pack_propagate(False)

            switches_frame = tk.Frame(rhythmData_frame,bg="#2A2B2C",width=655,height=26)
            switches_frame.pack(side=TOP)
            switches_frame.pack_propagate(0)

            succesSwitch_label = tk.Label(switches_frame,text="Successful Switch",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            succesSwitch_label.pack(side=LEFT,anchor=NW)

            failedSwitch_label = tk.Label(switches_frame,text="Failed",fg="#F7BF50",bg="#2A2B2C",font=controller.song_font_after)
            failedSwitch_label.pack(side=RIGHT,anchor=NE)

            total = success_switch/(success_switch+failed_switch)*655
            success_bar = tk.LabelFrame(rhythmData_frame,text=success_switch,bg="#F7BF50",fg="#2A2B2C",border=0,width=total,height=16,labelanchor=E,font=controller.title_font)
            success_bar.pack(pady=5,side=LEFT)   

            failed_bar = tk.LabelFrame(rhythmData_frame,text=failed_switch,bg="#3a3a3c",fg="#F7BF50",border=0,width=655,height=16,labelanchor=E,font=controller.title_font)
            failed_bar.pack(pady=5,side=RIGHT) 
<<<<<<< HEAD
            try:
                notesData_frame.place_forget()
            except NameError:
                print("okay lang")
=======

            notesData_frame.place_forget()
>>>>>>> parent of 52d8259 (Revert "Merge branch 'GUI' of https://github.com/s1cnarf/Thesis1 into GUI")
            correctHits_bar2.place_forget()
            partialHits_bar2.place_forget()
            extraHits_bar2.place_forget()
            missedHits_bar2.place_forget()
            
<<<<<<< HEAD
        #notesData_frame = tk.Frame(self)
        #rhythmData_frame = tk.Frame(self)
        
=======
        rhythmData_frame = tk.Frame(self,width=655,height=89,bg="#2A2B2C")
>>>>>>> parent of 52d8259 (Revert "Merge branch 'GUI' of https://github.com/s1cnarf/Thesis1 into GUI")

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img,borderwidth=0, cursor="hand2")
        #logo_label.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        logo_label.image = logo_img

        img= Image.open("Pictures/PerfReport.png")
        perfTitle_img = ImageTk.PhotoImage(img)
        perfTitle_label = tk.Label(self, image=perfTitle_img,borderwidth=0)
        perfTitle_label.image = perfTitle_img

        main_frame = tk.Frame(self,width=988,height=545,bg="#2A2B2C",border=0)
        
        dash_frame = tk.Frame(self,width=139,height=545,bg="#3A3A3C",border=0)
        dash_frame.pack_propagate(0)
        
        notes_frame = tk.Frame(dash_frame,width=139,height=70,bg="#3A3A3C",border=0)
        notes_label = tk.Label(notes_frame,width=139,height=51,text="Notes",fg="#F7BF50",bg="#3A3A3C",cursor="hand2",font=controller.Mont_bold20)
        notes_frame.pack_propagate(0)
        notes_label.bind("<Button-1>",DisplayNote)
        #notes_label.pack_propagate(0)

        rhythm_frame = tk.Frame(dash_frame,width=139,height=51,bg="#3A3A3C",border=0,cursor="hand2")
        rhythm_label = tk.Label(rhythm_frame,width=139,height=51,text="Rhythm",fg="#F7BF50",bg="#3a3a3c",font=controller.Mont_bold20)
        rhythm_frame.pack_propagate(0)
        rhythm_label.bind("<Button-1>",DisplayRhythm)
        

        artic_frame = tk.Frame(dash_frame,width=139,height=51,bg="#3A3A3C",border=0)
        artic_label = tk.Label(artic_frame,width=139,height=51,text="Articulation",fg="#F7BF50",bg="#3a3a3c",font=controller.Mont_bold20)
        artic_frame.pack_propagate(0)

        dynamics_frame = tk.Frame(dash_frame,width=139,height=51,bg="#3A3A3C",border=0)
        dynamics_label = tk.Label(dynamics_frame,width=139,height=51,text="Dynamics",fg="#F7BF50",bg="#3a3a3c",font=controller.Mont_bold20)
        dynamics_frame.pack_propagate(0)

        finger_frame = tk.Frame(dash_frame,width=139,height=51,bg="#3A3A3C",border=0)
        finger_label = tk.Label(finger_frame,width=139,height=51,text="Finger\nPattern",fg="#F7BF50",bg="#3a3a3c",font=controller.Mont_bold20)
        finger_frame.pack_propagate(0)

        
        #####################################

        
        
        main_frame.place(x=105,y=124)
        logo_label.place(x=35,y=34)
        perfTitle_label.place(x=840,y=49)

        dash_frame.place(x=105,y=124)
        
        notes_frame.pack(anchor=CENTER,pady=45)
        notes_label.pack(anchor=CENTER)

        rhythm_frame.pack(anchor=CENTER,pady=0)
        rhythm_label.pack(anchor=CENTER)

        artic_frame.pack(anchor=CENTER,pady=45)
        artic_label.pack(anchor=CENTER)

        dynamics_frame.pack(anchor=CENTER,pady=0)
        dynamics_label.pack(anchor=CENTER)

        finger_frame.pack(anchor=CENTER,pady=45)
        finger_label.pack(anchor=CENTER)






class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        label = tk.Label(self, text="Library",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

#History

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        # label = tk.Label(self, text="Statistics",bg="#F7BF50", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Home",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()
        def call(e):
            listbox_songs2.insert(song_label)

        
        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img,borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        logo_label.image = logo_img

        

        img6= Image.open("Pictures/info.png")
        info_img = ImageTk.PhotoImage(img6)
        info_label = tk.Label(self, image=info_img,borderwidth=0)
        info_label.image = info_img


        frame_histo = tk.Frame(self,width=988,height=545,bg="#2A2B2C",border=0)
        frame_histoList = tk.Frame(self,width=500,height=200,bg="#2A2B2C",border=0)



        image = Image.open("Pictures/menuHisto.png")
        image = image.resize((950,100), Image.ANTIALIAS)
        imgMenu = ImageTk.PhotoImage(image)
        
        

        labelhisto_menu = tk.Label(self, image=imgMenu,border=0)
        labelhisto_menu.image = imgMenu

        global listbox_songs2
        listbox_songs2 = tk.Listbox(frame_histoList,width=80,height=20,fg="#FFFFFF",bg="#2A2B2C",borderwidth=0,font=controller.font_song)
        scrollbar2 = tk.Scrollbar(frame_histoList,orient=VERTICAL)
        listbox_songs2.config(yscrollcommand=scrollbar2.set)
        #listbox.pack(side="top", fill="both", expand=True)
        scrollbar2.config(command=listbox_songs2.yview)
        scrollbar2.pack(side=RIGHT,fill=Y)
        #scrollbar.place(x=365,y=259)
        listbox_songs2.pack(pady=1)
        
        listbox_songs2.bind("<<ListboxSelect>>", combinedFunc)
        
        frame_histo.place(x=105,y=124)
        labelhisto_menu.place(x=120,y=128)
        frame_histoList.place(x=190,y=235)
        logo_label.place(x=35,y=34)
        info_label.place(x=738,y=57)
        

        

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        label = tk.Label(self, text="History",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()




if __name__ == "__main__":
    app = SampleApp()

    window_width = 1206
    window_height = 730
    
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    app.attributes('-fullscreen',False)
    app.resizable(False,False)
    app.mainloop()