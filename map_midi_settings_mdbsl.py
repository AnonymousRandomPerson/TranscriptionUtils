import os
from general_midi import *

program_mapping = {
  2: BASSOON,
  22: GLOCKENSPIEL,
  23: ACCORDION,
  30: VIBRAPHONE,
  40: FLUTE,
  41: MARIMBA,
  42: LEAD_1_SQUARE,
  60: FRENCH_HORN,
  74: CELESTA,
  79: PIZZICATO_STRINGS,
  90: MUSIC_BOX,
  106: VIOLIN,
}

program_transpose = {
}

percussion_parts = {
  39: MARACAS,
  50: HIGH_BONGO,
  51: LOW_BONGO,
  52: OPEN_HIGH_CONGA,
  63: None,
  68: MUTE_TRIANGLE,
  69: OPEN_TRIANGLE,
  76: None,
  78: CRASH_CYMBAL_1,
}

percussion_programs = {109}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blazing Light Stormy Adventure Squad')
