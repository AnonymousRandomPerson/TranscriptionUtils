import os, shutil
from game_acronyms import *

rename_tracks = [
  ('CS Fight', 'Fight!'),
  ('FO OD Wait 1', 'Wait Theme 1'),
  ('FO OD Wait 2', 'Wait Theme 2'),
  ('FO OD Wait 3', 'Wait Theme 3'),
  ('FO OD Wave 3', 'Wave Theme 3'),
  ('FO SC Level 1', 'Level Theme 1'),
  ('MDGTI It\'s a Monster House', 'It\'s a Monster House!'),
  ('MDGTI Stop Thief', 'Stop Thief!'),
  ('MDR Boss Battle', 'Boss Battle!'),
  ('MDR It\'s a Thief', 'It\'s a Thief!'),
  ('MDR Monster House', 'Monster House!'),
  ('MDRTDX Monster House', 'Monster House!'),
  ('MDTDS Boss Battle', 'Boss Battle!'),
  ('MDTDS Dialga\'s Fight to the Finish', 'Dialga\'s Fight to the Finish!'),
  ('MDTDS Monster House', 'Monster House!'),
  ('MDTDS Outlaw', 'Outlaw!'),
  ('MDTDS Palkia\'s Onslaught', 'Palkia\'s Onslaught!'),
  ('MRKB Bwa Enemies', 'Bwa Enemies!'),
  ('MRKB Hoppers', 'Hoppers!'),
  ('MRKB Huggers', 'Huggers!'),
  ('SMD Boss Battle Children\'s Adventure', 'Boss Battle Children\'s Adventure!'),
  ('SMD Boss Battle with Great Powers', 'Boss Battle with Great Powers!'),
  ('SMD Legendary Boss Battle Rock Version', 'Legendary Boss Battle Rock Version!'),
  ('SMD Oh No This is Bad', 'Oh No! This is Bad!'),
  ('SMD Onward Expedition Society', 'Onward Expedition Society!'),
  ('SMD Showdown with a Volcanic Entei', 'Showdown with a Volcanic Entei!'),
]

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
scores_folder = os.path.join(os.sep, 'Volumes', 'GoogleDrive', 'My Drive', 'Transcribed Scores')

for rename_track in rename_tracks:
  old_full_name, new_track_name = rename_track
  game_acronym, old_track_name, game_name = split_track_name(old_full_name)
  drive_track_name, drive_folder = get_drive_track_name(game_acronym, old_track_name)
  drive_path = os.path.join(scores_folder, drive_folder, drive_track_name)
  parts_path = os.path.join(parts_folder, old_full_name)
  scores_path = os.path.join(scores_folder, old_full_name)

  if os.path.exists(parts_path):
    print('Renaming', old_full_name, 'in parts folder.')
    for parts_file_inner in os.listdir(parts_path):
      parts_path_inner = os.path.join(parts_path, parts_file_inner)
      shutil.move(parts_path_inner, os.path.join(parts_path, parts_file_inner.replace(old_track_name, new_track_name)))
    shutil.move(parts_path, parts_path.replace(old_track_name, new_track_name))

  if os.path.exists(drive_path):
    changed = False
    for drive_file_inner in os.listdir(drive_path):
      drive_path_inner = os.path.join(drive_path, drive_file_inner)
      if new_track_name not in drive_file_inner:
        changed = True
        shutil.move(drive_path_inner, os.path.join(drive_path, drive_file_inner.replace(old_track_name, new_track_name)))
    if changed:
      print('Renaming', old_full_name, 'in Drive folder.')
