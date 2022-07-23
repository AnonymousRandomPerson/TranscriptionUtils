from mido import MidiFile
import os
from file_locations import *

file = 'KSSt Sub-Tree.mid'
midi_path = os.path.join(modified_folder, file)
channel = 15

mid = MidiFile(midi_path)
notes = []
current_time = 0
for i, track in enumerate(mid.tracks):
  remove_messages = []
  for msg in track:
    matching_channel = None
    if hasattr(msg, 'channel') and msg.channel == channel and msg.type != 'note_on' and msg.type != 'note_off':
      print(i, msg)
    if hasattr(msg, 'time'):
      current_time += msg.time
    if msg.type == 'program_change' and msg.channel == channel:
      print('Program:', msg.program)
    if msg.type == 'note_on' and msg.velocity > 0 and msg.channel == channel:
      #print(msg.note, current_time / mid.ticks_per_beat)
      notes.append(msg.note)

print(notes)
