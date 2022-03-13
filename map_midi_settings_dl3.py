import os
from general_midi import *

program_mapping = {
}

program_transpose = {
}

percussion_parts = {
  12: ACOUSTIC_BASS_DRUM,
  13: CLOSED_HI_HAT,
  16: ACOUSTIC_SNARE,
  19: LOW_MID_TOM,
  24: HIGH_FLOOR_TOM,
  44: HI_MID_TOM,
  52: ELECTRIC_BASS_DRUM,
}

percussion_programs = {
  None,
  35,
  37,
  38,
  #39,
}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Kirby\'s Dream Land 3')
