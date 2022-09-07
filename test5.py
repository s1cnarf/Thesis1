
import tkinter as tk                
from tkinter import font as tkfont  
from tkinter import *
from PIL import ImageTk, Image

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
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg="#F7BF50")
        self.controller = controller
        self.controller.title("ChopIn")
        self.controller.state("zoomed")

        image = Image.open("Pictures/picpic.jpeg")
        image = image.resize((50,50), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(image)
   
        #label.pack(side="top", fill="x", pady=10)

        logo_pic = Image.open("Pictures/Logo.png")
        logo_pic= logo_pic.resize((250,55), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo_pic)

        logo_label = tk.Label(self, image=logo_img,borderwidth=0)
        logo_label.image = logo_img

        play_label = tk.Label(self,image=img, cursor="hand2")
        play_label.bind("<Button-1>", lambda e: controller.show_frame("PageOne"))
        play_label.image = img


        #button1 = tk.Button(self, text="PLAY MUSIC", bg='#F7BF50',font="Arial",image=img,compound=TOP,
                            #command=lambda: controller.show_frame("PageOne"))
        
        button2 = tk.Button(self, text="LIBRARY",bg="#F7BF50",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="STATISTICS",bg="#F7BF50",
                            command=lambda: controller.show_frame("PageThree"))
        button4 = tk.Button(self, text="HISTORY",
                            command=lambda: controller.show_frame("PageFour"))
    
        logo_label.place(x=14,y=15)
        play_label.place(x=400, y=5)
        #button1.place(x=400, y=5)
        button2.place(x=500, y=5)
        button3.place(x=600, y=5)
        button4.place(x=720, y=5)


class PageOne(tk.Frame):

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
    app.geometry("1207x703")
    app.mainloop()