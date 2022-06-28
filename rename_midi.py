import os, shutil
from file_locations import *

for root, subdirs, files in os.walk(parts_folder):
  for file in files:
    if file.endswith('.midi'):
      print('Renaming', file)
      shutil.move(os.path.join(root, file), os.path.join(root, file.replace('.midi', '.mid')))