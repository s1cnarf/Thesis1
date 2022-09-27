import pygame as pg
from mido import MidiFile
from kmapSample import midi_number_to_note
from piano_roll import index_of_note
import sys
from keySample import * 
from pianoSample import Piano 
from threading import Thread 


class pRoll:

    # Define Constructor 
    def __init__ (self) -> None:

        self.midiFile = self.load_midi_file() ## addons ulets

        # Attribute for transcribing the MIDI file 
        self.transcribed_song = self.transcribe(self.midiFile) 

        # Layout Notes to Surface Area 
        self.surface = self.drawNotesToSurface()

        # Specifies height 
        self.height = self.surface.get_height()

        # Addons not included in original file 
        self.song_name = sys.argv[1]
        self.running = True
        self.clock = pg.time.Clock()
        self.time = 0
        self.piano = Piano()
        self.display = self.setup_pygame(self.song_name)
        self.background = self.create_background()
    


    #  Draw the Image of the surface 
    def draw(self, surface: pg.surface.Surface, offset: float) -> None: 
        surface.blit(self.surface, (0, -self.height + offset))

    
    # Transcription of MIDI File 

    def transcribe(self, song: MidiFile) -> list [tuple[str, float, float]]:

       
        note_history = []  # [note, start_time, end_time]

       
        playing_notes = []  # [note, start_time]
        

        time = 0
        # "msg" as an iterator 
        for msg in song: # Loop inside the MIDI File [from transcribe class]

            if not msg.is_meta:  # If message is a META Data
                time += msg.time # Accumulate the initial time + time in midi data
                
                # Midi data is an event of NoteON/OFF and velocity is 0 
                # Probably a "Release key" event 

                if msg.type == "note_off" or msg.type == "note_on" and msg.velocity == 0:

                    note = midi_number_to_note(msg.note) # Convert MIDI note # to Note Name 
                    note_index = index_of_note(note,playing_notes)
                    # note_index contains -> index of the note 


                    if note_index >= 0:

                        # This acts like a TMP variable that holds popped value -
                        played_note = playing_notes.pop(note_index) # Pop the Data outside the container 
                       
                        # played_note should contain the Note# and StartTime - 
                        played_note.append(time) # Insert Time in the data container 
                        # this action should append the ending time along with Note# and StartTime - 

                        # Append the pop value to a new container -
                        # Played_note contains -> Index and Time  -
                        note_history.append(played_note) # This action appends Note#-Start-End -
                    
                    # IF a key is pressed - 
                elif msg.type == "note_on": 
                    note = midi_number_to_note(msg.note) # Convert MIDI note # to Note Name 
                    playing_notes.append([note,time]) # Record the Note and Starting Time  -
        
        return note_history 
        # returns the complete value - 


    def drawNotesToSurface(self) -> pg.surface.Surface:

        # Create dictionary for black keys - 

        black_dict = {
            'c': 2, 'd': 3, 'f': 5, 'g': 6, 'a': 7
        }

        white_dict = {
            'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'a': 7, 'b': 8
        }

        #Define the surface height - 
        surface_height = round(self.transcribed_song[-1][2]*100) + 500
        
        #Define the surface of pygame - 
        surface = pg.Surface((1248, surface_height)) # x and y 

        surface.set_colorkey((255,255,255)) 
        surface.fill((42,42,42))

        # Create a loop to draw a line 

        for i in range(8):
            pg.draw.line(surface, (60, 60, 60),
            (48 + 7 * i * 24, 0), (48 + 7 * i * 24, surface_height))

        # Create a loop to to traverse the data we gathered in transcription func
        for (note,start,end) in self.transcribed_song:
            
            s = round(start * 100) # defines the initial point 
            nend = round(end *100)  # defines the end 
            length = max (nend - s, 10) # defines the duration
            nstart = surface_height -s -length # defines the start 

            # Check if the note is sharp # / a0# 

            if note[-1] == '#':
                if note == 'a0#':

                    pg.draw.rect(surface, (255, 255, 255), 
                    (16, nstart, 14, length),
                    border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                    (16, nstart, 14, length),
                    width=2, border_radius=5)

            # Else if normal note 

            else:

                if note == 'a0':

                    pg.draw.rect(surface, (255, 255, 255),
                    (0, nstart, 24, length), 
                    border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                    (0, nstart, 24, length), 
                    width=2, border_radius=5)

                elif note == 'b0':

                    pg.draw.rect(surface, (255, 255, 255),
                                 (24, nstart, 24, length), 
                                 border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (24, nstart, 24, length), 
                                 width=2, border_radius=5)
                else:

                    pg.draw.rect(surface, (255, 255, 255), 
                    (24 * white_dict[note[0]] + 
                    ( int(note[1]) - 1) * 24 * 7, nstart, 24, length),
                     border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0), (24 * white_dict[note[0]] + 
                    (int(note[1]) - 1) * 24 * 7, nstart, 24, length),
                     width=2, border_radius=5)
        
        return surface # return the surface design 

    def index_of_note(note,arr) -> int:
        for i, n in enumerate(arr):
            if n[0] == note:
                return i 
        return -1

    def play_notes(self):
        for msg in self.midiFile:

            if not self.running:
                return
            if not msg.is_meta:
                 # is msg is not meta 
                 divider = round (10 + msg.time * 100)

                 for _ in range(divider):
                     pg.time.delay(round((msg.time * 1000) / divider))
                     self.time += msg.time / divider 
                    
                 if msg.type == "note_on":
                     self.piano.play_key(midi_number_to_note(msg.note),
                      msg.velocity)
                 elif msg.type == "note_off":
                    self.piano.stop_key(midi_number_to_note(msg.note))

        pg.time.delay(1000)
        self.running = False


    def load_midi_file(self):
        file = sys.argv[1]
       #file = 'sample.mid'
        #print("accessed the load")
        return MidiFile(file, clip=True)

    def setup_pygame(self, songName: str):
        pg.init()
        display = pg.display.set_mode((1248, 500))
        pg.display.set_caption(f'Playing: {songName}')
        pg.mixer.set_num_channels(100)
        return display

    def create_background(self):
        background = pg.Surface((1248, 500))
        background.fill((255, 255, 0))
        image = pg.image.load('doodad.png')
        background.blit(image, (0, 0))
        return background




pr = pRoll()


 # Start playing midi File in separate Thread
thread = Thread(target=pr.play_notes)
thread.start()
#display = pg.display.set_mode((1248, 500))
#pg.mixer.init()


while pr.running:

    pr.clock.tick(50)

    # Calculate piano roll offaet
    offset = pr.time * 100 + 400

    #update keys 
    #pr.display.blit(pr.background, (0, 0))
    pr.draw(pr.display, offset)
    #pr.piano.draw_keys(display)
    pg.display.flip()
    
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pr.running = False

 # Makes sure thread has stopped before ending program
if thread.is_alive():
    thread.join() 
        