import os, shutil

drive_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
for root, subdirs, files in os.walk(drive_folder):
  for file in files:
    if file.endswith('.midi'):
      print('Renaming', file)
      shutil.move(os.path.join(root, file), os.path.join(root, file.replace('.midi', '.mid')))