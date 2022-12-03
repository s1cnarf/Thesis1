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

ready = False

class Piano: 
    
    # Define the constructor 
    def __init__(self) -> None:

        print("INIT")
        pg.init()
        pg.fastevent.init()
        # pg.midi.init()

        self.ready = False
        self.running = True
        self.display = pg.display.set_mode((1540, 800))
        self.rectList = []
        self.iterVal = 0
        #self.font = pg.font.SysFont('Arial', 15)
        self.globalVal = 0
        self.keys = self.load_keys()
        # We Define the surfaces of the Piano Keys 

        # self.white_key_surface, self.black_key_surface = self.create_key_surfaces()
        self.white_key_surface = pg.surface.Surface(
            (1540,200))
        self.black_key_surface = pg.surface.Surface(
            (1540,200), pg.SRCALPHA, 32).convert_alpha()

        self.white_pressed_surface = pg.surface.Surface((1540,200),
        pg.SRCALPHA, 32).convert_alpha()

        self.black_pressed_surface = pg.surface.Surface((1540,200),
        pg.SRCALPHA, 32).convert_alpha()

    def draw_keys(self, surface):
        self.draw_pressed()
        #self.input_main()
        surface.blit(self.white_key_surface, (0, 600)) # Draw the UNPRESSED white key
        surface.blit(self.white_pressed_surface, (0, 600)) # Draw the PRESSED white Key
        surface.blit(self.black_key_surface, (0, 600)) # Draw the UNPRESSED black key
        surface.blit(self.black_pressed_surface, (0, 600)) # Draw the PRESSED black key
       #self.button()

        pg.display.update()
        '''
        if self.ready == False:
            pg.time.wait((3000))
            self.ready = True
            pg.init()
        else:
            self.ready = True
        '''
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

    def create_key_surfaces(self,surface):

        print("ACCESS")

        display = pg.display.set_mode((1540, 800))

        # Define the surface resolution for White Keys
        white_keys = pg.surface.Surface(
            (1540,200))
        # Define the surface resolution for White Keys
        black_keys = pg.surface.Surface(
            (1540,200), pg.SRCALPHA, 32).convert_alpha()

        newVal = 0
        localcounter = 0
        font = pg.font.SysFont('Arial', 20)
        posVal = 10

        keyset1 = ['C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1',
                   'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2',
                   'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
                   'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
                   'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
                   'C6']
        for i in range(38):  # Number of white Keys???

            if i < 10:
                # Shadow Animation
                pg.draw.rect(white_keys, (200, 200, 200),  # Resolution, Fill Color
                             (i * 43, 0, 45, 207),  # Location
                             border_radius=5)  # Border

                # White Colored Keys
                self.rectList.append(pg.draw.rect(white_keys, (255, 255, 255),
                                                  pg.Rect(i * 43, 0, 45, 200),
                                                  border_radius=5))

                # print("GL CNT: ", self.globalVal)
                white_keys.blit(font.render(keyset1[localcounter], True, (0, 0, 0)), (posVal, 130))
                posVal = posVal + 43

                self.globalVal = self.globalVal + 1
                # print("Val: ", self.globalVal)
                '''
                smallfont = pg.font.SysFont('Arial',36) 
                text = smallfont.render('1' , True , (0,0,0))
               # self.iterVal = self.iterVal + 45
                white_keys.blit(text , (10 , 130))
                white_keys.blit(text , (50 , 130))
                white_keys.blit(text , (100 , 130))
                '''
                # print("Key Value: ", newVal)
                newVal = newVal + 43

                # "Gap" animation between the keys
                pg.draw.rect(white_keys, (0, 0, 0),
                             (i * 43, 0, 45, 207),
                             width=1, border_radius=5)

                localcounter = localcounter + 1


            elif i < 20:
                # Shadow Animation
                pg.draw.rect(white_keys, (200, 200, 200),  # Resolution, Fill Color
                             (i * 43, 0, 45, 207),  # Location
                             border_radius=5)  # Border

                # White Colored Keys
                self.rectList.append(pg.draw.rect(white_keys, (255, 255, 255),
                                                  pg.Rect(i * 43, 0, 45, 200),
                                                  border_radius=5))
                white_keys.blit(font.render(keyset1[localcounter], True, (0, 0, 0)), (posVal, 130))
                posVal = posVal + 43

                self.globalVal = self.globalVal + 1
                # print("Val: ", self.globalVal)
                #  print("Key Value: ", newVal)
                newVal = newVal + 43

                # "Gap" animation between the keys
                pg.draw.rect(white_keys, (0, 0, 0),
                             (i * 43, 0, 45, 207),  # Location
                             width=1, border_radius=5)

                localcounter = localcounter + 1

            elif i < 30:
                # Shadow Animation
                pg.draw.rect(white_keys, (200, 200, 200),  # Resolution, Fill Color
                             (i * 43, 0, 45, 207),  # Location
                             border_radius=5)  # Border

                # White Colored Keys
                self.rectList.append(pg.draw.rect(white_keys, (255, 255, 255),
                                                  pg.Rect(i * 43, 0, 45, 200),
                                                  border_radius=5))
                white_keys.blit(font.render(keyset1[localcounter], True, (0, 0, 0)), (posVal, 130))
                posVal = posVal + 43

                self.globalVal = self.globalVal + 1

                # "Gap" animation between the keys
                pg.draw.rect(white_keys, (0, 0, 0),
                             (i * 43, 0, 45, 207),  # Location
                             width=1, border_radius=5)

                localcounter = localcounter + 1

            else:
                # Shadow Animation
                pg.draw.rect(white_keys, (200, 200, 200),  # Resolution, Fill Color
                             (i * 43, 0, 45, 207),  # Location
                             border_radius=5)  # Border

                # White Colored Keys
                self.rectList.append(pg.draw.rect(white_keys, (255, 255, 255),
                                                  pg.Rect(i * 43, 0, 45, 200),
                                                  border_radius=5))
                white_keys.blit(font.render(keyset1[localcounter], True, (0, 0, 0)), (posVal, 130))
                posVal = posVal + 43
                self.globalVal = self.globalVal + 1

                # "Gap" animation between the keys
                pg.draw.rect(white_keys, (0, 0, 0),
                             (i * 43, 0, 45, 207),  # Location
                             width=1, border_radius=5)

                if localcounter < 35:
                    localcounter = localcounter + 1


        for i in range(35):
            # 2 - 3 - 3 - 3 - 4 - 3 - 4 -3 4- 3 - 4 - 3
            if i not in [2,6,9,13,16,20,23,27,30,34,37,41,44]:




                # Black colored keys
                pg.draw.rect(black_keys, (0, 0, 0), 
                            (i * 43 + 26 + 2, 0, 30, 110))
                counter = i * 43 + 26 + 2
                #print("COUNTER BLK: ", counter)

        self.white_key_surface = white_keys
        self.black_key_surface = black_keys

        print(white_keys)
        print(black_keys)

        surface.blit(self.white_key_surface, (0, 600))  # Draw the UNPRESSED white key
        surface.blit(self.white_pressed_surface, (0, 600))  # Draw the PRESSED white Key
        surface.blit(self.black_key_surface, (0, 600))  # Draw the UNPRESSED black key
        surface.blit(self.black_pressed_surface, (0, 600))  # Draw the PRESSED black
        pg.display.update()
        #return (white_keys, black_keys)


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

        keyCoordinates = {
        36: 0, 38: 43, 40: 86,
        41: 129, 43: 172, 45: 215,
        47: 258, 48: 301, 50: 344,
        52: 387,

        53: 430, 55: 473, 57: 516,
        59: 559, 60: 602, 62: 645,
        64: 688, 65: 731, 67:774,
        69: 817,

        71: 860, 72: 903, 74: 946,
        76: 989, 77: 1032, 79: 1075,
        81: 1118, 83: 1161, 84: 1204,
        86: 1247,

        88: 1290, 89: 1333, 91: 1376,
        93: 1419, 95: 1462, 96: 1505

        }

        blackCoordinates = {
        37: 28, 39: 71, 42: 157, 44: 200, 46: 243,
        49: 329, 51: 372, 54: 458, 56: 501, 58: 544,
        61: 630, 63: 673, 66: 749, 68: 802, 70: 845,
        73: 931, 75: 974, 78: 1060, 80: 1103, 82: 1146,
        85: 1232, 87: 1275, 90: 1361, 92: 1404, 94: 1447
        }


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
        value = 1
        going = True
        while going:
            #print("VALUE AMOUNT: ", value)
            value = value + 1
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
                    print("KEY VAL: ", val)


                    if stat!=128:

                        if val in keyCoordinates.keys():

                            pg.draw.rect(self.white_pressed_surface,
                                     (213, 50, 66, 200), (keyCoordinates.get(val), 0, 45, 207), border_radius=5)
                        # "Gap" animation between the keys
                            pg.draw.rect(self.white_pressed_surface, (0, 0, 0),
                                     (keyCoordinates.get(val), 0, 45, 207),  # Location
                                     width=1, border_radius=5)

                        if val in blackCoordinates.keys():
                            pg.draw.rect(self.black_pressed_surface, (213, 50, 66, 200),
                                         (blackCoordinates.get(val), 0, 30, 110))

                    else:

                        if val in keyCoordinates.keys():
                            pg.draw.rect(self.white_pressed_surface,
                                         (155, 255, 255), (keyCoordinates.get(val), 0, 45, 207), border_radius=5)

                            pg.draw.rect(self.white_pressed_surface, (0, 0, 0),
                                         (keyCoordinates.get(val), 0, 45, 207),  # Location
                                         width=1, border_radius=5)

                        if val in blackCoordinates.keys():
                            pg.draw.rect(self.black_pressed_surface, (0,0,0),
                                             (blackCoordinates.get(val), 0, 30, 110))




                surface.blit(self.white_key_surface, (0, 600))  # Draw the UNPRESSED white key
                surface.blit(self.white_pressed_surface, (0, 600))  # Draw the PRESSED white Key
                surface.blit(self.black_key_surface, (0, 600))  # Draw the UNPRESSED black key
                surface.blit(self.black_pressed_surface, (0, 600))  # Draw the PRESSED black key
                pg.display.update()



            if i.poll():
                midi_events = i.read(10)
                # convert them into pygame events.
                midi_evs = pg.midi.midis2events(midi_events, i.device_id)

                for m_e in midi_evs:
                    event_post(m_e)



 # Start playing midi File in separate Thread

# pn = Piano()
#
#
# display = pg.display.set_mode((1540, 800))
# while pn.running:
#     pg.midi.init()
#     pn.create_key_surfaces(display)
#     pn.draw_keys(display)
#     pn.input_main(display)
#     pg.display.flip()
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             pn.running = False



#display = pg.display.set_mode((0,0), pg.FULLSCREEN)


# Makes sure thread has stopped before ending program


