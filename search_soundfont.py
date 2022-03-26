import os
from typing import Set
from mido import MidiFile

soundfont_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Pokémon Emerald')
midi_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Emerald')

midi_file_name = 'Battle! (Mew)'

midi_file = os.path.join(midi_folder, midi_file_name + '.mid')
search_programs: Set[int] = set()


mid = MidiFile(midi_file)
for i, track in enumerate(mid.tracks):
  for msg in track:
    if msg.type == 'program_change':
      search_programs.add(msg.program)

print('Found programs:', list(sorted(search_programs)))

search_program_strings = [str(n).zfill(3) for n in search_programs]

for folder_name in os.listdir(soundfont_folder):
  folder_path = os.path.join(soundfont_folder, folder_name)
  if os.path.isdir(folder_path):
    folder_programs = set()
    for file_name in os.listdir(folder_path):
      if file_name.endswith('.sfz'):
        folder_programs.add(file_name[:3])
    found_match = True
    for program in search_program_strings:
      if program not in folder_programs:
        found_match = False
        break
    if found_match:
      print('Found match:', folder_name)
