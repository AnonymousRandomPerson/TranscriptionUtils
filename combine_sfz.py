import os

combined_soundfont_name = 'combined.sfz'
soundfont_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Pokémon HeartGold and SoulSilver')
soundfont_bank = 'Route 34'

soundfont_folder = os.path.join(soundfont_folder, soundfont_bank)
combined_soundfont_path = os.path.join(soundfont_folder, combined_soundfont_name);

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
      regions = soundfont[soundfont.index('<region>') : soundfont.index('<curve>')].rstrip('\n') + '\n\n'
      regions = regions.replace('<region>', '<region>\n loprog=%s hiprog=%s' % (program, program))
      combined_curve_index = combined_soundfont.index('<curve>')
      combined_soundfont = combined_soundfont[:combined_curve_index].rstrip('\n') + '\n\n' + regions + combined_soundfont[combined_curve_index:]
    else:
      combined_soundfont = soundfont.replace('<region>', '<region>\n loprog=%s hiprog=%s' % (program, program))

if combined_soundfont:
  with open(combined_soundfont_path, 'w') as combined_soundfont_file:
    combined_soundfont_file.write(combined_soundfont)
  print('Created combined soundfont at', combined_soundfont_path)
