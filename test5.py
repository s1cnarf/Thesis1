import ast
from ast import Load
#from ast import *
from logging import root
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from turtle import bgcolor, color, width
from PIL import ImageTk, Image
import time



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Fredoka One', size=16,slant="italic")
        self.title2_font = tkfont.Font(family='Lemon Milk', size=24, weight="bold")
        self.title3_font = tkfont.Font(family='Lemon Milk', size=20, weight="bold")
        self.button_font = tkfont.Font(family='Lemon Milk', size=16, weight="bold")
        self.button2_font = tkfont.Font(family='Lemon Milk Regular Italic', size=16, weight="bold", slant="italic")
        self.body_font = tkfont.Font(family='Lemon Milk', size=16)
        self.font_song = tkfont.Font(family='Fredoka One',size=16)
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
        for F in (LoadingPage, LogIn, Register, StartPage, PlayPage, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("LoadingPage")
        #self.show_frame("StartPage")
        

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
                controller.show_frame("LogIn")
            
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
        label = tk.Label(self, text="Song Title",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        

        image = Image.open("Pictures/recents.png")
        #image = image.resize((40,49), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)
        logo_label = tk.Label(self, image=logo_img,borderwidth=0, cursor="hand2")
        logo_label.bind("<Button-1>", lambda e: controller.show_frame("StartPage"))
        logo_label.image = logo_img

        frame_play = tk.Frame(self,width=259,height=509,bg="#2A2B2C",border=0)
        #sframe_play = tk.Frame(self,width=220,height=100,bg="#F8BA43",border=0)
        label_play = tk.Label(self, image=img,border=0)
        label_play.image = img

        

        listbox = tk.Listbox(self,width=22,height=18,fg="#FFFFFF",bg="#2A2B2C",borderwidth=0,font=controller.font_song)
        scrollbar = tk.Scrollbar(self,bg="yellow",orient=VERTICAL)
        listbox.config(yscrollcommand=scrollbar.set)
        #listbox.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        #scrollbar.pack(side=RIGHT,fill=Y)
        scrollbar.place(x=365,y=259)
        listbox.insert("end","", "all too well", "","sparks fly","", "white horse", "ama namin remix", "chocolate", "its not living if its not with you", "girls", "eh paano kung", "hindi", "ka nakilala", "bugoy drillon", "2 joints", "pakyu ka ced","song 1","song 2","song 3")

        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                label.configure(text=data)
            else:
                label.configure(text="")

        listbox.bind("<<ListboxSelect>>", callback)

        #frame_play = tk.Frame(self,width=250,height=480,bg="#2A2B2C",border=0)
        #sframe_play = tk.Frame(self,width=220,height=100,bg="#F8BA43",border=0)
        #label_play = tk.Label(self, text="RECENTS",bg="#F7BF50", font=controller.title2_font)
        frame2_play = tk.Frame(self,width=250,height=480,bg="#2A2B2C",border=0)
        sframe2_play = tk.Frame(self,width=220,height=100,bg="#F8BA43",border=0)
        label2_play = tk.Label(self, text="POPULAR",bg="#F8BA43",fg="#2A2B2C",font=controller.title3_font)
        frame3_play = tk.Frame(self,width=250,height=480,bg="#2A2B2C",border=0)
        sframe3_play = tk.Frame(self,width=220,height=100,bg="#F8BA43",border=0)
        label3_play = tk.Label(self, text="MOST PLAYED",bg="#F8BA43",fg="#2A2B2C", font=controller.title3_font)


        logo_label.place(x=35,y=34)
        frame_play.place(x=120,y=146)
        #sframe_play.place(x=175, y=150)
        label_play.place(x=130, y=158)
        listbox.place(x=137,y=253)
        frame2_play.place(x=480,y=134)
        sframe2_play.place(x=495, y=150)
        label2_play.place(x=550, y=180)
        frame3_play.place(x=800,y=134)
        sframe3_play.place(x=815, y=150)
        label3_play.place(x=840, y=180)
        


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        label = tk.Label(self, text="Library",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        label = tk.Label(self, text="Statistics",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


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