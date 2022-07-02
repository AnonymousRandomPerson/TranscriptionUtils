import os, shutil
from file_locations import *

scores2_folder = os.path.join(finale_scores_folder, 'Scores2')

completed_midis = set()
all_musx = []

for file in sorted(os.listdir(finale_scores_folder)):
  if file.endswith('.mid'):
    completed_midis.add(file[:-4])
  elif file.endswith('.musx'):
    all_musx.append(file)

for file in all_musx:
  if file[:-5] not in completed_midis:
    print('Copying', file)
    shutil.copyfile(os.path.join(finale_scores_folder, file), os.path.join(scores2_folder, file))
