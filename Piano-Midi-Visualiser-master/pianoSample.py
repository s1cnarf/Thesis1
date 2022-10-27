from threading import Thread
from keySample import keySample
from kmapSample import kmap
import pygame as pg 
from sys import exit

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

class Piano: 
    # Define the constructor 
    def __init__(self) -> None:
        self.keys = self.load_keys()
        
        # We Define the surfaces of the Piano Keys 
        
        self.white_key_surface , self.black_key_surface = self.create_key_surfaces()

        self.white_pressed_surface = pg.surface.Surface((1248,100),
        pg.SRCALPHA, 32).convert_alpha()

        self.black_pressed_surface = pg.surface.Surface((1248,100),
        pg.SRCALPHA, 32).convert_alpha()

    def draw_keys(self, surface):
        self.draw_pressed()
        surface.blit(self.white_key_surface, (0, 400)) # Draw the UNPRESSED white key
        surface.blit(self.white_pressed_surface, (0, 400)) # Draw the PRESSED white Key
        surface.blit(self.black_key_surface, (0, 400)) # Draw the UNPRESSED black key
        surface.blit(self.black_pressed_surface, (0, 400)) # Draw the PRESSED black key
        pg.display.update()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()


    def draw_pressed(self):
        self.white_pressed_surface.fill((0, 0, 0, 0)) # fill with white
        self.black_pressed_surface.fill((0, 0, 0, 0))

        black_dict = { # Making a dict for black keys 
            'c': 2, 'd': 3, 'f': 5, 'g': 6, 'a': 7
        }
        white_dict = { # Making a dict for white keys 
            'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'a': 7, 'b': 8
        }

        pressed_colour = (213, 50, 66, 200) # RED fill the keys when pressed

        for key in self.keys.items():
            if key[1].is_pressed:
                # Checks sharp note 
                if key[0][-1] == '#':
                    if key[0] == 'a0#': # 1st element is sharp
                        pg.draw.rect(self.black_pressed_surface, 
                        pressed_colour, (16, 0, 14, 70),
                        border_radius=5)
                    else:
                        pg.draw.rect(self.black_pressed_surface, 
                        pressed_colour, (16 + 24 * 
                        black_dict[key[0][0]] + 24 * 7 * 
                        (int(key[0][1]) - 1), 0, 14, 70),
                        border_radius=5)

                else: # IF Not Sharp
                    if key[0] == 'a0':
                            pg.draw.rect(self.white_pressed_surface,
                            pressed_colour, (0, 0, 24, 100), border_radius=5)
                    elif key[0] == 'b0':
                        pg.draw.rect(self.white_pressed_surface,
                        pressed_colour, (24, 0, 24, 100), border_radius=5)
                    else:
                        pg.draw.rect(self.white_pressed_surface,
                        pressed_colour, (24 * white_dict[key[0][0]] + 
                        (int(key[0][1]) - 1) * 24 * 7, 0, 24, 100), border_radius=5)



                

 # ----------------------------------------------------------------------------------------

    def create_key_surfaces(self):

        display = pg.display.set_mode((1248, 500))

        # Define the surface resolution for White Keys
        white_keys = pg.surface.Surface(
            (1248, 100))

        # Define the surface resolution for White Keys
        black_keys = pg.surface.Surface(
            (1248, 100), pg.SRCALPHA, 32).convert_alpha()

        for i in range (52): # Number of white Keys???

            if i <= 4 or i >= 37:
                pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                        (i * 24, 0, 24, 100), # Location
                         border_radius=5) # Border 

            # White Colored Keys
                pg.draw.rect(white_keys, (175, 220, 220), 
                        (i * 24, 0, 24, 93),
                         border_radius=5)

            # "Gap" animation between the keys 
                pg.draw.rect(white_keys, (0, 0, 0), 
                        (i * 24, 0, 24, 100),
                         width=1, border_radius=5)

            else:

            # Shadow Animation 
                pg.draw.rect(white_keys, (200, 200, 200), # Resolution, Fill Color
                        (i * 24, 0, 24, 100), # Location
                         border_radius=5) # Border 

            # White Colored Keys
                pg.draw.rect(white_keys, (255, 255, 255), 
                        (i * 24, 0, 24, 93),
                         border_radius=5)

            # "Gap" animation between the keys 
                pg.draw.rect(white_keys, (0, 0, 0), 
                        (i * 24, 0, 24, 100),
                         width=1, border_radius=5)

        for i in range(50):
            if i not in [1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46]:

                # Shadow Animation of Black Keys  
                pg.draw.rect(black_keys, (150, 150, 150), # Color
                            (i * 24 + 16, 0, 14, 68),
                             border_bottom_left_radius=2, 
                             border_bottom_right_radius=2)

                # Black colored keys
                pg.draw.rect(black_keys, (0, 0, 0), 
                            (i * 24 + 16 + 2, 0, 10, 70),
                             border_bottom_left_radius=2, 
                             border_bottom_right_radius=2)

        return (white_keys, black_keys)



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



'''
pn = Piano()


 # Start playing midi File in separate Thread


display = pg.display.set_mode((1080, 720))

pn.draw_keys(display)

# Makes sure thread has stopped before ending program
'''


