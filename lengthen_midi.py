from mido import MidiFile
import os;
from file_locations import *

target_folder = os.path.join(sf2_folder, 'Pokémon Colosseum')
source_folder = os.path.join(target_folder, 'Original')
for file in sorted(os.listdir(source_folder)):
  file_location = os.path.join(source_folder, file)
  if file.endswith('.mid'):
    mid = MidiFile(os.path.join(source_folder, file))
    mid.ticks_per_beat -= 2
    new_file_location = os.path.join(target_folder, file)
    print('Saving file to', new_file_location)
    mid.save(new_file_location)