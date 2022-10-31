from pygame import mixer 


'''
In this class "KeySample":
-> We define our 2 major functions namely Play and Stop
 This class allow us to create an object that 
 we could call when a Key is either press or release 

Imports used:
Mixer -> pygame module for loading and playing sounds

.Channel() -> Create a Channel object for controlling playback
.Sound() -> Create a new Sound object from a file or buffer object
.play() - > begin sound playback
.set_volume() -> Set volume of the sound
.fadeout(time in ms) -> Fade out the volume on all sounds before stopping

'''


class keySample:
    # Constructor with 3 Parameters 
    def __init__(self,key_name: str,  file_name: str, channel_id: int) -> None:
        self.key_name = key_name  # Piano Key Name 
        self.file_name = file_name  # File Name of MIDI
        self.channel_id = channel_id  # Channel Number in MIDI
        self.is_pressed = False  # Is the Key Pressed? 

        #Function for a key that is Played 

    def play(self, velocity: int = 127) -> None:
    

        if velocity == 0:  
            self.stop() # When a velocity is 0 it's a NOTE OFF event
        else:
            self.is_pressed = True # On the other hand if velocity is not 0 then it's a NOT ON!
            note = mixer.Sound(self.file_name) 

            # Identifies the volume based on it's loudness or velocity

            mixer.Channel(self.channel_id).set_volume((velocity / 127)*1)
            mixer.Channel(self.channel_id).play(note)

        # Function to Stop a Key
    def stop(self) -> None:
        self.is_pressed = False # The sound will stop when the key is released
        mixer.Channel(self.channel_id).fadeout(300)





