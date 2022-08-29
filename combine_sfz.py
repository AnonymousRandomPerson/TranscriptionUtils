import os
from file_locations import *

combined_soundfont_name = 'combined.sfz'
soundfont_folder = os.path.join(soundfont_banks_folder, 'Donkey Kong Country 2', 'Stickerbush Symphony')
soundfont_bank = '001'

soundfont_folder = os.path.join(soundfont_folder, soundfont_bank)
combined_soundfont_path = os.path.join(soundfont_folder, combined_soundfont_name)

combined_soundfont = None

for file_name in sorted(os.listdir(soundfont_folder)):
  folder_path = os.path.join(soundfont_folder, file_name)
  if not folder_path.endswith('.sfz') or file_name == combined_soundfont_name:
    continue

  program = file_name[:3]
  if program == '000':
    program = '0'
  else:
    program = program.lstrip('0')
  with open(folder_path, 'r') as soundfont_file:
    soundfont = soundfont_file.read()
    if combined_soundfont:
      end_region = soundfont.find('<curve>')
      if end_region < 0:
        end_region = len(soundfont)
      regions = soundfont[soundfont.index('<region>') : end_region].rstrip('\n') + '\n\n'
      regions = regions.replace('<region>', '<region>\n loprog=%s hiprog=%s' % (program, program))
      combined_curve_index = combined_soundfont.find('<curve>')
      if combined_curve_index < 0:
        combined_curve_index = len(combined_soundfont)
      combined_soundfont = combined_soundfont[:combined_curve_index].rstrip('\n') + '\n\n' + regions + combined_soundfont[combined_curve_index:]
    else:
      combined_soundfont = soundfont.replace('<region>', '<region>\n loprog=%s hiprog=%s' % (program, program))

if combined_soundfont:
  with open(combined_soundfont_path, 'w') as combined_soundfont_file:
    combined_soundfont_file.write(combined_soundfont)
  print('Created combined soundfont at', combined_soundfont_path)
