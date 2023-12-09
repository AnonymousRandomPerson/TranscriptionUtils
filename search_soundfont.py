import os
from typing import Set
from mido import MidiFile
from file_locations import *

soundfont_folder = os.path.join(soundfont_banks_folder, 'Pokémon Emerald')
midi_folder = os.path.join(sf2_folder, 'Pokémon Emerald')

midi_file_name = 'Victory Road'

midi_file = os.path.join(midi_folder, midi_file_name + '.mid')
search_programs: Set[int] = set()


mid = MidiFile(midi_file)
for i, track in enumerate(mid.tracks):
  for msg in track:
    if msg.type == 'program_change':
      search_programs.add(msg.program)

print('Found programs:', list(sorted(search_programs)))

search_program_strings = [str(n).zfill(3) for n in search_programs]

closest_match = None
found_match = False

for folder_name in os.listdir(soundfont_folder):
  folder_path = os.path.join(soundfont_folder, folder_name)
  if os.path.isdir(folder_path):
    folder_programs = set()
    for file_name in os.listdir(folder_path):
      if file_name.endswith('.sfz'):
        folder_programs.add(file_name[:3])
    num_mismatches = 0
    for program in search_program_strings:
      if program not in folder_programs:
        num_mismatches += 1
    sorted_programs = list(sorted(folder_programs))
    if num_mismatches == 0:
      found_match = True
      print('Found match:', folder_name, sorted_programs)
    elif closest_match is None or closest_match[1] > num_mismatches:
      closest_match = (folder_name, num_mismatches, sorted_programs)

if not found_match:
  print('Closest match:', closest_match)
