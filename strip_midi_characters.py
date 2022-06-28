import os, shutil, sys
from file_locations import *

def strip_file(root: str, file: str, split_folder: bool):
  if file.endswith('.mid'):
    print('Renaming', file)
    modified_name = file[:-4].replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').replace('&', 'and').replace('!', '').replace('\'', '').replace('é', 'e')
    modified_name += '.mid'
    if split_folder:
      abbreviation = root[root.rfind('/') + 1:]
      abbreviation = abbreviation[:abbreviation.find(' ')]
      new_folder = os.path.join(modified_folder, abbreviation)
      if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    else:
      new_folder = modified_folder
    shutil.copy(os.path.join(root, file), os.path.join(new_folder, modified_name))

if len(sys.argv) > 1:
  for arg in sys.argv[1:]:
    root = os.path.join(parts_folder, arg)
    for file in os.listdir(root):
      strip_file(root, file, False)
else:
  for root, subdirs, files in os.walk(parts_folder):
    for file in files:
      strip_file(root, file, True)