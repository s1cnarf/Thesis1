import pygame as pg
from mido import MidiFile
from kmapSample import midi_number_to_note
from piano_roll import index_of_note
import sys
from keySample import *
from pianoSampleTest import Piano
from threading import Thread
import threading
import time as tm


class pRoll:

    # Define Constructor 
    def __init__(self) -> None:
        pg.init()
        pg.fastevent.init()
        pg.midi.init()

        #self.input_id = pg.midi.get_default_input_id()
        # self.i = pg.midi.Input(self.input_id)
        self.lp = 0
        self.delayVal = 0
        self.lock = threading.Lock()
        self.midiFile = self.load_midi_file()  ## addons ulets

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
        self.customClock = pg.time.Clock()
        self.time = 0
        self.piano = Piano()
        self.display = self.setup_pygame(self.song_name)
        self.background = self.create_background()

        #Extra
        self.getTicksLastFrame = 0
        self.timer = 0

    #  Draw the Image of the surface
    def draw(self, surface: pg.surface.Surface, offset: float) -> None:
        surface.blit(self.surface, (0, -self.height + offset))

    # Transcription of MIDI File

    def transcribe(self, song: MidiFile) -> list[tuple[str, float, float]]:

        note_history = []  # [note, start_time, end_time]

        playing_notes = []  # [note, start_time]

        time = 0
        # "msg" as an iterator
        for msg in song:  # Loop inside the MIDI File [from transcribe class]

            if not msg.is_meta:  # If message is a META Data
                time += msg.time  # Accumulate the initial time + time in midi data

                # Midi data is an event of NoteON/OFF and velocity is 0
                # Probably a "Release key" event

                if msg.type == "note_off" or msg.type == "note_on" and msg.velocity == 0:

                    note = midi_number_to_note(msg.note)  # Convert MIDI note # to Note Name
                    note_index = index_of_note(note, playing_notes)
                    # note_index contains -> index of the note

                    if note_index >= 0:
                        # This acts like a TMP variable that holds popped value -
                        played_note = playing_notes.pop(note_index)  # Pop the Data outside the container

                        # played_note should contain the Note# and StartTime -
                        played_note.append(time)  # Insert Time in the data container
                        # this action should append the ending time along with Note# and StartTime -

                        # Append the pop value to a new container -
                        # Played_note contains -> Index and Time  -
                        note_history.append(played_note)  # This action appends Note#-Start-End -

                    # IF a key is pressed -
                elif msg.type == "note_on":
                    note = midi_number_to_note(msg.note)  # Convert MIDI note # to Note Name
                    playing_notes.append([note, time])  # Record the Note and Starting Time  -

        return note_history
        # returns the complete value -

    def drawNotesToSurface(self) -> pg.surface.Surface:

        # Create dictionary for black keys -

        black_dict = {
            'c': 0, 'd': 1, 'f': 3, 'g': 4, 'a': 5
        }

        white_dict = {
            'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6
        }

        # Define the surface height -
        surface_height = round(self.transcribed_song[-1][2] * 100) + 500

        # Define the surface of pygame -
        surface = pg.Surface((1540, surface_height))  # x and y

        surface.set_colorkey((255, 255, 255))
        surface.fill((42, 42, 42))

        # Create a loop to draw a line

        for i in range(8):
            pg.draw.line(surface, (60, 60, 60),
                         (48 + 7 * i * 24, 0), (48 + 7 * i * 24, surface_height))

        itr = 0

        # Create a loop to to traverse the data we gathered in transcription func
        for (note, start, end) in self.transcribed_song:

            # print("This is Note 0: ", note[0], "This is Note 1: ", note[1])

            if itr == 3:
                pass

            s = round(start * 100)  # defines the initial point
            nend = round(end * 100)  # defines the end
            length = max(nend - s, 10)  # defines the duration
            nstart = surface_height - s - length  # defines the start

            # Check if the note is sharp # / a0#

            if note[-1] == '#':
                if note == 'a0#':

                    pg.draw.rect(surface, (255, 255, 255),
                                 (16, nstart, 45, length),
                                 border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (16, nstart, 45, length),
                                 width=2, border_radius=5)

                else:
                    pg.draw.rect(surface, (255, 255, 255),
                                 (26 + 43 * black_dict[note[0]] + 43 * 7 * (int(note[1]) - 1), nstart, 30, length),
                                 border_radius=5)
                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (26 + 43 * black_dict[note[0]] + 43 * 7 * (int(note[1]) - 1), nstart, 30, length),
                                 width=2, border_radius=5)

            # Else if normal note

            else:

                if note == 'a0':

                    pg.draw.rect(surface, (255, 255, 255),
                                 (0, nstart, 45, length),
                                 border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (0, nstart, 5, length),
                                 width=2, border_radius=5)

                elif note == 'b0':

                    pg.draw.rect(surface, (255, 255, 255),
                                 (24, nstart, 45, length),
                                 border_radius=5)

                    pg.draw.rect(surface, (0, 0, 0, 0),
                                 (24, nstart, 45, length),
                                 width=2, border_radius=5)
                else:

                    pg.draw.rect(surface, (255, 255, 255),
                                 (43 * white_dict[note[0]] +  # 43 * c -> 43 x 2 = 66
                                  (int(note[1]) - 1) * 43 * 7, nstart, 45, length),  # + (66-1) x 43 x  7
                                 border_radius=5)

                    # print(43 * white_dict[note[0]],"-> white dict value")
                    # print((int(note[1]) - 1) * 43 * 7, "-> block value")

                    pg.draw.rect(surface, (0, 0, 0, 0), (43 * white_dict[note[0]] +
                                                         (int(note[1]) - 1) * 43 * 7, nstart, 45, length),
                                 width=2, border_radius=5)

            itr = itr + 1

        return surface  # return the surface design

    def index_of_note(note, arr) -> int:
        for i, n in enumerate(arr):
            if n[0] == note:
                return i
        return -1

    def play_notes(self):

        cnt = 1
        delayChange = True
        NoteCheck = False
        accVal = 0
        div = 70

        for msg in self.midiFile:
            # print (msg)
            if not self.running:
                return
            if not msg.is_meta:
                # is msg is not meta
                divider = round(10 + msg.time * 100)
                formula = (msg.time * 3000) / divider
                # print("Divider Value: ",divider)
                # #print("Divider Val: ", divider)

                t = pg.time.get_ticks()
                # deltaTime in seconds.
                deltaTime = (t - pr.getTicksLastFrame) / 1000.0
                # print(f't : {t}, deltatime : {deltaTime}')
                pr.getTicksLastFrame = t

                for _ in range(divider):  # RUN THE FALLING NOTES (without this hindi baba ang notes)
                    # pg.init

                    # pg.time.delay(1000)
                    # print("XXX MSG TIME VAL:" , msg.time, "MSG TIME converted: ", msg.time*1000, "DELAY TIME: ", round((msg.time*1000 / divider)))
                    pg.time.delay(round((msg.time * 1000 / divider) - 1.5))
                    accVal = accVal + round(msg.time * 1000 / divider)
                    # print("DELAYED: ", pg.time.delay())
                    self.time += msg.time / divider
                # print ("TOTAL DELAY IN MS: ", accVal, "---------- TOTAL DELAY IN S: ", accVal/1000)
                accVal = 0
                # print(msg.time/divider,"time --> ",cnt)
                #     if delayChange and formula != 0.0:
                #        print("Delay Change: ", round(msg.time * 1000 / divider), "-- D# ", cnt)
                #        cnt = cnt + 1
                #        delayChange = False
                #     else:
                #         delayChange = False
                #
                # delayChange = True

                # print(pg.time.get_ticks())
                # print("SELF TIME: ", self.time, "Divider: ", divider)

                if msg.type == "note_on":
                    NoteCheck = True
                    pr.timer += deltaTime
                    # print("---------------- META EVENT DETECTED ---------------- ", "META#", cnt)
                    # cnt = cnt + 1
                    # print("Note: ",msg.note ,"Note ON : ", "---- ", pg.time.get_ticks() / 1000)
                    #print("NoteON: [", msg.note, "] ", self.time, "vs Ticks Val: ", pg.time.get_ticks() / 1000,
                    #      "TIME DIFFERENCE: ", "%.2f" % ((pg.time.get_ticks() / 1000) - self.time), " -- ")
                    print("NoteON: [", msg.note, "] ", self.time, "vs Ticks Val: ", pr.timer, "TIME DIFFERENCE: ",
                          "%.2f" % ((pr.timer) - self.time), " -- ")
                    # print("NOTE ON DETECTED AT: ", self.time)
                    self.piano.play_key(midi_number_to_note(msg.note),
                                        msg.velocity)


                # cnt = cnt + 1
                # break

                elif msg.type == "note_off":
                    NoteCheck = False
                    pr.timer += deltaTime
                    # print("---------------- META EVENT DETECTED ---------------- ", "META#", cnt)
                    # cnt = cnt + 1
                    # print("TIME IN TICKS/S: ", pg.time.get_ticks() / 1000)
                    # print("NoteOFF: [", msg.note, "] ", self.time, "vs Ticks Val: ", pg.time.get_ticks() / 1000, "TIME DIFFERENCE: ", "%.2f" %((pg.time.get_ticks()/1000)-self.time)," -- ")
                    # print("NOTE OFF DETECTED AT: ", self.time)
                    self.piano.stop_key(midi_number_to_note(msg.note))

        # pg.time.delay(100)
        self.running = False

    def load_midi_file(self):
        file = sys.argv[1]
        # file = 'sample.mid'
        # print("accessed the load")
        return MidiFile(file, clip=True)

    def setup_pygame(self, songName: str):
        pg.init()
        # display = pg.display.set_mode((1248, 500))
        display = pg.display.set_mode((1540, 800))
        pg.display.set_caption(f'Playing: {songName}')
        pg.mixer.set_num_channels(100)
        return display

    def create_background(self):
        background = pg.Surface((1540, 800))
        # background.fill((255, 255, 0))
        image = pg.image.load('doodad.png')
        background.blit(image, (180, 100))
        return background

    def input_main(self, surface, device_id=None):

        # pg.init()
        pr.piano.white_pressed_surface.fill((0, 0, 0, 0))  # fill with white
        pr.piano.black_pressed_surface.fill((0, 0, 0, 0))

        keyCoordinates = {
            36: 0, 38: 43, 40: 86,
            41: 129, 43: 172, 45: 215,
            47: 258, 48: 301, 50: 344,
            52: 387,

            53: 430, 55: 473, 57: 516,
            59: 559, 60: 602, 62: 645,
            64: 688, 65: 731, 67: 774,
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

        if self.lp == 1:
            # if device_id is None:
            #     input_id = pg.midi.get_default_input_id()
            #     print("INPUT:", input_id)
            # else:
            #     input_id = device_id
            #     print("DID NOT ACCESS")
            print("access true")
            # input_id = pg.midi.get_default_input_id()
            # print("using input_id :%s:" % input_id)
            # self.i = pg.midi.Input(input_id)
        id = self.i
        # print("i value: ", id)

        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                # going = False
                pr.running = False
            if e.type in [pg.KEYDOWN]:
                # going = False
                pr.running = False
            if e.type in [pg.midi.MIDIIN]:
                print(e.__dict__['data1'], "Test!!")
                val = e.__dict__['data1']
                stat = e.__dict__['status']
                print("KEY VAL: ", val)

                if stat != 128:

                    if val in keyCoordinates.keys():
                        pg.draw.rect(pr.piano.white_pressed_surface,
                                     (213, 50, 66, 200), (keyCoordinates.get(val), 0, 45, 207), border_radius=5)
                        # "Gap" animation between the keys
                        pg.draw.rect(pr.piano.white_pressed_surface, (0, 0, 0),
                                     (keyCoordinates.get(val), 0, 45, 207),  # Location
                                     width=1, border_radius=5)

                    if val in blackCoordinates.keys():
                        pg.draw.rect(pr.piano.black_pressed_surface, (213, 50, 66, 200),
                                     (blackCoordinates.get(val), 0, 30, 110))


                else:

                    if val in keyCoordinates.keys():
                        pg.draw.rect(pr.piano.white_pressed_surface,
                                     (155, 255, 255), (keyCoordinates.get(val), 0, 45, 207), border_radius=5)

                        pg.draw.rect(pr.piano.white_pressed_surface, (0, 0, 0),
                                     (keyCoordinates.get(val), 0, 45, 207),  # Location
                                     width=1, border_radius=5)

                    if val in blackCoordinates.keys():
                        pg.draw.rect(pr.piano.black_pressed_surface, (0, 0, 0),
                                     (blackCoordinates.get(val), 0, 30, 110))

            surface.blit(pr.piano.white_key_surface, (0, 600))  # Draw the UNPRESSED white key
            surface.blit(pr.piano.white_pressed_surface, (0, 600))  # Draw the PRESSED white Key
            surface.blit(pr.piano.black_key_surface, (0, 600))  # Draw the UNPRESSED black key
            surface.blit(pr.piano.black_pressed_surface, (0, 600))  # Draw the PRESSED black key
            pg.display.update(0, 0, 1540, 800)

        if id.poll():
            midi_events = id.read(10)
            # convert them into pygame events.
            midi_evs = pg.midi.midis2events(midi_events, id.device_id)

            for m_e in midi_evs:
                event_post(m_e)


if __name__ == '__main__':
    pr = pRoll()

    # Start playing midi File in separate Thread
    thread = Thread(target=pr.play_notes)

    # display = pg.display.set_mode((1248, 500))
    # pg.mixer.init()

    display = pg.display.set_mode((1540, 800))

    thread.start()

    # print("TIME IN TICKS/S: ",pg.time.get_ticks()/1000)
    pr.piano.create_key_surfaces()
    pg.display.update((0,0,1540,800))
    while pr.running:
        # print("LOOP BACK: ", pr.lp)
        pr.lp = pr.lp + 1

        pr.clock.tick(90)

        # Calculate piano roll offset

        offset = pr.time * 100 + 600

        # update keys
        pr.display.blit(pr.background, (0, 0))
        pr.draw(pr.display, offset)

        # pr.piano.draw_keys(display)

        #pr.input_main(display)
        pg.display.update(0, 0, 1540, 600)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pr.running = False

    # Makes sure thread has stopped before ending program
    if thread.is_alive():
        thread.join()
