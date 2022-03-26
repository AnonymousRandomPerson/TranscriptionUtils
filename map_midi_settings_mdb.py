import os
from general_midi import *

program_mapping = {
  7: TRUMPET,
  45: VIOLIN,
  52: LEAD_1_SQUARE,
  54: VIOLIN,
  83: LEAD_1_SQUARE,
  95: VIOLIN,
  102: PERCUSSIVE_ORGAN,
  119: LEAD_1_SQUARE
}

program_transpose = {
  54: 12,
  95: 12,
  102: 24
}

percussion_parts = {
  24: ACOUSTIC_BASS_DRUM,
  29: ACOUSTIC_SNARE,
  31: HAND_CLAP,
  32: CLOSED_HI_HAT,
  33: ACOUSTIC_SNARE,
  39: PEDAL_HI_HAT,
  40: OPEN_HI_HAT,
  49: LOW_BONGO,
  50: HIGH_BONGO,
  51: OPEN_HIGH_CONGA,
  52: LOW_CONGA,
  57: MARACAS,
  68: MUTE_TRIANGLE,
  69: OPEN_TRIANGLE
}

percussion_programs = {PERCUSSION}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blue Rescue Team', 'Mapped')
