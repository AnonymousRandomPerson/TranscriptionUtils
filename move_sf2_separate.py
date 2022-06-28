import os
import shutil
from file_locations import *

source_folder = os.path.join(soundfont_banks_folder, 'Sforzando', 'ARIAConverted', 'sf2')
target_folder = os.path.join(soundfont_banks_folder, 'Chrono Trigger')
target_folder_wav = os.path.join(target_folder, 'Wav')

for folder in os.listdir(source_folder):
  if '.' in folder:
    continue
  clean_name = folder[:-4].replace('_', ' ').replace('  ', ' ')
  print(clean_name)
  for file in os.listdir(os.path.join(source_folder, folder)):
    file_path = os.path.join(source_folder, folder, file)
    if file.endswith('.sfz'):
      with open(file_path, 'r') as sfz_file:
        sfz = sfz_file.read()
      sfz = sfz.replace('sf2_smpl.wav', os.path.join('Wav', clean_name + '.wav')).replace('lfo07_amplitude', '//lfo07_amplitude')

      with open(os.path.join(target_folder, clean_name + '.sfz'), 'w') as target_file:
        target_file.write(sfz)

    elif file.endswith('.wav'):
      shutil.copyfile(file_path, os.path.join(target_folder_wav, clean_name + '.wav'))
