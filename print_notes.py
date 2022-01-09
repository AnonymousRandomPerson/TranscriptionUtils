from mido import MidiFile
import os

midi_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Explorers of Time and Darkness')
# midi_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blue Rescue Team')
file = '030 - Craggy Coast.mid'
channel = 4

mid = MidiFile(os.path.join(midi_folder, file))
notes = []
current_time = 0
for i, track in enumerate(mid.tracks):
  for msg in track:
    matching_channel = None
    if hasattr(msg, 'time'):
      current_time += msg.time
    if msg.type == 'program_change' and msg.channel == channel:
      print('Program:', msg.program)
    if msg.type == 'note_on' and msg.velocity > 0 and msg.channel == channel:
      #print(msg.note, current_time / mid.ticks_per_beat)
      notes.append(msg.note)

print(notes)
