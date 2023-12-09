import os
import shutil
from file_locations import *

source_folder = os.path.join(soundfont_banks_folder, 'Sforzando', 'ARIAConverted', 'sf2', 'RuneScape_HD_sf2')
target_folder = os.path.join(soundfont_banks_folder, 'RuneScape')
target_folder_wav = os.path.join(target_folder, 'Wav')

separate = False

for file_name in os.listdir(source_folder):
  if file_name == 'sf2_smpl.wav':
    if not os.path.exists(target_folder_wav):
      os.mkdir(target_folder_wav)
    shutil.copyfile(os.path.join(source_folder, file_name), os.path.join(target_folder_wav, file_name))
  if '.' in file_name:
    continue
  for file in os.listdir(os.path.join(source_folder, file_name)):
    if separate:
      name_to_clean = file_name
    else:
      name_to_clean = file[4:]
    clean_name = name_to_clean[:-4].replace('_', ' ').replace('  ', ' ')
    file_path = os.path.join(source_folder, file_name, file)
    if file.endswith('.sfz'):
      with open(file_path, 'r') as sfz_file:
        sfz = sfz_file.read()
      if separate:
        sfz = sfz.replace('sf2_smpl.wav', os.path.join('Wav', clean_name + '.wav')).replace('lfo07_amplitude', '//lfo07_amplitude')
      else:
        sfz = sfz.replace('sf2_smpl.wav', os.path.join('sf2_smpl.wav')).replace('default_path=../', 'default_path=Wav/')

      with open(os.path.join(target_folder, clean_name + '.sfz'), 'w') as target_file:
        target_file.write(sfz)

    elif file.endswith('.wav'):
      shutil.copyfile(file_path, os.path.join(target_folder_wav, clean_name + '.wav'))
