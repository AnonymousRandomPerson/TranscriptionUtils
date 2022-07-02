from general_midi import *
import re
from typing import Dict, List, Set
from dataclasses import dataclass, field

midi_instruments = {
  'Piano': ACOUSTIC_GRAND_PIANO,
  'Electric Piano': ELECTRIC_PIANO_2,
  'Harpsichord': HARPSICHORD,
  'Clavinet': CLAVINET,
  'Celesta': CELESTA,
  'Cowbell (Autotune)': CELESTA,
  'Glass Harmonica': CELESTA,
  'Crotales': GLOCKENSPIEL,
  'Glockenspiel': GLOCKENSPIEL,
  'Music Box': MUSIC_BOX,
  'Bonang': VIBRAPHONE,
  'Cowbell (Auto-tune)': VIBRAPHONE,
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
  'Muted Electric Bass': ELECTRIC_BASS_FINGER,
  'Electric Bass (Slap)': SLAP_BASS_1,
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
  'Choir': CHOIR_AAHS,
  'Choir Aahs': CHOIR_AAHS,
  'Contralto': CHOIR_AAHS,
  'Laugh FX': CHOIR_AAHS,
  'Soprano': CHOIR_AAHS,
  'Tenor': CHOIR_AAHS,
  'Choir Oohs': VOICE_OOHS,
  'Kirby Voice': VOICE_OOHS,
  'Voice': VOICE_OOHS,
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
  'Tenor Trombone': TROMBONE,
  'Trombone': TROMBONE,
  'Euphonium': TUBA,
  'Tuba': TUBA,
  'Muted Trumpet': MUTED_TRUMPET,
  'Trumpet (Muted)': MUTED_TRUMPET,
  'Flugelhorn': TRUMPET,
  'Alto Horn': FRENCH_HORN,
  'French Horn': FRENCH_HORN,
  'Horn': FRENCH_HORN,
  'Synth Brass': SYNTH_BRASS_1,
  'Soprano Sax': SOPRANO_SAX,
  'Alto Sax': ALTO_SAX,
  'Tenor Sax': TENOR_SAX,
  'Baritone Sax': BARITONE_SAX,
  'Oboe': OBOE,
  'Pungi': OBOE,
  'Rhaita': OBOE,
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
  'Bottle Blow': BLOWN_BOTTLE,
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
  'Steel Drums': STEEL_DRUMS,
  'Temple Blocks': WOODBLOCK,
  'Melodic Tom': MELODIC_TOM,
  'Compressed Air FX': BREATH_NOISE,
  'Fire FX': BREATH_NOISE,
  'Noise FX': BREATH_NOISE,
  'Sound FX': BREATH_NOISE,
  'Whoosh FX': BREATH_NOISE,
  'Wind FX': BREATH_NOISE,
  'Bubble FX': SEASHORE,
  'Rustling FX': SEASHORE,
  'Boing': BIRD_TWEET,
  'Laser FX': BIRD_TWEET,
  'Screech FX': BIRD_TWEET,
  'Squeak FX': BIRD_TWEET,
  'Electric Bell': TELEPHONE_RING,
  'Drill FX': HELICOPTER,
  'Engine FX': HELICOPTER,
  'Machine FX': HELICOPTER,
  'Sweep FX': HELICOPTER,
  'Zap FX': HELICOPTER,
  'Cymbal FX': GUNSHOT,
  'Gun Shot FX': GUNSHOT,
  'Gunshot': GUNSHOT,
  'Metal Bang FX': GUNSHOT,
  'Piano Slam': GUNSHOT,
  'Rock Hit FX': GUNSHOT,
}

mxl_instruments = {
  BIRD_TWEET: 'effect.bird.tweet',
  BREATH_NOISE: 'effect.breath',
  ELECTRIC_GUITAR_DISTORTION: '',
  GUNSHOT: 'effect.gunshot',
  HELICOPTER: 'effect.helicopter',
  PERCUSSIVE_ORGAN: 'keyboard.organ.percussive',
  SEASHORE: 'effect.seashore',
  SLAP_BASS_1: 'effect.bass-string-slap',
  TELEPHONE_RING: 'effect.telephone-ring',
  VOICE_OOHS: 'voice.oo',
  WOODBLOCK: '',
}

mxl_percussion_override = {
  'Tsuzumi': HIGH_BONGO,
}

mxl_percussion_to_non_percussion = set([
  'Temple Blocks',
])

mxl_manual_remap = set([
  'Bonang',
  'Gend\x8er',
  'Wind Chimes',
])

CRASH_CYMBAL_MAPPING = {
  84: CRASH_CYMBAL_1,
  87: CRASH_CYMBAL_1,
  89: PEDAL_HI_HAT,
}

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
  'Clock Tick': SIDE_STICK,
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
  'Crash Cymbal': CRASH_CYMBAL_MAPPING,
  'Crash Cymbals': CRASH_CYMBAL_MAPPING,
  'Cu\x92ca': OPEN_CUICA,
  'Cuíca': OPEN_CUICA,
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
  'Frame Drum': LOW_BONGO,
  'Goblet Drum': {
    58: LOW_CONGA,
    60: OPEN_HIGH_CONGA,
  },
  'Guiro': LONG_GUIRO,
  'Hand Castanets': CASTANETS,
  'Hand Drum': LOW_BONGO,
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
    41: LOW_TOM,
    48: LOW_MID_TOM,
  },
  'Ratchet': LONG_GUIRO,
  'Ride Cymbal': {
    92: RIDE_CYMBAL_1,
    93: RIDE_BELL,
  },
  'Sand Block': CABASA,
  'Scratching': CABASA,
  'Shaker': SHAKER,
  'Shime-daiko': {
    45: LOW_MID_TOM,
    47: HI_MID_TOM,
    48: HIGH_TOM,
  },
  'Sleigh Bells': JINGLE_BELL,
  'Snap': HAND_CLAP,
  'Snare Drum': ACOUSTIC_SNARE,
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
    93: CRASH_CYMBAL_1,
    94: RIDE_BELL,
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

percussion_sequence_mappings = {
  'Bongo Drums': {
    1: [HIGH_BONGO],
    2: [LOW_BONGO, HIGH_BONGO],
    3: [OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    4: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    5: [LOW_CONGA, MUTE_HIGH_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
  },
  'Conga Drums': {
    1: [OPEN_HIGH_CONGA],
    2: [LOW_CONGA, OPEN_HIGH_CONGA],
    3: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO],
    4: [LOW_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    5: [LOW_CONGA, MUTE_HIGH_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    6: [LOW_CONGA, MUTE_HIGH_CONGA, OPEN_HIGH_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
    7: [LOW_CONGA, LOW_CONGA, MUTE_HIGH_CONGA, OPEN_HIGH_CONGA, OPEN_HIGH_CONGA, LOW_BONGO, HIGH_BONGO],
  },
  'Toms': {
    1: [LOW_MID_TOM],
    2: [LOW_MID_TOM, HI_MID_TOM],
    3: [LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    4: [LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    5: [HIGH_FLOOR_TOM, LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
    6: [LOW_FLOOR_TOM, HIGH_FLOOR_TOM, LOW_TOM, LOW_MID_TOM, HI_MID_TOM, HIGH_TOM],
  },
  'Triangle': {
    1: [OPEN_TRIANGLE],
    2: [MUTE_TRIANGLE, OPEN_TRIANGLE],
  },
}

percussion_sequence_orders = {
  'Bongo Drums': [47, 46, 45, 48, 49, 50, 60, 61],
  'Conga Drums': [73, 76, 75, 54, 55, 57, 61, 63, 64]
}

percussion_parts_override = {
}

ignore_unmapped_percussion = set([
  'ARIA Player',
  'Drum Set',
])

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
    ELECTRIC_PIANO_2: 12,
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
  'DPP': {
    CHOIR_AAHS: 12,
    TUBULAR_BELLS: 12
  },
  'EB': {
    CELESTA: 12,
  },
  'FL': {
    VIBRAPHONE: {
      'Burning, Churning Power Plant': -36,
    },
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
      'Battle! (Gym Leader - Kanto Version)': 0,
      'Battle! (Ho-Oh)': {
        'Timpani 1': 0,
        'Timpani 2': -12,
      },
      'Battle! (Lugia))': {
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
    BLOWN_BOTTLE: 24,
    CLARINET: 24,
    ELECTRIC_BASS_FINGER: 24,
    LEAD_1_SQUARE: 24,
    MARIMBA: 24,
    ORCHESTRA_HIT: 36,
    PAD_1_NEW_AGE: 24,
    PAN_FLUTE: 24,
    STEEL_DRUMS: 36,
    STRING_ENSEMBLE_1: 24,
    SYNTH_BRASS_1: 24,
    TIMPANI: 36,
    TRUMPET: 36,
    VOICE_OOHS: 24,
  },
  'KSSt': {
    ELECTRIC_BASS_FINGER: -12,
    LEAD_1_SQUARE: {
      'Candy Mountain': 12,
    },
    ORCHESTRA_HIT: 12,
    PAN_FLUTE: 12,
    PICCOLO: {
      DEFAULT_TRACK: 12,
      'Candy Mountain': 24,
    },
    STRING_ENSEMBLE_1: 12,
    SYNTH_BASS_1: -12,
    TRUMPET: 12,
    VOICE_OOHS: {
      DEFAULT_TRACK: 12,
      'Candy Mountain': 0,
    },
  },
  'LTTP': {
    TIMPANI: -12,
  },
  'MDB': {
    BASSOON: -12,
    CELESTA: 12,
    CHOIR_AAHS: {
      'Great Canyon': -12,
      'Mt Blaze': -12,
      'Sky Tower': -12,
      'The Escape': -12,
    },
    PAN_FLUTE: 12,
    PERCUSSIVE_ORGAN: {
      DEFAULT_TRACK: 12,
      'Battle With Rayquaza': 24,
    },
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'It\'s a Thief': 0,
      'Monster House': 0,
      'Oddity Cave': 0,
      'The Escape': 0,
    },
    SYNTH_BASS_1: {
      'Lapis Cave': -12,
      'Magma Cavern': -12,
      'Makuhita Dojo': -24,
      'Monster House': -12,
      'Mt Freeze': -12,
      'Mt Steel': -12,
      'Silent Chasm': -12,
      'Tiny Woods': -12,
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
    PAN_FLUTE: 12,
    PERCUSSIVE_ORGAN: {
      DEFAULT_TRACK: 12,
      'Battle With Rayquaza': 24,
    },
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'It\'s a Thief': 0,
      'Monster House': 0,
      'Oddity Cave': 0,
      'The Escape': 0,
    },
    SYNTH_BASS_1: {
      'Lapis Cave': -12,
      'Magma Cavern': -12,
      'Makuhita Dojo': -24,
      'Monster House': -12,
      'Mt Freeze': -12,
      'Mt Steel': -12,
      'Silent Chasm': -12,
      'Tiny Woods': -12,
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
    STRING_ENSEMBLE_1: {
      DEFAULT_TRACK: 12,
      'It\'s a Thief': 0,
      'Monster House': 0,
      'Oddity Cave': 0,
      'The Escape': 0,
    },
    SYNTH_BASS_1: {
      'Lapis Cave': -12,
      'Magma Cavern': -12,
      'Makuhita Dojo': -24,
      'Monster House': -12,
      'Mt Freeze': -12,
      'Mt Steel': -12,
      'Silent Chasm': -12,
      'Tiny Woods': -12,
    },
  },
  'MDS': {
    STRING_ENSEMBLE_1: {
      'Murky Forest': 12,
      'Sky Peak Cave': 12,
      'Sky Peak Coast': 12,
      'Spring Cave': 12,
    },
    SYNTH_BASS_1: {
      'Dark Wasteland': -12,
    },
  },
  'MLSS': {
    ELECTRIC_BASS_FINGER: -12,
    STEEL_DRUMS: 12,
    TUBA: -24,
  },
  'MLSSBM': {
    ELECTRIC_BASS_FINGER: {
      DEFAULT_TRACK: -12,
      'Sweet Surfin\'': 0,
    },
    STEEL_DRUMS: 12,
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

midi_instrument_overrides = {
  'B2W2 Virbank City': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
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
    'Choir': VOICE_OOHS,
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'BISBJJ Bowser\'s Stolen Castle': {
    'Organ': CHURCH_ORGAN,
  },
  'BISBJJ Meet Me at Wonder Woods (Inside Bowser)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'CS Cherry Lake': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'DPP Fight Area (Day)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'DPP Fight Area (Night)': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'HGSS Azalea Town': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'HGSS SS Aqua': {
    'Electric Guitar 2': ELECTRIC_GUITAR_CLEAN,
  },
  'HGSS Viridian Forest': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'ITM Rem': {
    'Electric Guitar': ELECTRIC_GUITAR_CLEAN,
  },
  'K64': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'KSSq': {
    'Synth Pad': PAD_1_NEW_AGE,
  },
  'MDB': {
    'Celesta': PAD_1_NEW_AGE,
  },
  'MDB Stormy Sea': {
    'Violin I': PIZZICATO_STRINGS,
  },
  'MDB Thunderwave Cave': {
    'Violin I': PIZZICATO_STRINGS,
  },
  'MDR': {
    'Celesta': PAD_1_NEW_AGE,
  },
  'MDS': {
    'Celesta': PAD_1_NEW_AGE,
  },
  'MDTDS': {
    'Celesta': PAD_1_NEW_AGE,
  },
  'MRKB': {
    'Organ': CHURCH_ORGAN,
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

def get_transpose_offset(game_acronym: str, current_program: int, track_name: str, orig_instrument_name: str):
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
