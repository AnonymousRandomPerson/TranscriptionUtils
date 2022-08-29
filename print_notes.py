from mido import MidiFile
import os
from file_locations import *

file = 'Sinister Woods.mid'
midi_path = os.path.join(modified_folder, file)
#midi_path = os.path.join(sf2_folder, 'Pokémon Mystery Dungeon Red Rescue Team', file)
channel = 0

mid = MidiFile(midi_path)
notes = []
current_time = 0
for i, track in enumerate(mid.tracks):
  for msg in track:
    matching_channel = None
    if msg.type != 'note_on' and msg.type != 'note_off' and msg.type != 'control_change' and msg.type != 'pitchwheel' and msg.type != 'aftertouch':
      pass
      #print(msg)
    if i==7:#hasattr(msg, 'channel') and msg.channel == channel:# and msg.type != 'note_on' and msg.type != 'note_off':
      pass
      print(i, msg)
    if hasattr(msg, 'time'):
      current_time += msg.time
    if msg.type == 'program_change' and msg.channel == channel:
      pass
      print('Program:', msg.program)
    if msg.type == 'note_on' and msg.velocity > 0 and msg.channel == channel:
      #print(msg.note, current_time / mid.ticks_per_beat)
      notes.append(msg.note)

#print(notes)
