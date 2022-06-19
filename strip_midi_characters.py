import os, shutil, sys

drive_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
new_file_location = 'Modified'

single_file = len(sys.argv) > 1
if single_file:
  drive_folder = os.path.join(drive_folder, sys.argv[1])

for root, subdirs, files in os.walk(drive_folder):
  for file in files:
    if file.endswith('.mid'):
      print('Renaming', file)
      modified_name = file[:-4].replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').replace('&', 'and').replace('!', '').replace('\'', '').replace('é', 'e')
      modified_name += '.mid'
      if single_file:
        new_folder = new_file_location
      else:
        abbreviation = root[root.rfind('/') + 1:]
        abbreviation = abbreviation[:abbreviation.find(' ')]
        new_folder = os.path.join(new_file_location, abbreviation)
        if not os.path.exists(new_folder):
          os.mkdir(new_folder)
      shutil.copy(os.path.join(root, file), os.path.join(new_folder, modified_name))