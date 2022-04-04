import os
from general_midi import *

program_mapping = {
  2: BASSOON,
  5: MARIMBA,
  10: MUSIC_BOX,
  20: None,
  22: GLOCKENSPIEL,
  23: ACCORDION,
  30: VIBRAPHONE,
  34: PERCUSSIVE_ORGAN,
  40: FLUTE,
  41: MARIMBA,
  42: LEAD_1_SQUARE,
  59: TRUMPET,
  60: FRENCH_HORN,
  70: TRUMPET,
  74: CELESTA,
  77: VIOLIN,
  79: PIZZICATO_STRINGS,
  88: PAN_FLUTE,
  90: MARIMBA,
  93: ELECTRIC_BASS_FINGER,
  102: ACOUSTIC_GUITAR_NYLON,
  103: ELECTRIC_PIANO_1,
  104: ACOUSTIC_GRAND_PIANO,
  106: VIOLIN,
  113: ELECTRIC_BASS_FINGER,
  119: OBOE,
  120: ACOUSTIC_GUITAR_NYLON,
}

program_transpose = {
  90: 12,
  93: -12,
  113: -12,
}

percussion_parts = {
  24: ACOUSTIC_BASS_DRUM,
  25: SIDE_STICK,
  27: HAND_CLAP,
  28: ACOUSTIC_SNARE,
  29: LOW_TOM,
  30: CLOSED_HI_HAT,
  31: LOW_MID_TOM,
  33: None,
  34: OPEN_HI_HAT,
  35: HI_MID_TOM,
  36: None,
  38: RIDE_CYMBAL_1,
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
  64: HIGH_WOODBLOCK,
  65: LOW_WOODBLOCK,
  68: MUTE_TRIANGLE,
  69: OPEN_TRIANGLE,
  72: BELL_TREE,
  76: None,
  77: CRASH_CYMBAL_2,
  78: CRASH_CYMBAL_1,
  79: SPLASH_CYMBAL,
}

percussion_programs = {49, 91, 92, 109}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blazing Light Stormy Adventure Squad')
