import os

root_dir = '/Users/chenghanngan/Library/Audio/Sounds/Banks/Sforzando/ARIAConverted/sf2'

os.chdir(root_dir)
for folder in os.listdir(os.getcwd()):
  if folder.endswith('sf2'):
    os.rename(folder, folder.replace('_sf2', '').replace('_', ' '))