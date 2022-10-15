import rtmidi
rtmidi.API_WINDOWS_MM in rtmidi.get_compiled_api()

# midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
# print(available_ports)

# midiout.open_port(1)
# midiout.is_port_open()  # should be True

# from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
# midiout.send_message([NOTE_ON, 67, 100])

midiIn = rtmidi.MidiIn()
midiIn.get_ports()
midiIn.open_port(0)

def handle_input(event, data=None):
    message, deltatime = event
    print(f'message: {message}, deltatime: {deltatime}, data: {data}')

midiIn.set_callback(handle_input)