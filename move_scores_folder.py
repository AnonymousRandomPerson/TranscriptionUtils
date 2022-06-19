import os, shutil, sys, time
from game_acronyms import *

copy_recent_files = True
recent_threshold = time.time() - 60 * 60 * 12

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
scores_drive_folder = os.path.join(os.sep, 'Volumes', 'GoogleDrive', 'My Drive', 'Transcribed Scores')
finale_scores_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Scores')
musescore_scores_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'MuseScore3', 'Scores')
trash_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Trash')

def move_parts(combined_name: str):
  game_parts_folder = os.path.join(parts_folder, combined_name)
  game_acronym, track_name, game_name = split_track_name(combined_name)
  drive_track_name, drive_folder = get_drive_track_name(game_acronym, track_name)
  drive_path = os.path.join(scores_drive_folder, drive_folder, drive_track_name)
  drive_pdfs = os.path.join(drive_path, 'PDFs')
  full_name = '{} ({})'.format(track_name, game_name)

  if not os.path.exists(drive_path):
    print(drive_path, 'not found.')
    return
  if not os.path.exists(drive_pdfs):
    os.mkdir(drive_pdfs)

  def copy_file_if_recent(source, dest):
    if not copy_recent_files or os.path.getmtime(source) > recent_threshold:
      print('Copying {} to {}'.format(source, dest))
      shutil.copy(source, dest)

  finale_score_path = os.path.join(finale_scores_folder, combined_name + '.musx')
  if not os.path.exists(finale_score_path):
    print('No Finale score found for', combined_name)
    return
  copy_file_if_recent(finale_score_path, os.path.join(drive_path, full_name + '.musx'))

  musescore_score_path = os.path.join(musescore_scores_folder, combined_name + '.mscz')
  if os.path.exists(musescore_score_path):
    copy_file_if_recent(musescore_score_path, os.path.join(drive_path, full_name + '.mscz'))

  pdf_files = set()
  for file in sorted(os.listdir(game_parts_folder)):
    file_path = os.path.join(game_parts_folder, file)
    if file.endswith('.pdf'):
      copy_file_if_recent(file_path, os.path.join(drive_pdfs, file))
      pdf_files.add(file)
    elif file.endswith('.mid') or file.endswith('.mxl'):
      copy_file_if_recent(file_path, os.path.join(drive_path, file))

  for file in os.listdir(drive_pdfs):
    if file.endswith('.pdf') and file not in pdf_files:
      file_path = os.path.join(drive_pdfs, file)
      print('Removing {}.'.format(file_path))
      os.remove(file_path)

if len(sys.argv) > 1:
  move_parts(sys.argv[1])
else:
  for folder in sorted(os.listdir(parts_folder)):
    if os.path.isdir(os.path.join(parts_folder, folder)):
      move_parts(folder)