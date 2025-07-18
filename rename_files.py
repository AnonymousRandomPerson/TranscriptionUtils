import os
from file_locations import *

rename_file_locations = [
  os.path.join(parts_folder, 'RS Incantation (original)'),
]
find_string = 'RuneScape HD'
replace_string = 'RuneScape 2'

for rename_file_location in rename_file_locations:
  for file in os.listdir(rename_file_location):
    if find_string in file:
      renamed_file = file.replace(find_string, replace_string)
      print('Renaming', file, 'to', renamed_file)
      os.rename(os.path.join(rename_file_location, file), os.path.join(rename_file_location, renamed_file))
