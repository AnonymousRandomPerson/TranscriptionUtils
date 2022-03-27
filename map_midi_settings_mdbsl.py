import os
from general_midi import *

program_mapping = {
  2: BASSOON,
  5: MARIMBA,
  10: MUSIC_BOX,
  22: GLOCKENSPIEL,
  23: ACCORDION,
  30: VIBRAPHONE,
  40: FLUTE,
  41: MARIMBA,
  42: LEAD_1_SQUARE,
  60: FRENCH_HORN,
  74: CELESTA,
  77: VIOLIN,
  79: PIZZICATO_STRINGS,
  90: MARIMBA,
  106: VIOLIN,
  120: ACOUSTIC_GUITAR_NYLON
}

program_transpose = {
  90: 12
}

percussion_parts = {
  24: ACOUSTIC_BASS_DRUM,
  25: SIDE_STICK,
  29: LOW_TOM,
  30: CLOSED_HI_HAT,
  31: LOW_MID_TOM,
  34: OPEN_HI_HAT,
  35: HI_MID_TOM,
  39: MARACAS,
  40: PEDAL_HI_HAT,
  41: None,
  42: None,
  43: None,
  44: None,
  46: None,
  50: HIGH_BONGO,
  51: LOW_BONGO,
  52: OPEN_HIGH_CONGA,
  54: TAMBOURINE,
  63: None,
  68: MUTE_TRIANGLE,
  69: OPEN_TRIANGLE,
  72: BELL_TREE,
  76: None,
  78: CRASH_CYMBAL_1,
}

percussion_programs = {49, 92, 109}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blazing Light Stormy Adventure Squad')
