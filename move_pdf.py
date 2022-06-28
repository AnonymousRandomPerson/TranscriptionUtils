import os, shutil
from game_acronyms import *
from file_locations import *

for file in sorted(os.listdir(finale_scores_folder)):
  if file.endswith('.pdf'):
    file_path = os.path.join(finale_scores_folder, file)
    instrument_index = file.rindex(' - ')
    combined_name = file[:instrument_index]
    game_acronym, track_name, game_name = split_track_name(combined_name)
    long_name = '{} ({}){}'.format(track_name, game_name, file[instrument_index:])

    parts_dir = os.path.join(parts_folder, combined_name)
    if os.path.isdir(parts_dir):
      dest_path = os.path.join(parts_dir, long_name)
      print('Moving', file_path, 'to', dest_path)
      shutil.move(file_path, dest_path)
    else:
      print('No parts folder found for', combined_name)
