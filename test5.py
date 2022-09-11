
from ast import Load
from logging import root
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import *
from tkinter.ttk import Progressbar
from turtle import bgcolor, color, width
from PIL import ImageTk, Image
import time

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoadingPage, StartPage, PlayPage, PageTwo, PageThree, PageFour):
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
        

        def comm():
            
            current = loading['width']
            
            if current == 365:
                self.destroy()
                controller.show_frame("StartPage")
            
            if current < 365:
                loading.config(width=current+71)
                self.after(500,comm)
        self.after(1000,comm)

        


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        self.controller.title("Chop-In")
        self.controller.state("zoomed")

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((386,82),Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        image = Image.open("Pictures/menu1.png")
        #image = image.resize((40,49), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/library icon.png")
        #image = image.resize((67,53), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu2.png")
        #image = image.resize((88,53), Image.ANTIALIAS)
        img3 = ImageTk.PhotoImage(image)

        image = Image.open("Pictures/menu3.png")
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
        play_label4.bind("<Button-1>", lambda e: controller.show_frame("PageFour"))
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
        label = tk.Label(self, text="Play",bg="#F7BF50", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


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

    window_width = 1207
    window_height = 703
    
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    app.attributes('-fullscreen',False)
    app.resizable(False,False)
    app.mainloop()