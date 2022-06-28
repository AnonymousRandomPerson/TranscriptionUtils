import os, shutil
from game_acronyms import *
from file_locations import *

dry_run = False

for parts_file_outer in sorted(os.listdir(parts_folder)):
  parts_path_outer = os.path.join(parts_folder, parts_file_outer)
  if os.path.isdir(parts_path_outer):
    game_acronym, track_name, game_name = split_track_name(parts_file_outer)
    drive_track_name, drive_folder = get_drive_track_name(game_acronym, track_name)
    drive_path = os.path.join(scores_drive_folder, drive_folder, drive_track_name)
    drive_pdfs = os.path.join(drive_path, 'PDFs')

    if not os.path.exists(drive_path):
      print(drive_path, 'not found.')
      continue
    if not os.path.exists(drive_pdfs):
      if dry_run:
        pass#print('Making dir', drive_pdfs)
      else:
        os.mkdir(drive_pdfs)

    drive_has_midi = False
    drive_has_mxl = False
    musx_name = None
    for drive_file in os.listdir(drive_path):
      if drive_file.endswith('.pdf'):
        source_path = os.path.join(drive_path, drive_file)
        dest_path = os.path.join(drive_pdfs, drive_file)
        if dry_run:
          pass
        else:
          shutil.move(source_path, dest_path)
      elif drive_file.endswith('.musx'):
        musx_name = drive_file[:-5]
      drive_has_midi = drive_has_midi or drive_file.endswith('.mid')
      drive_has_mxl = drive_has_mxl or drive_file.endswith('.mxl')
    if musx_name is None:
      print('No musx found for', parts_file_outer)
      continue

    for parts_file in os.listdir(parts_path_outer):
      parts_path = os.path.join(parts_path_outer, parts_file)
      if not drive_has_midi and parts_file.endswith('.mid'):
        dest_path = os.path.join(drive_path, musx_name + '.mid')
        if dry_run:
          pass
        else:
          shutil.copy(parts_path, dest_path)
      if not drive_has_mxl and parts_file.endswith('.mxl'):
        dest_path = os.path.join(drive_path, musx_name + '.mxl')
        if dry_run:
          pass
        else:
          shutil.copy(parts_path, dest_path)
