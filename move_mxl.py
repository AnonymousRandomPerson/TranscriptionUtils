import os, shutil
from game_acronyms import *
from file_locations import *;

overwrite = True

for file in sorted(os.listdir(modified_folder)):
  if file.endswith('.mxl'):
    file_path = os.path.join(modified_folder, file)
    full_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_name)
    long_name = '{} ({}).mxl'.format(track_name, game_name)

    parts_dir = os.path.join(parts_folder, full_name)
    if os.path.isdir(parts_dir):
      found_mxl = False
      for file in os.listdir(parts_dir):
        if file.endswith('.mxl'):
          found_mxl = True
          break
      if found_mxl and not overwrite:
        print(long_name, 'already exists.')
      else:
        dest_path = os.path.join(parts_dir, long_name)
        print('Moving', file_path, 'to', dest_path)
        shutil.move(file_path, dest_path)
    else:
      print('No parts folder found for' + full_name)

for file in sorted(os.listdir(finale_scores_folder)):
  if file.endswith('.mxl'):
    shutil.move(os.path.join(finale_scores_folder, file), os.path.join(raw_exports_folder, file))
