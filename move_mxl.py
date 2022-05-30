import os, shutil
from game_acronyms import *

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
scores_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Scores')
mxl_folder = os.path.join('.', 'Modified')
raw_mxl_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Raw MXLs')

overwrite = True

for file in sorted(os.listdir(mxl_folder)):
  if file.endswith('.mxl'):
    file_path = os.path.join(mxl_folder, file)
    full_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_name)
    long_name = '{} ({}).mxl'.format(track_name, game_name)

    parts_dir = os.path.join(parts_folder, full_name)
    if os.path.isdir(parts_dir):
      new_mxl_file = os.path.join(parts_dir, long_name)
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

for file in sorted(os.listdir(scores_folder)):
  if file.endswith('.mxl'):
    shutil.move(os.path.join(scores_folder, file), os.path.join(raw_mxl_folder, file))
