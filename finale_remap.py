from general_midi import *
import re
from typing import Dict, List, Set
from dataclasses import dataclass, field

midi_instruments = {
  'Piano': ACOUSTIC_GRAND_PIANO,
  'Electric Piano': ELECTRIC_PIANO_1,
  'Harpsichord': HARPSICHORD,
  'Clavinet': CLAVINET,
  'Celesta': CELESTA,
  'Glass Harmonica': CELESTA,
  'Crotales': GLOCKENSPIEL,
  'Glockenspiel': GLOCKENSPIEL,
  'Music Box': MUSIC_BOX,
  'Bonang': VIBRAPHONE,
  'Gend\x8er': VIBRAPHONE,
  'Handbells': VIBRAPHONE,
  'Vibraphone': VIBRAPHONE,
  'Balafon': MARIMBA,
  'Marimba': MARIMBA,
  'Saron': XYLOPHONE,
  'Xylophone': XYLOPHONE,
  'Chimes': TUBULAR_BELLS,
  'Dulcimer': DULCIMER,
  'Organ': PERCUSSIVE_ORGAN,
  'Accordion': ACCORDION,
  'Harmonica': HARMONICA,
  'Melodica': HARMONICA,
  'Acoustic Guitar': ACOUSTIC_GUITAR_NYLON,
  'Kora': ACOUSTIC_GUITAR_NYLON,
  'Mandolin': ACOUSTIC_GUITAR_NYLON,
  'Ukulele': ACOUSTIC_GUITAR_NYLON,
  'Muted Electric Guitar': ELECTRIC_GUITAR_MUTED,
  'Electric Guitar': ELECTRIC_GUITAR_DISTORTION,
  'Electric Bass': ELECTRIC_BASS_FINGER,
  'Muted Electric Bass': ELECTRIC_GUITAR_MUTED,
  'Slap Bass': SLAP_BASS_1,
  'Synth Bass': SYNTH_BASS_1,
  'Erhu': VIOLIN,
  'Harp': ORCHESTRAL_HARP,
  'Timpani': TIMPANI,
  'Violin': STRING_ENSEMBLE_1,
  'Viola': STRING_ENSEMBLE_1,
  'Cello': STRING_ENSEMBLE_1,
  'Double Bass': STRING_ENSEMBLE_1,
  'Synth Strings': SYNTH_STRINGS_1,
  'Alto': CHOIR_AAHS,
  'Baritone': CHOIR_AAHS,
  'Bass': CHOIR_AAHS,
  'Bass Voice': CHOIR_AAHS,
  'Choir Aahs': CHOIR_AAHS,
  'Contralto': CHOIR_AAHS,
  'Soprano': CHOIR_AAHS,
  'Tenor': CHOIR_AAHS,
  'Choir Oohs': VOICE_OOHS,
  'Kirby Voice': VOICE_OOHS,
  'Vocals': VOICE_OOHS,
  'Yoshi Voice': VOICE_OOHS,
  'Synth Voice': SYNTH_VOICE,
  'Orchestra Hit': ORCHESTRA_HIT,
  'Bass Trumpet': TRUMPET,
  'Trumpet': TRUMPET,
  'Alto Trombone': TROMBONE,
  'Bass Trombone': TROMBONE,
  'Contrabass Trombone': TROMBONE,
  'Muted Trombone': TROMBONE,
  'Trombone': TROMBONE,
  'Alto Horn': TUBA,
  'Euphonium': TUBA,
  'Tuba': TUBA,
  'Muted Trumpet': MUTED_TRUMPET,
  'Flugelhorn': TRUMPET,
  'Horn': FRENCH_HORN,
  'Synth Brass': SYNTH_BRASS_1,
  'Soprano Sax': SOPRANO_SAX,
  'Alto Sax': ALTO_SAX,
  'Tenor Sax': TENOR_SAX,
  'Baritone Sax': BARITONE_SAX,
  'Oboe': OBOE,
  'Pungi': SHANAI,
  'Rhaita': SHANAI,
  'Shehnai': SHANAI,
  'English Horn': ENGLISH_HORN,
  'Bassoon': BASSOON,
  'Contrabassoon': BASSOON,
  'Didgeridoo': BASSOON,
  'Bass Clarinet': CLARINET,
  'Clarinet': CLARINET,
  'Contrabass Clarinet': CLARINET,
  'Piccolo': PICCOLO,
  'Alto Flute': FLUTE,
  'Bass Flute': FLUTE,
  'Flute': FLUTE,
  'Alto Recorder': RECORDER,
  'Bass Recorder': RECORDER,
  'Contrabass Recorder': RECORDER,
  'Sopranino Recorder': RECORDER,
  'Soprano Recorder': RECORDER,
  'Tenor Recorder': RECORDER,
  'Fife': PAN_FLUTE,
  'Pan Flute': PAN_FLUTE,
  'Tin Whistle': PAN_FLUTE,
  'Blown Bottle': BLOWN_BOTTLE,
  'Whistle': WHISTLE,
  'Ocarina': OCARINA,
  'Synth Lead': LEAD_1_SQUARE,
  'Calliope': LEAD_3_CALLIOPE,
  'Theremin': LEAD_6_SPACE_VOICE,
  'Synth Pad': PAD_2_WARM,
  'Sitar': SITAR,
  'Banjo': BANJO,
  'Shamisen': SHAMISEN,
  'Koto': KOTO,
  'Kalimba': KALIMBA,
  'Bagpipes': BAGPIPE,
  'Cowbell (Auto-tune)': AGOGO,
  'Steel Drums': STEEL_DRUMS,
  'Temple Blocks': WOODBLOCK,
  'Melodic Tom': MELODIC_TOM,
  'Breath FX': BREATH_NOISE,
  'Compressed Air FX': BREATH_NOISE,
  'Cymbal FX': BREATH_NOISE,
  'Fire FX': BREATH_NOISE,
  'Laugh FX': BREATH_NOISE,
  'Noise FX': BREATH_NOISE,
  'Sound FX': BREATH_NOISE,
  'Vacuum FX': BREATH_NOISE,
  'Whoosh FX': BREATH_NOISE,
  'Wind FX': BREATH_NOISE,
  'Bubble FX': SEASHORE,
  'Rustling FX': SEASHORE,
  'Beep FX': BIRD_TWEET,
  'Boing FX': BIRD_TWEET,
  'Laser FX': BIRD_TWEET,
  'Scream FX': BIRD_TWEET,
  'Screech FX': BIRD_TWEET,
  'Squeak FX': BIRD_TWEET,
  'Electric Bell FX': TELEPHONE_RING,
  'Drill FX': HELICOPTER,
  'Engine FX': HELICOPTER,
  'Machine FX': HELICOPTER,
  'Sweep FX': HELICOPTER,
  'Wave FX': HELICOPTER,
  'Zap FX': HELICOPTER,
  'Gun Shot FX': GUNSHOT,
  'Metal Bang FX': GUNSHOT,
  'Rock Hit FX': GUNSHOT,
  'Swirl FX': GUNSHOT,
}

mxl_instruments = {
  BIRD_TWEET: 'effect.bird.tweet',
  BREATH_NOISE: 'effect.breath',
  DRAWBAR_ORGAN: 'keyboard.organ.drawbar',
  ELECTRIC_GUITAR_DISTORTION: '',
  ELECTRIC_PIANO_2: '',
  GUNSHOT: 'effect.gunshot',
  HELICOPTER: 'effect.helicopter',
  LEAD_2_SAWTOOTH: 'synth.tone.sawtooth',
  LEAD_3_CALLIOPE: 'wind.flutes.calliope',
  MUSIC_BOX: 'pitched-percussion.music-box',
  MUTED_TRUMPET: '',
  PAD_1_NEW_AGE: 'synth.pad',
  PAD_2_WARM: 'synth.pad.warm',
  PAD_6_METALLIC: 'synth.pad.metallic',
  PAD_7_HALO: 'synth.pad.halo',
  PAD_8_SWEEP: 'synth.pad.sweep',
  PAN_FLUTE: 'wind.flutes.panpipes',
  PERCUSSIVE_ORGAN: 'keyboard.organ.percussive',
  ROCK_ORGAN: 'keyboard.organ.rotary',
  SEASHORE: 'effect.seashore',
  SLAP_BASS_1: 'effect.bass-string-slap',
  STRING_ENSEMBLE_1: 'strings.group',
  SYNTH_BRASS_1: 'brass.group.synth',
  TELEPHONE_RING: 'effect.telephone-ring',
  VIBRAPHONE: 'pitched-percussion.vibraphone',
  VOICE_OOHS: 'voice.oo',
  WHISTLE: 'wind.flutes.whistle',
  WOODBLOCK: '',
}

mxl_percussion_override = {
  'Bodhrán': LOW_BONGO,
  'Tsuzumi': HIGH_BONGO,
}

mxl_percussion_to_non_percussion = set([
  'Temple Blocks',
])

mxl_manual_remap = set([
  'Click FX',
  'Gend\x8er',
  'Guiro',
  'Melodic Tom',
  'Muted Electric Bass',
  'Muted Electric Guitar',
  'Muted Trombone',
  'Muted Trumpet',
  'Static FX',
  'Wind Chimes',
])

percussion_parts = {
  'Agogo Bells': {
    56: HIGH_AGOGO,
    58: LOW_AGOGO,
    59: HIGH_AGOGO,
    60: LOW_AGOGO,
  },
  'Bass Drum': ACOUSTIC_BASS_DRUM,
  'Bell': RIDE_BELL,
  'Bell Tree': BELL_TREE,
  'Bodhrán': LOW_BONGO,
  'Bodhr\x87n': LOW_BONGO,
  'Bongo Drums': {
    45: LOW_BONGO,
    46: LOW_BONGO,
    47: LOW_BONGO,
    48: HIGH_BONGO,
    49: HIGH_BONGO,
    50: HIGH_BONGO,
    60: HIGH_BONGO,
    61: LOW_BONGO,
  },
  'Brake Drum': RIDE_BELL,
  'Cabasa': CABASA,
  'Castanets': CASTANETS,
  'China Cymbal': CHINESE_CYMBAL,
  'Clap': HAND_CLAP,
  'Claves': CLAVES,
  'Click FX': CASTANETS,
  'Clock Tick FX': SIDE_STICK,
  'Conga Drums': {
    54: LOW_CONGA,
    55: OPEN_HIGH_CONGA,
    57: OPEN_HIGH_CONGA,
    61: OPEN_HIGH_CONGA,
    63: OPEN_HIGH_CONGA,
    64: LOW_CONGA,
    73: LOW_CONGA,
    75: LOW_CONGA,
    76: LOW_CONGA,
  },
  'Cowbell': COWBELL,
  'Crash Cymbal': {
    49: CRASH_CYMBAL_1,
    84: CRASH_CYMBAL_1,
    87: CRASH_CYMBAL_1,
    89: PEDAL_HI_HAT,
    92: CRASH_CYMBAL_1,
  },
  'Cu\x92ca': MUTE_CUICA,
  'Cuíca': MUTE_CUICA,
  'Cymbal FX': CRASH_CYMBAL_1,
  'Djembe': OPEN_HIGH_CONGA,
  'Drum Set': None,
  'Drum Set (Brushes)': None,
  'Field Drum': ACOUSTIC_SNARE,
  'Finger Cymbals': OPEN_TRIANGLE,
  'Floor Tom': {
    42: LOW_FLOOR_TOM,
    66: LOW_FLOOR_TOM,
  },
  'Goblet Drum': {
    58: LOW_CONGA,
    60: OPEN_HIGH_CONGA,
  },
  'Guiro': {
    61: LONG_GUIRO,
    62: SHORT_GUIRO,
    74: LONG_GUIRO,
  },
  'Hand Castanets': CASTANETS,
  'Hi-Hat Cymbal': {
    42: CLOSED_HI_HAT,
    44: PEDAL_HI_HAT,
    46: OPEN_HI_HAT,
    89: CLOSED_HI_HAT,
  },
  'Kick Drum': ACOUSTIC_BASS_DRUM,
  'Machine Castanets': CASTANETS,
  'Maracas': MARACAS,
  'O-daiko': {
    12: LOW_TOM,
    13: LOW_MID_TOM,
    41: LOW_TOM,
    48: LOW_MID_TOM,
  },
  'Ratchet': LONG_GUIRO,
  'Ride Cymbal': {
    92: RIDE_CYMBAL_1,
    93: RIDE_BELL,
  },
  'Sand Block': CABASA,
  'Scratching FX': CABASA,
  'Shaker': SHAKER,
  'Shime-daiko': {
    45: LOW_MID_TOM,
    47: HI_MID_TOM,
    48: HIGH_TOM,
  },
  'Sleigh Bells': JINGLE_BELL,
  'Snap': HAND_CLAP,
  'Snare Drum': {
    59: SIDE_STICK,
    60: ACOUSTIC_SNARE,
    61: SIDE_STICK,
  },
  'Snare Drum (Brushes)': ACOUSTIC_SNARE,
  'Splash Cymbal': SPLASH_CYMBAL,
  'Static FX': CASTANETS,
  'Stick Click': DRUM_STICKS,
  'Suspended Cymbal': {
    49: CRASH_CYMBAL_1,
    85: CRASH_CYMBAL_1,
    87: CRASH_CYMBAL_1,
    91: RIDE_BELL,
    92: CRASH_CYMBAL_1,
    93: CLOSED_HI_HAT,
    94: CRASH_CYMBAL_1,
  },
  'Tablas': {
    36: HIGH_BONGO,
    37: HIGH_BONGO,
    43: LOW_BONGO,
    60: HIGH_BONGO,
    61: LOW_BONGO,
  },
  'Tambourine': TAMBOURINE,
  'Tamtam': CHINESE_CYMBAL,
  'Timbales': {
    65: HIGH_TIMBALE,
    66: LOW_TIMBALE,
    70: LOW_TIMBALE,
    71: HIGH_TIMBALE,
    72: LOW_TIMBALE,
  },
  'Toms': {
    42: LOW_TOM,
    43: LOW_MID_TOM,
    44: LOW_MID_TOM,
    45: HI_MID_TOM,
    46: HI_MID_TOM,
    48: LOW_TOM,
    52: LOW_TOM,
    55: LOW_MID_TOM,
    59: LOW_MID_TOM,
    62: HI_MID_TOM,
    65: HI_MID_TOM,
    66: LOW_TOM,
    68: LOW_MID_TOM,
    69: HIGH_TOM,
    70: HI_MID_TOM,
    72: HIGH_TOM,
  },
  'Triangle': {
    80: MUTE_TRIANGLE,
    81: MUTE_TRIANGLE,
    82: OPEN_TRIANGLE,
  },
  'Tsuzumi': {
    45: LOW_BONGO,
    46: LOW_BONGO,
    48: HIGH_BONGO,
    71: HIGH_BONGO,
  },
  'VibraSlap': VIBRASLAP,
  'Washboard': SHORT_GUIRO,
  'Whip': SLAP_NOISE,
  'Wind Chimes': BELL_TREE,
  'Wood Block': HIGH_WOODBLOCK,
  'Wood Blocks': {
    63: HIGH_WOODBLOCK,
    62: LOW_WOODBLOCK,
  }
}

BONGO_DRUMS_MAPPING = {
  1: [HIGH_BONGO],
  2: [LOW_BONGO, HIGH_BONGO],
  3: [OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
  4: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
  5: [LOW_CONGA, OPEN_HIGH_CONGA, MUTE_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
}

CUICA_MAPPING = {
  1: [MUTE_CUICA],
  2: [OPEN_CUICA, MUTE_CUICA],
  3: [OPEN_CUICA, MUTE_CUICA, MUTE_CUICA],
}

percussion_sequence_mappings = {
  'Bongo Drums': BONGO_DRUMS_MAPPING,
  'Conga Drums': {
    1: [OPEN_HIGH_CONGA],
    2: [LOW_CONGA, OPEN_HIGH_CONGA],
    3: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO],
    4: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    5: [LOW_CONGA, OPEN_HIGH_CONGA, MUTE_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    6: [LOW_CONGA, OPEN_HIGH_CONGA, OPEN_HIGH_CONGA, MUTE_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    7: [LOW_CONGA, LOW_CONGA, OPEN_HIGH_CONGA, OPEN_HIGH_CONGA, MUTE_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
  },
  'Cu\x92ca': CUICA_MAPPING,
  'Cuíca': CUICA_MAPPING,
  'Tablas': BONGO_DRUMS_MAPPING,
  'Toms': {
    1: [LOW_MID_TOM],
    2: [LOW_MID_TOM, HI_MID_TOM],
    3: [LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    4: [LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    5: [HIGH_FLOOR_TOM, LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    6: [LOW_FLOOR_TOM, HIGH_FLOOR_TOM, LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    8: [LOW_FLOOR_TOM, HIGH_FLOOR_TOM, LOW_TOM, LOW_MID_TOM, LOW_MID_TOM, HI_MID_TOM, HI_MID_TOM, HIGH_TOM],
  },
  'Triangle': {
    1: [OPEN_TRIANGLE],
    2: [MUTE_TRIANGLE, OPEN_TRIANGLE],
  },
}

percussion_sequence_orders = {
  'Bongo Drums': [47, 46, 45, 48, 49, 50, 60, 61],
  'Conga Drums': [73, 76, 75, 54, 55, 57, 61, 63, 64],
  'Tablas': [43, 47, 45, 61, 36, 37, 60, 48, 50],
}

percussion_parts_override = {
}

ignore_unmapped_percussion = set([
  'ARIA Player',
  'SmartMusicSoftSynth',
  'Drum Set',
  'Drum Set (Brushes)',
])

PMD_EXPLORERS_PROGRAM_TRANSPOSE = {
  ACOUSTIC_GRAND_PIANO: -12,
  BAGPIPE: -12,
  BANJO: {
    'Aegis Cave': -12,
  },
  BASSOON: -12,
  CELESTA: {
    DEFAULT_TRACK: -12,
    'Time Gear': 0,
  },
  CELLO: -12,
  CHOIR_AAHS: {
    DEFAULT_TRACK: -12,
    'Dark Ice Mountain': 0,
    'Murky Forest': 0,
  },
  CONTRABASS: -12,
  ELECTRIC_BASS_FINGER: -12,
  ELECTRIC_PIANO_2: {
    'Amp Plains': -12,
    'Brine Cave': -12,
    'Far Amp Plains': -12,
    'Hidden Highland': -12,
  },
  ENGLISH_HORN: -12,
  FLUTE: {
    DEFAULT_TRACK: -12,
    'Blizzard Island Rescue Team Medley': 0,
  },
  FRENCH_HORN: {
    DEFAULT_TRACK: -12,
    'Foggy Forest': 0,
  },
  GLOCKENSPIEL: {
    DEFAULT_TRACK: -12,
    'Crystal Cave': 0,
  },
  HARMONICA: -12,
  HARPSICHORD: {
    'Dialga\'s Fight to the Finish!': -12,
  },
  LEAD_1_SQUARE: {
    'Blizzard Island Rescue Team Medley': {
      'Synth Lead 1': 12,
    },
    'Mt Travail': -12,
  },
  LEAD_2_SAWTOOTH: {
    'Blizzard Island Rescue Team Medley': {
      'Synth Lead 3': -12,
    },
    'Boss Battle!': -12,
    'Far Amp Plains': {
      'Synth Lead 2': -12,
    },
  },
  MELODIC_TOM: -12,
  MUSIC_BOX: -12,
  OBOE: {
    DEFAULT_TRACK: -12,
    'Wigglytuff\'s Guild': 0,
  },
  ORCHESTRAL_HARP: -12,
  PAD_1_NEW_AGE: -12,
  PICCOLO: -12,
  PIZZICATO_STRINGS: {
    DEFAULT_TRACK: -12,
    'Blizzard Island Rescue Team Medley': {
      'Cello II': -12,
    },
    'Dialga\'s Fight to the Finish!': {
      'Violin III': -12,
    },
    'Dusk Forest': {
      'Cello II': -12,
      'Double Bass I': -12,
      'Violin II': -12,
    },
    'Foggy Forest': {
      'Cello II': -12,
    },
    'In the Nightmare': {
      'Violin III': -12,
      'Violin IV': -12,
    },
    'Mt Travail': {
      'Violin I': -12,
      'Violin II': -12,
    },
  },
  SITAR: -12,
  SLAP_BASS_1: -12,
  STEEL_DRUMS: -12,
  STRING_ENSEMBLE_1: {
    'Beach Cave': {
      'Cello': -12,
      'Viola I': -12,
      'Violin I': -12,
      'Violin II': -12,
    },
    'Blizzard Island Rescue Team Medley': {
      'Cello II': -12,
    },
    'Boulder Quarry': -12,
    'Crystal Cave': {
      'Viola': -12,
      'Violin IV': -12,
      'Violin V': -12,
    },
    'Crystal Crossing': -12,
    'Dark Ice Mountain': -12,
    'Dark Wasteland': -12,
    'Deep Dusk Forest': {
      'Double Bass': -12,
    },
    'Dialga\'s Fight to the Finish!': {
      'Violin III': -12,
    },
    'Dusk Forest': {
      'Cello II': -12,
      'Double Bass I': -12,
      'Violin II': -12,
    },
    'Foggy Forest': {
      'Cello II': -12,
    },
    'Guildmaster Wigglytuff': -12,
    'Hidden Highland': -12,
    'In the Nightmare': {
      'Violin III': -12,
      'Violin IV': -12,
    },
    'Mt Travail': {
      'Violin I': -12,
      'Violin II': -12,
    },
    'Murky Forest': {
      'Cello': -12,
      'Violin III': -12,
      'Violin IV': -12,
    },
    'Mystifying Forest': {
      'Cello': -12,
      'Viola': -12,
      'Violin I': -12,
    },
    'Sky Peak Coast': {
      'Violin I': -12,
    },
    'Sky Peak Forest': {
      'Double Bass I': -12,
      'Violin IV': -12,
      'Violin V': -12,
      'Violin VI': -12,
    },
    'Sky Peak Prairie': {
      'Double Bass': -12,
      'Viola II': -12,
      'Violin I': -12,
      'Violin III': -12,
    },
    'Star Cave': {
      'Cello': -12,
      'Violin I': -12,
      'Violin II': -12,
      'Violin IV': -12,
      'Violin V': -12,
      'Violin VI': -12,
      'Violin VII': -12,
    },
    'Surrounded Sea': {
      'Cello II': -12,
      'Violin II': -12,
      'Violin III': -12,
    },
    'The Gatekeepers': {
      'Double Bass': -12,
      'Violin II': -12,
      'Violin III': -12,
    },
    'Vast Ice Mountain': {
      'Violin I': -12,
    },
  },
  SYNTH_BASS_1: -24,
  SYNTH_BRASS_1: {
    'Boss Battle!': -12,
    'Boulder Quarry': -12,
    'Craggy Coast': -12,
    'Dark Hill': -12,
  },
  SYNTH_STRINGS_1: {
    DEFAULT_TRACK: -12,
    'Spring Cave': {
      'Synth Strings 2': -12,
    },
  },
  TIMPANI: -12,
  TROMBONE: {
    'Battle against Dusknoir': -12,
    'Concealed Ruins': -12,
    'Defy the Legends': -12,
    'Random Dungeon Theme 3': -12,
  },
  TRUMPET: {
    'Bass Trumpet': -12,
    'Flugelhorn': -12,
    'Defy the Legends': -12,
    'Dialga\'s Fight to the Finish!': -12,
    'Monster House!': 0,
    'Mt Horn': -12,
    'Random Dungeon Theme 3': {
      'Bass Trumpet': -12,
      'Flugelhorn': -12,
      'Trombone': -12,
      'Trumpet 3': -12,
      'Trumpet 4': -12,
      'Trumpet 5': -12,
    }
  },
  TUBA: {
    'Wigglytuff\'s Guild': -12,
  },
  TUBULAR_BELLS: -12,
  VIBRAPHONE: -12,
  VIOLA: {
    DEFAULT_TRACK: -12,
    'Barren Valley': 0,
  },
  VIOLIN: -12,
}

program_transpose = {
  'AM': {
    BANJO: 12,
    BLOWN_BOTTLE: 12,
    CLAVINET: -12,
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -24,
      'Forest Nature Area': 0
    },
    GLOCKENSPIEL: {
      DEFAULT_TRACK: 36,
      'Space Area': 24,
    },
    OCARINA: 12,
    ORCHESTRA_HIT: 12,
    PAN_FLUTE: 12,
    SLAP_BASS_1: -24,
    STEEL_DRUMS: 12,
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'Forest Nature Area': {
        'Violin I': 12,
        'Violin II': 0,
      },
      'Olive Ocean': 24,
    },
    SYNTH_BRASS_1: {
      DEFAULT_TRACK: 12,
      'Dark Mind Battle': {
        'Synth Brass 2': 12
      },
      'Mustard Mountain': 0,
    },
    TIMPANI: {
      DEFAULT_TRACK: -12,
      'Mustard Mountain': -14
    },
    TRUMPET: {
      DEFAULT_TRACK: 12,
      'Space Area': 0,
    },
    VOICE_OOHS: 12,
  },
  'B2W2': {
    CHOIR_AAHS: {
      'Battle! (Champion - Sinnoh Version)': 12,
    },
    ELECTRIC_GUITAR_DISTORTION: {
      'Battle! (Champion - Hoenn Version)': {
        'Electric Guitar 1': -12,
      }
    },
    FRENCH_HORN: {
      'Battle! (Black Kyurem White Kyurem)': 12,
    },
    GLOCKENSPIEL: {
      DEFAULT_TRACK: 24,
      'Battle! (Black Kyurem White Kyurem)': 0,
      'Battle! (Champion Iris)': 12,
      'Battle! (Gym Leader - Sinnoh Version)': 0,
      'Route 19 (Winter)': 0,
    },
    ORCHESTRA_HIT: {
      'Battle! (Champion - Sinnoh Version)': 12,
      'Battle! (Gym Leader)': 24,
      'Battle! (N)': 12,
    },
    SLAP_BASS_1: {
      'Default': 0,
      'Pokestar Studios Battle': -12,
    },
    TIMPANI: {
      'Battle! (Black Kyurem White Kyurem)': -12,
    },
    XYLOPHONE: 12,
  },
  'BDSP': {
    CHOIR_AAHS: 12,
    TUBULAR_BELLS: {
      'Default': 12,
      'Battle! (Ramanas Park - Major Legendary Pokemon)': 0,
      'Battle! (Ramanas Park - Minor Legendary Pokemon)': 0,
    },
  },
  'BIS': {
    ACCORDION: 12,
    ACOUSTIC_GRAND_PIANO: 12,
    BANJO: 12,
    BASSOON: 12,
    CELESTA: 12,
    CHOIR_AAHS: 12,
    CHURCH_ORGAN: 12,
    CLARINET: 12,
    ELECTRIC_BASS_FINGER: {
      'Forever in the Plains': 12,
      'Meet Me at Wonder Woods (Inside Bowser)': -12,
    },
    ELECTRIC_GUITAR_CLEAN: 12,
    ELECTRIC_GUITAR_DISTORTION: 12,
    ELECTRIC_PIANO_1: 12,
    ENGLISH_HORN: 12,
    FLUTE: 12,
    FRENCH_HORN: 12,
    GLOCKENSPIEL: 24,
    HARPSICHORD: 12,
    LEAD_1_SQUARE: {
      'A Gentle Breeze at Cavi Cape (Inside Bowser)': {
        'Synth Lead 1': 12,
        'Synth Lead 2': 12,
        'Synth Lead 4': 12,
      },
      'Forever in the Plains (Inside Bowser)': 12,
      'Meet Me at Wonder Woods (Inside Bowser)': {
        'Synth Lead 1': 12,
      },
      'The Castle Depths (Inside Bowser)': {
        'Synth Lead 2': 12,
      },
      'The Grand Finale': 12,
    },
    MARIMBA: 12,
    OBOE: 12,
    ORCHESTRA_HIT: 24,
    ORCHESTRAL_HARP: 12,
    PAD_2_WARM: 12,
    PAN_FLUTE: 12,
    PERCUSSIVE_ORGAN: 24,
    PICCOLO: {
      DEFAULT_TRACK: 12,
      'The Castle Depths (Inside Bowser)': 24,
    },
    PIZZICATO_STRINGS: 12,
    SITAR: 12,
    STRING_ENSEMBLE_1: 12,
    SYNTH_BASS_1: {
      'BIS The Castle Depths (Inside Bowser)': 12,
      'BIS Tough Guy Alert!': 12,
    },
    SYNTH_BRASS_1: 12,
    TRUMPET: 12,
    VOICE_OOHS: 12,
  },
  'BW': {
    CHOIR_AAHS: {
      'Battle! (Cynthia)': 12,
    },
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -12,
      'Battle! (Strong Wild Pokemon)': 0,
      'Nimbasa City': 0,
    },
    GLOCKENSPIEL: {
      DEFAULT_TRACK: 24,
      'Route 2 (Winter)': 0,
    },
    ORCHESTRA_HIT: {
      'Battle! (Cynthia)': 12,
      'Battle! (Legendary Pokemon)': 24,
      'Battle! (N)': 12,
    },
    PICCOLO: {
      'Battle! (Cynthia)': 12,
    },
    TIMPANI: {
      'Battle! (Battle Subway Trainer)': -12,
      'Battle! (Trainer Battle)': -12,
      'Mistralton City': -12,
      'Pokemon World Championships Final': -12,
      'Route 4 (Autumn)': -12,
      'Route 4 (Spring)': -12,
      'Route 4 (Summer)': -12,
      'Route 4 (Winter)': -12,
      'Victory Lies Before You!': -12,
      'Victory Road': -12,
    },
    XYLOPHONE: 12,
  },
  'C': {
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -12,
      'Pyrite Building': 0,
      'Shadow Pokemon Lab': 0,
    },
    SLAP_BASS_1: -12,
  },
  'CT': {
    PAD_2_WARM: 12,
    SYNTH_BASS_1: {
      'World Revolution': -12,
    },
    TIMPANI: {
      'Ocean Palace': -24,
    },
  },
  'DPP': {
    CHOIR_AAHS: 12,
    LEAD_1_SQUARE: {
      'Battle! (Azelf Mesprit Uxie)': -12,
    },
    TUBULAR_BELLS: {
      DEFAULT_TRACK: 12,
      'Battle! (Azelf Mesprit Uxie)': 0,
    }
  },
  'FL': {
    VIBRAPHONE: {
      'Burning, Churning Power Plant': -36,
    },
  },
  'FRLG': {
    LEAD_1_SQUARE: {
      'Battle! (Deoxys)': {
        'Synth Lead 2': 24,
      }
    }
  },
  'HGSS': {
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -12,
      'Battle! (Ho-Oh)': 0,
      'SS Aqua': 0,
    },
    GLOCKENSPIEL: 24,
    LEAD_1_SQUARE: {
      DEFAULT_TRACK: 12,
      'Battle! (Champion)': 0,
      'SS Aqua': 0,
    },
    PERCUSSIVE_ORGAN: {
      'Azalea Town': 12,
      'Battle! (Entei)': 12,
      'Battle! (Raikou)': 12,
    },
    TIMPANI: {
      DEFAULT_TRACK: -12,
      'Battle! (Champion)': 0,
      'Battle! (Gym Leader - Kanto Version)': 0,
      'Battle! (Ho-Oh)': {
        'Timpani 1': 0,
        'Timpani 2': -12,
      },
      'Battle! (Lugia)': {
        'Timpani 1': 0,
        'Timpani 2': -12,
      },
      'Battle! (Super-Ancient Pokemon)': 0,
      'Battle! (Trainer Battle - Johto Version)': 0,
      'Battle! (Wild Pokemon - Johto Version)': 0,
    }
  },
  'K64': {
    CELESTA: 12,
    GLOCKENSPIEL: 12,
    ORCHESTRA_HIT: {
      'Studying the Factory': 12,
    },
    TIMPANI: 12,
    VIBRAPHONE: {
      DEFAULT_TRACK: 12,
      'Rock Star 3': -12,
    },
  },
  'KSSq': {
    ACOUSTIC_GUITAR_NYLON: 24,
    BANJO: 24,
    BLOWN_BOTTLE: {
      DEFAULT_TRACK: 24,
      'Vegetable Valley': 12,
    },
    CLARINET: 24,
    ELECTRIC_BASS_FINGER: 24,
    FRENCH_HORN: 24,
    GLOCKENSPIEL: 36,
    LEAD_1_SQUARE: 24,
    MARIMBA: 24,
    ORCHESTRA_HIT: 36,
    PAD_1_NEW_AGE: 24,
    PAN_FLUTE: 24,
    PICCOLO: 24,
    PIZZICATO_STRINGS: 24,
    STEEL_DRUMS: 36,
    STRING_ENSEMBLE_1: 24,
    SYNTH_BRASS_1: 24,
    TIMPANI: 36,
    TRUMPET: 36,
    TUBA: 24,
    VOICE_OOHS: 24,
  },
  'KSSt': {
    ORCHESTRA_HIT: 12,
  },
  'LTTP': {
    FLUTE: 12,
    TIMPANI: 12,
  },
  'MDB': {
    BASSOON: -12,
    CHOIR_AAHS: {
      'Great Canyon': -12,
      'Mt Blaze': -12,
      'Sky Tower': -12,
      'The Escape': -12,
    },
    PAN_FLUTE: 12,
    PERCUSSIVE_ORGAN: 12,
    PIZZICATO_STRINGS: {
      'Sinister Woods': 12,
    },
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'It\'s a Thief!': {
        'Violin II': 12,
        'Viola': 12,
      },
      'Lapis Cave': {
        'Violin III': 12,
        'Violin IV': 12,
        'Cello': 12,
        'Double Bass': 12,
      },
      'Makuhita Dojo': {
        'Violin III': 12,
        'Viola': 12,
      },
      'Monster House!': 0,
      'Mt Freeze': {
        'Violin III': 12,
        'Violin IV': 12,
        'Cello': 12,
      },
      'Mt Thunder': 0,
      'Sky Tower': {
        'Violin I': 12,
        'Violin III': 12,
        'Viola': 12,
      },
      'Stormy Sea': {
        'Violin II': 12,
        'Violin III': 12,
      },
      'The Escape': {
        'Violin II': 12,
        'Violin III': 12,
        'Viola I': 12,
      },
      'Thunderwave Cave': {
        'Violin II': 12,
        'Viola I': 12,
        'Viola II': 12,
      },
      'Tiny Woods': {
        'Violin I': 12,
        'Violin II': 12,
      },
    },
    SYNTH_BASS_1: -12,
    TIMPANI: 12,
    VIOLIN: {
      'Sinister Woods': 12,
      'Sky Tower': 12,
    },
  },
  'MDR': {
    BASSOON: -12,
    CELESTA: 12,
    CHOIR_AAHS: {
      'Great Canyon': -12,
      'Mt Blaze': -12,
      'Sky Tower': -12,
      'The Escape': -12,
    },
    LEAD_1_SQUARE: {
      'Mt Thunder': {
        'Synth Bass': -12,
      },
    },
    LEAD_2_SAWTOOTH: {
      'A New Adventure': -12,
      'Boss Battle!': {
        'Synth Bass': -12,
      },
      'Great Canyon': {
        'Synth Bass': -12,
      },
      'It\'s a Thief!': {
        'Synth Bass': -12,
      },
      'Lapis Cave': {
        'Synth Bass': -12,
      },
      'Makuhita Dojo': {
        'Synth Bass': -12,
      },
      'Monster House!': {
        'Synth Bass': -12,
      },
      'Mt Blaze': {
        'Synth Bass': -12,
      },
      'Mt Freeze': {
        'Synth Bass': -12,
      },
      'Mt Steel': {
        'Synth Bass': -12,
      },
      'Silent Chasm': {
        'Synth Bass': -12,
      },
      'Sinister Woods': {
        'Synth Bass': -12,
      },
      'Sky Tower': {
        'Synth Bass': -12,
      },
      'Sky Tower Summit': {
        'Synth Bass': -12,
      },
      'Stormy Sea': {
        'Synth Bass': -12,
      },
      'The Escape': {
        'Synth Bass': -12,
      },
      'Thunderwave Cave': {
        'Synth Bass': -12,
      },
      'Tiny Woods': {
        'Synth Bass': -12,
      },
    },
    PAN_FLUTE: 12,
    PERCUSSIVE_ORGAN: 12,
    PIZZICATO_STRINGS: {
      'Sinister Woods': 12,
    },
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'It\'s a Thief!': {
        'Violin II': 12,
        'Viola': 12,
      },
      'Lapis Cave': {
        'Violin III': 12,
        'Violin IV': 12,
        'Cello': 12,
        'Double Bass': 12,
      },
      'Makuhita Dojo': {
        'Violin III': 12,
        'Viola': 12,
      },
      'Monster House!': 0,
      'Mt Freeze': {
        'Violin III': 12,
        'Violin IV': 12,
        'Cello': 12,
      },
      'Mt Thunder': 0,
      'Sky Tower': {
        'Violin I': 12,
        'Viola I': 12,
        'Viola II': 12,
      },
      'Stormy Sea': {
        'Violin II': 12,
        'Violin III': 12,
      },
      'The Escape': {
        'Violin II': 12,
        'Violin III': 12,
        'Viola I': 12,
      },
      'Thunderwave Cave': {
        'Violin II': 12,
        'Viola I': 12,
        'Viola II': 12,
      },
      'Tiny Woods': {
        'Violin I': 12,
        'Violin II': 12,
      },
    },
    SYNTH_BASS_1: -12,
    SYNTH_BRASS_1: 12,
    VIOLIN: {
      'Sinister Woods': 12,
      'Sky Tower': 12,
    },
  },
  'MDRTDX': {
    BASSOON: -12,
    CHOIR_AAHS: {
      'Great Canyon': -12,
      'Mt Blaze': -12,
      'Sky Tower': -12,
      'The Escape': -12,
    },
    PERCUSSIVE_ORGAN: 12,
    PIZZICATO_STRINGS: {
      'Sinister Woods': 12,
    },
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'Frosty Forest': {
        'Violin I': 12,
        'Violin II': 12,
      },
      'Lapis Cave': {
        'Violin III': 12,
        'Violin IV': 12,
        'Cello': 12,
        'Double Bass': 12,
      },
      'Makuhita Dojo': {
        'Violin III': 12,
        'Viola': 12,
        'Cello': 12,
      },
      'Monster House!': 0,
      'Mt Thunder': 0,
      'Oddity Cave': 0,
      'Sky Tower': {
        'Violin I': 12,
        'Violin III': 12,
        'Viola': 12,
      },
      'Stormy Sea': {
        'Violin II': 12,
        'Violin III': 12,
      },
      'The Escape': {
        'Violin II': 12,
        'Violin III': 12,
        'Viola I': 12,
      },
      'Thunderwave Cave': {
        'Violin II': 12,
        'Viola I': 12,
        'Viola II': 12,
      },
      'Tiny Woods': {
        'Violin I': 12,
        'Violin II': 12,
      },
    },
    SYNTH_BASS_1:{
      DEFAULT_TRACK: -12,
      'Sinister Woods': 0,
    },
    TIMPANI: {
      DEFAULT_TRACK: 12,
      'Oddity Cave': 0,
    },
    VIOLIN: {
      'Sinister Woods': 12,
      'Sky Tower': 12,
    },
  },
  'MDS': PMD_EXPLORERS_PROGRAM_TRANSPOSE,
  'MDTDS': PMD_EXPLORERS_PROGRAM_TRANSPOSE,
  'MK8D': {
    PERCUSSIVE_ORGAN: {
      'Choco Mountain': 12,
      'Choco Mountain (Final Lap)': 12,
    },
  },
  'MKDS': {
    PERCUSSIVE_ORGAN: 12,
  },
  'MLSS': {
    ELECTRIC_BASS_FINGER: -12,
    PIZZICATO_STRINGS: -12,
    STEEL_DRUMS: 12,
    STRING_ENSEMBLE_1: {
      'Decisive Battleground': {
        'Cello': -12,
      }
    },
    SYNTH_BASS_1: -24,
    TIMPANI: -12,
    TUBA: -24,
  },
  'MLSSBM': {
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -12,
      'Sweet Surfin\'': 0,
    },
    PIZZICATO_STRINGS: {
      'Decisive Battleground': -12,
    },
    STRING_ENSEMBLE_1: {
      'Decisive Battleground': {
        'Cello I': -12,
      }
    },
    STEEL_DRUMS: 12,
    TIMPANI: -12,
    TUBA: -24,
  },
  'Pt': {
    LEAD_1_SQUARE: {
      'Battle! (Regirock Regice Registeel)': {
        'Synth Lead 1': 12,
      },
    },
    TUBULAR_BELLS: 12,
  },
}

PMD_EXPLORERS_MIDI_INSTRUMENT_OVERRIDES = {
  'Electric Piano': ELECTRIC_PIANO_2,
  'Synth Pad': PAD_1_NEW_AGE,
}

midi_instrument_overrides = {
  'AM Space Area': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'B2W2 Battle! (Champion - Kanto Version)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'B2W2 Battle! (Champion - Sinnoh Version)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'B2W2 Battle! (Colress)': {
    'Vocals': BREATH_NOISE,
  },
  'B2W2 Driftveil City Gym': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'B2W2 Virbank City': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BBT Buckle Your Pants (instrumental)': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Lead 5': LEAD_2_SAWTOOTH,
    'Vocals 1': BREATH_NOISE,
    'Vocals 2': BREATH_NOISE,
  },
  'BBT Level Theme 9': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BBT Panic Version': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'BDSP Battle! (Azelf Mesprit Uxie)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BDSP Battle! (Dialga Palkia)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BDSP Battle! (Giratina)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BDSP Stark Mountain': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BDSP Fight Area (Day)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BDSP Fight Area (Night)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BIS Bowser\'s Stolen Castle': {
    'Organ': CHURCH_ORGAN,
  },
  'BIS Meet Me at Wonder Woods (Inside Bowser)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BIS The Castle Depths (Inside Bowser)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Soprano': VOICE_OOHS,
  },
  'BIS The Grand Finale': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BISBJJ Bowser\'s Stolen Castle': {
    'Organ': CHURCH_ORGAN,
  },
  'BISBJJ Forever in the Plains': {
    'Alto': VOICE_OOHS,
    'Soprano': VOICE_OOHS,
  },
  'BISBJJ Meet Me at Wonder Woods (Inside Bowser)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BISBJJ The Castle Depths (Inside Bowser)': {
    'Soprano': VOICE_OOHS,
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BISBJJ The Grand Finale': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'BR Battle! (Sashay)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BR Courtyard Colosseum': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'BR Crystal Colosseum': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'BR Magma Colosseum': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'BR Sunny Park Colosseum': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BR Waterfall Colosseum': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'BW Battle! (Elite Four)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BW Battle! (Gym Leader)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'BW Battle! (Legendary Pokemon)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'C Battle! (Cipher)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'C Battle! (Trainer Battle 2)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'C Battle! (Trainer Battle 3)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'COH Cliffs (Combat)': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'COH Forest (Combat)': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Lead 7': LEAD_2_SAWTOOTH,
  },
  'COH Grassland (Combat)': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Lead 5': LEAD_2_SAWTOOTH,
  },
  'COH Kakariko Crypt (Combat)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'COH Lost Swamp (Combat)': {
    'Electric Guitar 1': ELECTRIC_GUITAR_CLEAN,
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
    'Viola': VIOLA,
    'Cello': CELLO,
  },
  'CS': {
    'Vocals': BREATH_NOISE,
  },
  'CS Black Bowser\'s Castle': {
    'Organ': CHURCH_ORGAN,
  },
  'CS Cherry Lake': {
    'Electric Guitar 1': ELECTRIC_GUITAR_CLEAN,
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
  },
  'CS Fight!': {
    'Synth Lead': LEAD_2_SAWTOOTH
  },
  'CS Island in Violet': {
    'Synth Lead': LEAD_2_SAWTOOTH
  },
  'CS Lemmy\'s Grand Finale': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'CS The Golden Coliseum': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'CS Toad Trainworks': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'CT Black Omen': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'CT Derelict Factory': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'CT Tyranno Lair': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'CT World Revolution': {
    'Organ': CHURCH_ORGAN,
  },
  'CTTT Drop-Road Dash': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'CTTT Piranha Creeper Creek': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'CW Round and Round': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'DL3': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'DL3 Cloudy Park': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Gourmet Race': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'DL3 Grass Land 1': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Grass Land 2': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Grass Land 3': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Grass Land 4': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'DL3 King Dedede\'s Theme': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'DL3 Minigame': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'DL3 Ripple Field Ocean Waves': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Sand Canyon 1': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 Sand Canyon 3': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DL3 The Last Iceberg': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'DPP Battle! (Azelf Mesprit Uxie)': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'DPP Battle! (Dialga Palkia)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'DPP Battle! (Cyrus)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DPP Fight Area (Day)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'DPP Fight Area (Night)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'DPP Stark Mountain': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'DR Pandora Palace': {
    'Synth Voice': BREATH_NOISE,
  },
  'DR Rude Buster': {
    'Electric Guitar 1': ELECTRIC_GUITAR_CLEAN,
  },
  'DR Smart Race': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'DR The World Revolving': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'DR WELCOME TO THE CITY': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'DT Neo Bowser Castle': {
    'Violin I': VIOLIN,
    'Organ': CHURCH_ORGAN,
  },
  'DT Rules on Dreamy Mountain': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'E Battle! (Frontier Brain)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'E Battle! (Mew)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Lead 4': LEAD_2_SAWTOOTH,
  },
  'EB': {
    'Organ': DRAWBAR_ORGAN,
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'FL Invasion at the House of Horrors': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'FL Northeast Frost Street': {
    'Electric Guitar 1': ELECTRIC_GUITAR_CLEAN,
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
  },
  'FL Running Through the New World': {
    'Violin I': VIOLIN,
  },
  'FL Scattered Souls across Isolated Isles': {
    'Violin': VIOLIN,
    'Viola': VIOLA,
    'Cello': CELLO,
  },
  'FL The Battle of Blizzard Bridge': {
    'Electric Piano 1': ELECTRIC_PIANO_2,
    'Electric Piano 2': ELECTRIC_PIANO_2,
  },
  'FL The Battle of Blizzard Bridge (Version 2)': {
    'Electric Piano 1': ELECTRIC_PIANO_2,
    'Electric Piano 2': ELECTRIC_PIANO_2,
  },
  'FL The Wondaria Dream Parade': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'FO CC Level Theme 2': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'FO CC Level Theme 3': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'FO CC Level Theme 4': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FO DB Fruit': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FO DB Swab The Deks': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FO EV Chilblains': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_5_CHARANG,
    'Synth Lead 4': LEAD_2_SAWTOOTH,
  },
  'FO EV Ctrl-Alt-Escape': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_5_CHARANG,
  },
  'FO G Solarium': {
    'Vocals': BREATH_NOISE,
  },
  'FO MD Miner Details': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Organ': DRAWBAR_ORGAN,
  },
  'FO OD Alienate': {
    'Synth Lead 1': SYNTH_BASS_1,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FO OD Gridlock 1': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'FO OD Gridlock 2': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': SYNTH_BASS_1,
  },
  'FO OD Journey to the Center of the Orb': {
    'Synth Lead 1': SYNTH_BASS_1,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FO OD Stronghold': {
    'Synth Lead 1': SYNTH_BASS_1,
  },
  'FO OD Wait Theme 1': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'FO OD Wait Theme 2': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': SYNTH_BASS_1,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FO OD Wait Theme 3': {
    'Synth Lead 1': SYNTH_BASS_1,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FO OD Wave Theme 3': {
    'Synth Lead 1': SYNTH_BASS_1,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Lead 4': LEAD_2_SAWTOOTH,
  },
  'FO SC Level Theme 1': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Pad 1': PAD_6_METALLIC,
    'Zap FX': GUNSHOT,
  },
  'FO SC Space Race': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': SYNTH_BASS_1,
    'Synth Lead 5': LEAD_5_CHARANG,
    'Zap FX 1': GUNSHOT,
    'Zap FX 2': BREATH_NOISE,
    'Zap FX 3': GUNSHOT,
  },
  'FRLG Battle! (Deoxys)': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FRLG Battle! (Gym Leader Battle)': {
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'FRLG Battle! (Legendary Pokemon)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FRLG Battle! (Mewtwo)': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FRLG Battle! (Trainer Battle)': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FRLG Battle! (Wild Pokemon)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'FRLG Final Battle! (Rival)': {
    'Electric Guitar 1': ELECTRIC_GUITAR_CLEAN,
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'FRLG Road to Cerulean City Leaving Mt Moon': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'FRLG Road to Fuschia City Leaving Lavender Town': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'HGSS Azalea Town': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'HGSS SS Aqua': {
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'HGSS Viridian Forest': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'IWBTG Home Sweet Grave': {
    'Synth Lead 1': LEAD_3_CALLIOPE,
    'Synth Lead 2': LEAD_5_CHARANG,
    'Synth Pad 2': PAD_1_NEW_AGE,
    'Vocals': BREATH_NOISE,
  },
  'ITM Rem': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'K64': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'K64 Above the Clouds': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'K64 Boss Battle Theme': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'K64 Gourmet Race': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'K64 Neo Star': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'K64 Pop Star 3': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'K64 Ripple Red': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'K64 Rock Star 1': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'K64 Rock Star 3': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'K64 Shiver Star 1': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'K64 Studying the Factory': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSq': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'KSSq Prism Plains': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSq Tower of Midbosses': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt Boss Battle Theme': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt Candy Mountain': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'KSSt Green Greens': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'KSSt Havoc Aboard the Halberd': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt King Dedede\'s Theme': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'KSSt Maize Hall': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt Mallow Castle': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Violin': VIOLIN,
  },
  'KSSt Orange Ocean': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt Peanut Plain': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'KSSt Sub-Tree': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'LF2': {
    'Organ': CHURCH_ORGAN,
  },
  'LF2 Future Reloaded': {
    'Laser FX': MELODIC_TOM,
  },
  'LF2 Transformed Psycotolonic': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'LGPE Battle! (Master Trainer Battle)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MBG': {
    'Organ': DRAWBAR_ORGAN,
  },
  'MBG Beach Party': {
    'Vocals': BREATH_NOISE,
  },
  'MBP Astrolabe': {
    'Synth Lead': LEAD_5_CHARANG,
  },
  'MBP Endurance': {
    'Synth Lead': LEAD_5_CHARANG,
  },
  'MBP Grudge': {
    'Synth Lead 1': SYNTH_BASS_1,
  },
  'MBP Rising Temper': {
    'Synth Lead 2': SYNTH_BASS_1,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MBP The Race': {
    'Synth Bass': LEAD_1_SQUARE,
    'Zap FX': BREATH_NOISE,
  },
  'MDB': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDB A New Adventure': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDB Battle With Rayquaza': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDB Boss Battle!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDB Great Canyon': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDB It\'s a Thief!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDB Magma Cavern': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDB Makuhita Dojo': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDB Monster House!': {
    'Violin': VIOLIN,
  },
  'MDB Mt Blaze': {
    'Electric Piano': ELECTRIC_PIANO_2,
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDB Mt Steel': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'MDB Mt Thunder': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDB Silent Chasm': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDB Sinister Woods': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Violin I': VIOLIN,
  },
  'MDB Sky Tower': {
    'Synth Bass': LEAD_1_SQUARE,
    'Violin I': VIOLIN,
  },
  'MDB Sky Tower Summit': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDB Stormy Sea': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDB The Escape': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Violin I': VIOLIN,
  },
  'MDB Thunderwave Cave': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDB Tiny Woods': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'MDBSL Grassy Dungeon 1': {
    'Viola': VIOLA,
  },
  'MDGTI': {
    'Organ': DRAWBAR_ORGAN,
  },
  'MDGTI Battling the Boss': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDGTI Come on in to Post Town': {
    'Violin I': VIOLIN,
  },
  'MDGTI Glacial Underpass': {
    'Electric Piano 2': ELECTRIC_PIANO_2,
    'Synth Lead 1': PAD_7_HALO,
    'Synth Lead 2': PAD_6_METALLIC,
  },
  'MDGTI Glacier Palace (Western Spire)': {
    'Synth Pad 2': PAD_8_SWEEP,
  },
  'MDGTI Holehills': {
    'Synth Lead': LEAD_5_CHARANG,
  },
  'MDGTI It\'s a Monster House!': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDGTI Kilionea Road': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDGTI Ragged Mountain': {
    'Violin I': VIOLIN,
    'Viola I': VIOLA,
  },
  'MDGTI Star Cave': {
    'Violin I': VIOLIN,
  },
  'MDGTI Stirrings of Hope': {
    'Electric Piano': ELECTRIC_PIANO_2,
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDGTI Stompstump Peak': {
    'Viola I': VIOLA,
  },
  'MDGTI Stony Cave': {
    'Violin': VIOLIN,
  },
  'MDGTI Stop Thief!': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDGTI Telluric Path': {
    'Synth Lead 3': PAD_7_HALO,
  },
  'MDGTI The Bittercold (First Battle)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDGTI Tyrian Maze': {
    'Electric Piano': ELECTRIC_PIANO_2,
    'Synth Lead 1': PAD_7_HALO,
    'Synth Lead 2': PAD_7_HALO,
  },
  'MDGTI Tyrian Maze (Inner Chamber)': {
    'Synth Lead 1': PAD_7_HALO,
    'Synth Lead 2': PAD_7_HALO,
    'Synth Lead 4': PAD_7_HALO,
  },
  'MDGTI Unlimited Dungeon 1': {
    'Synth Lead': SYNTH_BASS_1,
  },
  'MDR': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDR A New Adventure': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Battle With Rayquaza': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Boss Battle!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Great Canyon': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDR It\'s a Thief!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDR Lapis Cave': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Magma Cavern': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDR Makuhita Dojo': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDR Monster House!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Violin': VIOLIN,
  },
  'MDR Mt Blaze': {
    'Electric Piano': ELECTRIC_PIANO_2,
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Mt Freeze': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR Mt Steel': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'MDR Mt Thunder': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDR Silent Chasm': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDR Sinister Woods': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Violin I': VIOLIN,
  },
  'MDR Sky Tower': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Violin I': VIOLIN,
  },
  'MDR Sky Tower Summit': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDR Stormy Sea': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDR The Escape': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Violin I': VIOLIN,
  },
  'MDR Thunderwave Cave': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDR Tiny Woods': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDRTDX': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDRTDX A New Adventure': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDRTDX Battle With Rayquaza': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Boss Battle!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Frosty Forest': {
    'Synth Pad 2': PAD_2_WARM,
  },
  'MDRTDX Great Canyon': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDRTDX It\'s a Thief!': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Magma Cavern': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Makuhita Dojo': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Monster House!': {
    'Violin': VIOLIN,
  },
  'MDRTDX Mt Blaze': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDRTDX Mt Steel': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Synth Lead 1': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Mt Thunder': {
    'Synth Bass': LEAD_2_SAWTOOTH,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Oddity Cave': {
    'Synth Bass': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Sinister Woods': {
    'Violin I': VIOLIN,
  },
  'MDRTDX Sky Tower': {
    'Synth Bass': LEAD_1_SQUARE,
    'Violin I': VIOLIN,
  },
  'MDRTDX Sky Tower Summit': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDRTDX Stormy Sea': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDRTDX The Escape': {
    'Synth Bass': LEAD_1_SQUARE,
    'Violin I': VIOLIN,
  },
  'MDRTDX Thunderwave Cave': {
    'Synth Bass': LEAD_1_SQUARE,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'MDS': PMD_EXPLORERS_MIDI_INSTRUMENT_OVERRIDES,
  'MDS Barren Valley': {
    'Violin': VIOLIN,
    'Viola': VIOLA,
  },
  'MDS Dark Ice Mountain': {
    'Violin I': VIOLIN,
  },
  'MDS Dark Wasteland': {
    'Violin I': VIOLIN,
  },
  'MDS Fortune Ravine': {
    'Violin I': VIOLIN,
  },
  'MDS Murky Forest': {
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDS Random Dungeon Theme 3': {
    'Trombone': TRUMPET,
  },
  'MDS Sky Peak Cave': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDS Sky Peak Coast': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'MDS Sky Peak Forest': {
    'Violin I': VIOLIN,
  },
  'MDS Sky Peak Prairie': {
    'Violin I': VIOLIN,
  },
  'MDS Spacial Cliffs': {
    'Violin I': VIOLIN,
    'Viola I': VIOLA,
    'Cello': CELLO,
  },
  'MDS Spring Cave': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDS Star Cave': {
    'Violin I': VIOLIN,
  },
  'MDS Vast Ice Mountain': {
    'Violin I': VIOLIN,
  },
  'MDTDS': PMD_EXPLORERS_MIDI_INSTRUMENT_OVERRIDES,
  'MDTDS Aegis Cave': {
    'Violin I': VIOLIN,
  },
  'MDTDS Amp Plains': {
    'Synth Pad': LEAD_2_SAWTOOTH,
  },
  'MDTDS Battle against Dusknoir': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Beach Cave': {
    'Synth Pad': PAD_2_WARM,
  },
  'MDTDS Blizzard Island Rescue Team Medley': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'MDTDS Boss Battle!': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Chasm Cave': {
    'Violin I': VIOLIN,
  },
  'MDTDS Dialga\'s Fight to the Finish!': {
    'Double Bass': CONTRABASS,
    'Violin I': VIOLIN,
  },
  'MDTDS Far Amp Plains': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Pad': LEAD_2_SAWTOOTH,
  },
  'MDTDS Guildmaster Wigglytuff': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Hidden Highland': {
    'Viola I': VIOLA,
  },
  'MDTDS Monster House!': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Mt Horn': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Northern Desert': {
    'Cello': CELLO,
    'Viola': VIOLA,
    'Violin III': VIOLIN,
  },
  'MDTDS Palkia\'s Onslaught!': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Temporal Spire': {
    'Cello II': CELLO,
    'Double Bass': CONTRABASS,
  },
  'MDTDS Through the Sea of Time': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MDTDS Time Gear': {
    'Violin': VIOLIN,
  },
  'MDTDS Wigglytuff\'s Guild': {
    'Violin I': VIOLIN,
  },
  'MK8 Big Blue': {
    'Organ': ROCK_ORGAN,
  },
  'MK8 Big Blue (Final Lap)': {
    'Organ': ROCK_ORGAN,
  },
  'MK8 Tick Tock Clock': {
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Zap FX': BREATH_NOISE,
  },
  'MK8 Tick Tock Clock (Final Lap)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Zap FX': BREATH_NOISE,
  },
  'MK8 Wild Woods': {
    'Violin': VIOLIN,
  },
  'MK8 Wild Woods (Final Lap)': {
    'Violin': VIOLIN,
  },
  'MK8D Choco Mountain': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
  },
  'MK8D Choco Mountain (Final Lap)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
  },
  'MK8D Sky Garden': {
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
  },
  'MK8D Sky Garden (Final Lap)': {
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
  },
  'MKDS': {
    'Electric Piano': ELECTRIC_PIANO_2,
  },
  'MKDS Choco Mountain': {
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
  },
  'MKDS Choco Mountain (Final Lap)': {
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
  },
  'MKDS Tick Tock Clock': {
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Zap FX': BREATH_NOISE,
  },
  'MKDS Tick Tock Clock (Final Lap)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Zap FX': BREATH_NOISE,
  },
  'MKDS Waluigi Pinball': {
    'Organ': ROCK_ORGAN,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MKDS Waluigi Pinball (Final Lap)': {
    'Organ': ROCK_ORGAN,
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'MLSSBM Decisive Battleground': {
    'Violin I': VIOLIN,
  },
  'MPDS': {
    'Electric Piano': ELECTRIC_PIANO_2,
    'Organ': ROCK_ORGAN,
  },
  'MRKB': {
    'Organ': CHURCH_ORGAN,
  },
  'Pt Battle! (Frontier Brain)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'Pt Battle! (Giratina)': {
    'Synth Lead': LEAD_2_SAWTOOTH,
  },
  'SMD Abyssal Badlands': {
    'Synth Lead': LEAD_2_SAWTOOTH,
    'Violin': VIOLIN,
  },
  'SMD Air Continent Baram Town': {
    'Cello': CELLO,
    'Violin': VIOLIN,
  },
  'SMD Amp Plains': {
    'Synth Lead 2': LEAD_2_SAWTOOTH,
    'Synth Lead 3': LEAD_2_SAWTOOTH,
  },
  'SMD Boss Battle Children\'s Adventure!': {
    'Synth Bass': LEAD_1_SQUARE,
  },
  'SMD Boss Battle Expedition Society Fight': {
    'Organ': ROCK_ORGAN,
    'Synth Pad': SYNTH_BRASS_1,
  },
  'SMD Boss Battle with Great Powers!': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'SMD Fire Island Volcano': {
    'Violin I': VIOLIN,
    'Violin II': VIOLIN,
    'Viola I': VIOLA,
  },
  'SMD Legendary Boss Battle Rock Version!': {
    'Synth Lead': LEAD_5_CHARANG,
  },
  'SMD Oh No! This is Bad!': {
    'Cello': CELLO,
  },
  'SMD Sand Dune of Spirits': {
    'Synth Lead 1': LEAD_2_SAWTOOTH,
    'Synth Lead 2': LEAD_2_SAWTOOTH,
  },
  'SMD Second Dark Matter Battle': {
    'Violin': VIOLIN,
  },
  'SMD Showdown with a Volcanic Entei!': {
    'Violin': VIOLIN,
  },
}

def get_instrument_name(orig_instrument_name: str):
  return re.sub(r' [\dIV]{1,3}$', '', orig_instrument_name)

def get_mapped_program(game_acronym: str, full_file_name: str, instrument_name: str, orig_instrument_name: str):
  if game_acronym in midi_instrument_overrides:
    game_instrument_overrides = midi_instrument_overrides[game_acronym]
  else:
    game_instrument_overrides = {}
  if full_file_name in midi_instrument_overrides:
    instrument_overrides = midi_instrument_overrides[full_file_name]
  else:
    instrument_overrides = {}

  if orig_instrument_name in instrument_overrides:
    return instrument_overrides[orig_instrument_name]
  elif instrument_name in game_instrument_overrides:
    return game_instrument_overrides[instrument_name]
  elif instrument_name in midi_instruments:
    return midi_instruments[instrument_name]
  return None

def get_transpose_offset(game_acronym: str, current_program: int, track_name: str, instrument_name: str, orig_instrument_name: str):
  transpose_offset = 0
  if game_acronym in program_transpose:
    current_program_transpose = program_transpose[game_acronym]
    if current_program in current_program_transpose:
      transpose_offset = current_program_transpose[current_program]
      if not isinstance(transpose_offset, int):
        if track_name in transpose_offset:
          transpose_offset = transpose_offset[track_name]
          if not isinstance(transpose_offset, int):
            if orig_instrument_name in transpose_offset:
              transpose_offset = transpose_offset[orig_instrument_name]
            else:
              transpose_offset = 0
        elif instrument_name in transpose_offset:
          transpose_offset = transpose_offset[instrument_name]
        elif DEFAULT_TRACK in transpose_offset:
          transpose_offset = transpose_offset[DEFAULT_TRACK]
        else:
          transpose_offset = 0
  if current_program == WOODBLOCK and transpose_offset == 0:
    return 12
  if current_program == CHURCH_ORGAN:
    transpose_offset -= 12
  return transpose_offset

def get_percussion_mapping(game_acronym: str, track_name: str, instrument_name: str, current_note: str) -> int:
  parts_override = None
  combined_name = game_acronym + ' ' + track_name
  if game_acronym in percussion_parts_override:
    parts_override = percussion_parts_override[game_acronym]
  elif combined_name in percussion_parts_override:
    parts_override = percussion_parts_override[combined_name]
  if parts_override is not None:
    mapping = get_percussion_mapping_from_parts(instrument_name, current_note, parts_override)
    if mapping is not None:
      return mapping

  return get_percussion_mapping_from_parts(instrument_name, current_note, percussion_parts)

def get_percussion_mapping_from_parts(instrument_name: str, current_note: str, parts: Dict[str, Dict[int, int]]) -> int:
  if instrument_name in parts:
    mapping = parts[instrument_name]
    if isinstance(mapping, int):
      return parts[instrument_name]
    elif mapping is not None and current_note in mapping:
      return mapping[current_note]
    elif current_note == CRASH_CYMBAL_2:
      return CRASH_CYMBAL_1
  return None

@dataclass
class PercussionSequencePart:
  notes: Set[int] = field(default_factory=set)
  note_mapping: Dict[int, int] = field(default_factory=dict)
  messages: List = field(default_factory=list)

def fill_percussion_sequence_parts(instrument_name: str, current_note: int, message, percussion_sequence_parts: Dict[str, PercussionSequencePart]):
  sequence_part = percussion_sequence_parts[instrument_name]
  sequence_part.notes.add(current_note)
  sequence_part.messages.append(message)

def map_percussion_sequence_note(instrument_name: str, current_note: int, sequence_part: PercussionSequencePart) -> int:
  if len(sequence_part.note_mapping) == 0:
    num_notes = len(sequence_part.notes)
    if num_notes not in percussion_sequence_mappings[instrument_name]:
      print('Percussion sequence length {} not found for {}.'.format(num_notes, instrument_name))
      return get_percussion_mapping_from_parts(instrument_name, current_note, percussion_parts)

    percussion_sequence_mapping = percussion_sequence_mappings[instrument_name][num_notes]
    if instrument_name in percussion_sequence_orders:
      percussion_sequence_order = percussion_sequence_orders[instrument_name]
      sorted_notes = sorted(sequence_part.notes, key=percussion_sequence_order.index)
    else:
      sorted_notes = sorted(sequence_part.notes)
    for i, note in enumerate(sorted_notes):
      sequence_part.note_mapping[note] = percussion_sequence_mapping[i]

  return sequence_part.note_mapping[current_note]
