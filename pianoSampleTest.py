from threading import Thread
from keySample import keySample
from kmapSample import kmap
import pygame as pg
import pygame.midi
import sys
import os

from sys import exit
from pygame.locals import *
import sys
from threading import Thread 





'''
 Functions used in library:
 Surface - pygame object for representing images
 .Surface() 

 SRCALPHA, the pixel format will include a per-pixel alpha
 convert_alpha: It creates a new copy of the surface with the desired pixel format.


 .blit() - draw one image onto another

 display.update() - Update portions of the screen for software displays


 .fill() - fill Surface with a solid color

'''

class Piano: #1206,730 - new 1206,130   ->  1540,800 -sa set_mode  1540,200 - sa piano
    
    # Define the constructor 
    def __init__(self) -> None:
        pg.init()
        pg.fastevent.init()
        pg.midi.init()
        self.running = True
        self.display = pg.display.set_mode((1540,800 ))
        self.rectList = []
        self.iterVal = 0
        self.font = pg.font.SysFont('Arial', 15)
        self.globalVal = 0
        self.keys = self.load_keys()
        # We Define the surfaces of the Piano Keys 
        
        self.white_key_surface , self.black_key_surface = self.create_key_surfaces()

        self.white_pressed_surface = pg.surface.Surface((1540,200),
        pg.SRCALPHA, 32).convert_alpha()

        self.black_pressed_surface = pg.surface.Surface((1540,200),
        pg.SRCALPHA, 32).convert_alpha()

    def draw_keys(self, surface):
        self.draw_pressed()
        surface.blit(self.white_key_surface, (0, 600)) # Draw the UNPRESSED white key
        surface.blit(self.white_pressed_surface, (0, 600)) # Draw the PRESSED white Key
        surface.blit(self.black_key_surface, (0, 600)) # Draw the UNPRESSED black key
        surface.blit(self.black_pressed_surface, (0, 600)) # Draw the PRESSED black key
       #self.button()

        pg.display.update()

        #self.buttonClick()


        
        
       # print(f'left={self.rectList[0].left}')

       
    
          

    def draw_pressed(self):
        self.white_pressed_surface.fill((0, 0, 0, 0)) # fill with white
        self.black_pressed_surface.fill((0, 0, 0, 0))



        black_dict = {
            'c': 0, 'd': 1, 'f': 3, 'g': 4, 'a': 5
        }

        white_dict = {
            'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6
        }

        pressed_colour = (213, 50, 66, 200) # RED fill the keys when pressed

        for key in self.keys.items():
            if key[1].is_pressed:
                # Checks sharp note 
                if key[0][-1] == '#':
                    if key[0] == 'a0#': # 1st element is sharp
                        pg.draw.rect(self.black_pressed_surface, 
                        pressed_colour, (16, 0, 45, 207),
                        border_radius=5)
                    else:
                        pg.draw.rect(self.black_pressed_surface, 
                        pressed_colour, (26 + 43 * 
                        black_dict[key[0][0]] + 43 * 7 * 
                        (int(key[0][1]) - 1), 0, 30, 110),
                        border_radius=5)

                else: # IF Not Sharp
                    if key[0] == 'a0':
                            pg.draw.rect(self.white_pressed_surface,
                            pressed_colour, (0, 0, 45, 207), border_radius=5)
                    elif key[0] == 'b0':
                        pg.draw.rect(self.white_pressed_surface,
                        pressed_colour, (24, 0, 45, 207), border_radius=5)
                    else:
                        pg.draw.rect(self.white_pressed_surface,
                        pressed_colour, (43 * white_dict[key[0][0]] + 
                        (int(key[0][1]) - 1) * 43 * 7, 0, 45, 207), border_radius=5)



                

 # ----------------------------------------------------------------------------------------

    def create_key_surfaces(self):

        display = pg.display.set_mode((1540, 800))

        # Define the surface resolution for White Keys
        white_keys = pg.surface.Surface(
            (1540,200))
        # Define the surface resolution for White Keys
        black_keys = pg.surface.Surface(
            (1540,200), pg.SRCALPHA, 32).convert_alpha()

        newVal = 0
        counter = 0

        for i in range (38): # Number of white Keys???

                if i < 10:
                    # Shadow Animation
                    pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                                (i * 43, 0, 45, 207), # Location
                                border_radius=5) # Border

                    # White Colored Keys
                    self.rectList.append(pg.draw.rect(white_keys, (155, 255, 255),
                                pg.Rect(i *43, 0, 45, 200),
                                border_radius=5))
                    self.globalVal = self.globalVal + 1
                    #print("Val: ", self.globalVal)
                    smallfont = pg.font.SysFont('Arial',36) 
                    text = smallfont.render('1' , True , (0,0,0))
                   # self.iterVal = self.iterVal + 45
                    white_keys.blit(text , (10 , 130))
                    white_keys.blit(text , (50 , 130))
                    white_keys.blit(text , (100 , 130))
                    newVal = newVal+45

                    	
                    mouse = pg.mouse.get_pos()


                    # "Gap" animation between the keys
                    pg.draw.rect(white_keys, (0, 0, 0),
                                (i * 43, 0, 45, 207),
                                width=1, border_radius=5)

                
                elif i < 20:
                    # Shadow Animation
                    pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                                (i * 43, 0, 45, 207), # Location
                                border_radius=5) # Border

                    # White Colored Keys
                    self.rectList.append(pg.draw.rect(white_keys, (100, 155, 255),
                                pg.Rect(i *43, 0, 45, 200),
                                border_radius=5))
                    self.globalVal = self.globalVal + 1
                    print("Val: ", self.globalVal)
                    

                    # "Gap" animation between the keys
                    pg.draw.rect(white_keys, (0, 0, 0),
                                 (i * 43, 0, 45, 207), # Location
                                width=1, border_radius=5)
                
                elif i < 30:
                    # Shadow Animation
                    pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                                 (i * 43, 0, 45, 207), # Location
                                border_radius=5) # Border

                    # White Colored Keys
                    self.rectList.append(pg.draw.rect(white_keys, (55, 25, 255),
                                pg.Rect(i *43, 0, 45, 200),
                                border_radius=5))
                    self.globalVal = self.globalVal + 1
                    print("Val: ", self.globalVal)
                    

                    # "Gap" animation between the keys
                    pg.draw.rect(white_keys, (0, 0, 0),
                                 (i * 43, 0, 45, 207), # Location
                                width=1, border_radius=5)

                else:
                    # Shadow Animation
                    pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                                 (i * 43, 0, 45, 207), # Location
                                border_radius=5) # Border

                    # White Colored Keys
                    self.rectList.append(pg.draw.rect(white_keys, (255, 255, 255),
                                pg.Rect(i *43, 0, 45, 200),
                                border_radius=5))
                    self.globalVal = self.globalVal + 1
                    print("Val: ", self.globalVal)
                  #  display.blit(self.font.render('HELLO', True, (255,0,0)), (i *43, 0, 235, 630))
                   # pg.display.update()

                    

                    # "Gap" animation between the keys
                    pg.draw.rect(white_keys, (0, 0, 0),
                                (i * 43, 0, 45, 207), # Location
                                width=1, border_radius=5)


        for i in range(35):
            # 2 - 3 - 3 - 3 - 4 - 3 - 4 -3 4- 3 - 4 - 3
            if i not in [2,6,9,13,16,20,23,27,30,34,37,41,44]:



                # Black colored keys
                pg.draw.rect(black_keys, (0, 0, 0), 
                            (i * 43 + 26 + 2, 0, 30, 110),
                           )


        return (white_keys, black_keys)


    def highlight(self):
        mouse_pos = pg.mouse.get_pos()
        for rect in self.rectList:
                    if rect.collidepoint(mouse_pos):
                        # prints current location of mouse
                        print('button was pressed at {0}'.format(mouse_pos))
                        hover_color = (255, 204, 203)
                        pg.draw.rect(self.display, hover_color, rect)

    def buttonClick(self):

        self.rectList[0].top = 600

        white_keys = pg.surface.Surface(
            (1540,200))

      
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                for rect in self.rectList:
                    
                    if rect.collidepoint(mouse_pos):
                        print("Current Key: ", rect)
                        # prints current location of mouse
                        print('button was pressed at {0}'.format(mouse_pos))
                        hover_color = (255, 204, 203)
                        pg.draw.rect(self.display,hover_color,rect) # -  Y coord  - Taba ng Rect - Haba ng Rectangle  (0, 600, 45, 200)
                        pg.display.update()
                        break
        



    def play_key(self, key_name: str, velocity) -> None:
        # thread = Thread(target=self.keys[key_name].play, args=[velocity])
        # thread.start()
        self.keys[key_name].play(velocity) # Calls Play from KEY Class 


    def stop_key(self, key_name: str) -> None:
        # thread = Thread(target=self.keys[key_name].stop)
        # thread.start()
        self.keys[key_name].stop()  # Calls Stop from KEY Class

    # Load the key mappings from kmapSample Class
    def load_keys(self) -> dict[str, keySample]:
        keymap = kmap()

        return {
            k: keySample(k, keymap[k], i) for i, k in enumerate(keymap)
        }

    def input_main(self,surface,device_id=None):

       # pg.init()
        self.white_pressed_surface.fill((0, 0, 0, 0))  # fill with white
        self.black_pressed_surface.fill((0, 0, 0, 0))

        event_get = pg.fastevent.get

        event_post = pg.fastevent.post

        if device_id is None:
            input_id = pg.midi.get_default_input_id()
            print("INPUT:",input_id)
        else:
            input_id = device_id
            print("DID NOT ACCESS")

        print("using input_id :%s:" % input_id)
        i = pg.midi.Input(input_id)

        going = True
        while going:
            events = event_get()
            for e in events:
                if e.type in [pg.QUIT]:
                    going = False
                if e.type in [pg.KEYDOWN]:
                    going = False
                if e.type in [pg.midi.MIDIIN]:
                    print(e.__dict__['data1'], "Test!!")
                    val = e.__dict__['data1']
                    stat = e.__dict__['status']
                    if val == 38:
                        print("ACCESS!")
                        if stat!=128:
                            pg.draw.rect(self.white_pressed_surface, (200, 200, 200),  # Resolution, Fill Color
                                         (43, 0, 45, 207),  # Location
                                         border_radius=5)  # Border
                            # "Gap" animation between the keys
                            pg.draw.rect(self.white_pressed_surface, (0, 0, 0),
                                         (43, 0, 45, 207),
                                         width=1, border_radius=5)
                            pg.draw.rect(self.white_pressed_surface,
                                     (213, 50, 66, 200), (43, 0, 45, 207), border_radius=5)
                            surface.blit(self.white_key_surface, (0, 600))  # Draw the UNPRESSED white key
                            surface.blit(self.white_pressed_surface, (0, 600))  # Draw the PRESSED white Key
                            surface.blit(self.black_key_surface, (0, 600))  # Draw the UNPRESSED black key
                            surface.blit(self.black_pressed_surface, (0, 600))  # Draw the PRESSED black key
                            pg.display.update()
                        else:

                            pg.draw.rect(self.white_pressed_surface, (200, 200, 200),  # Resolution, Fill Color
                                         (43, 0, 45, 207),  # Location
                                         border_radius=5)  # Border
                            # "Gap" animation between the keys
                            pg.draw.rect(self.white_pressed_surface, (0, 0, 0),
                                         (43, 0, 45, 207),
                                         width=1, border_radius=5)
                            pg.draw.rect(self.white_pressed_surface,
                                         (155, 255, 255), (43, 0, 45, 207), border_radius=5)
                            surface.blit(self.white_key_surface, (0, 600))  # Draw the UNPRESSED white key
                            surface.blit(self.white_pressed_surface, (0, 600))  # Draw the PRESSED white Key
                            surface.blit(self.black_key_surface, (0, 600))  # Draw the UNPRESSED black key
                            surface.blit(self.black_pressed_surface, (0, 600))  # Draw the PRESSED black key
                            pg.display.update()
                        break



            if i.poll():
                midi_events = i.read(10)
                # convert them into pygame events.
                midi_evs = pg.midi.midis2events(midi_events, i.device_id)

                for m_e in midi_evs:
                    event_post(m_e)



 # Start playing midi File in separate Thread




#display = pg.display.set_mode((0,0), pg.FULLSCREEN)


# Makes sure thread has stopped before ending program


