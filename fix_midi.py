from mido import MidiFile
from general_midi import *
import os;
import re;

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
  'Mandolin': ACOUSTIC_GUITAR_NYLON,
  'Ukulele': ACOUSTIC_GUITAR_NYLON,
  'Muted Electric Guitar': ELECTRIC_GUITAR_MUTED,
  'Electric Guitar': ELECTRIC_GUITAR_DISTORTION,
  'Electric Bass': ELECTRIC_BASS_FINGER,
  'Electric Bass (Slap)': SLAP_BASS_1,
  'Slap Bass': SLAP_BASS_1,
  'Synth Bass': SYNTH_BASS_1,
  'Harp': ORCHESTRAL_HARP,
  'Timpani': TIMPANI,
  'Violin': STRING_ENSEMBLE_1,
  'Viola': STRING_ENSEMBLE_1,
  'Cello': STRING_ENSEMBLE_1,
  'Double Bass': STRING_ENSEMBLE_1,
  'Alto': CHOIR_AAHS,
  'Baritone': CHOIR_AAHS,
  'Bass': CHOIR_AAHS,
  'Choir': CHOIR_AAHS,
  'Laugh FX': CHOIR_AAHS,
  'Soprano': CHOIR_AAHS,
  'Tenor': CHOIR_AAHS,
  'Voice': VOICE_OOHS,
  'Vocals': VOICE_OOHS,
  'Synth Voice': SYNTH_VOICE,
  'Orchestra Hit': ORCHESTRA_HIT,
  'Trumpet': TRUMPET,
  'Muted Trombone': TROMBONE,
  'Trombone': TROMBONE,
  'Euphonium': TUBA,
  'Tuba': TUBA,
  'Muted Trumpet': MUTED_TRUMPET,
  'Flugelhorn': FRENCH_HORN,
  'Horn': FRENCH_HORN,
  'Synth Brass': SYNTH_BRASS_1,
  'Soprano Sax': SOPRANO_SAX,
  'Alto Sax': ALTO_SAX,
  'Tenor Sax': TENOR_SAX,
  'Oboe': OBOE,
  'English Horn': ENGLISH_HORN,
  'Bassoon': BASSOON,
  'Contrabassoon': BASSOON,
  'Didgeridoo': BASSOON,
  'Clarinet': CLARINET,
  'Piccolo': PICCOLO,
  'Alto Flute': FLUTE,
  'Flute': FLUTE,
  'Alto Recorder': RECORDER,
  'Soprano Recorder': RECORDER,
  'Fife': PAN_FLUTE,
  'Pan Flute': PAN_FLUTE,
  'Tin Whistle': PAN_FLUTE,
  'Synth Lead': LEAD_1_SQUARE,
  'Synth Pad': PAD_1_NEW_AGE,
  'Sound FX': FX_1_RAIN,
  'Squeak FX': FX_4_ATMOSPHERE,
  'Wind FX': FX_4_ATMOSPHERE,
  'Static FX': FX_7_ECHOES,
  'Zap FX': FX_7_ECHOES,
  'Sitar': SITAR,
  'Banjo': BANJO,
  'Kalimba': KALIMBA,
  'Bagpipes': BAGPIPE,
  'Steel Drums': STEEL_DRUMS,
}

percussion_parts = {
  'Agogo Bells': {
    58: HIGH_AGOGO,
    60: LOW_AGOGO
  },
  'Bass Drum': ACOUSTIC_BASS_DRUM,
  'Bell': RIDE_BELL,
  'Bodhr\x87n': LOW_BONGO,
  'Bongo Drums': {
    45: LOW_BONGO,
    47: LOW_BONGO,
    48: HIGH_BONGO,
    50: HIGH_BONGO,
    60: HIGH_BONGO,
    61: LOW_BONGO
  },
  'Cabasa': CABASA,
  'Castanets': CASTANETS,
  'Clap': HAND_CLAP,
  'Claves': CLAVES,
  'Click FX': CASTANETS,
  'Conga Drums': {
    54: LOW_CONGA,
    55: OPEN_HIGH_CONGA,
    61: OPEN_HIGH_CONGA,
    63: OPEN_HIGH_CONGA,
    64: LOW_CONGA,
    75: LOW_CONGA,
  },
  'Cowbell': COWBELL,
  'Crash Cymbal': CRASH_CYMBAL_1,
  'Drum Set': None,
  'Field Drum': ACOUSTIC_SNARE,
  'Finger Cymbals': OPEN_TRIANGLE,
  'Floor Tom': {
    42: LOW_FLOOR_TOM,
    66: LOW_FLOOR_TOM
  },
  'Goblet Drum': {
    58: LOW_CONGA,
    60: OPEN_HIGH_CONGA
  },
  'Guiro': LONG_GUIRO,
  'Hand Castanets': CASTANETS,
  'Hi-Hat Cymbal': {
    42: CLOSED_HI_HAT,
    44: PEDAL_HI_HAT,
    46: OPEN_HI_HAT,
    89: CLOSED_HI_HAT
  },
  'Kick Drum': ACOUSTIC_BASS_DRUM,
  'Machine Castanets': CASTANETS,
  'Maracas': MARACAS,
  'Ratchet': LONG_GUIRO,
  'Ride Cymbal': {
    92: RIDE_CYMBAL_1,
    93: RIDE_BELL
  },
  'Sand Block': CABASA,
  'Scratching': CABASA,
  'Shaker': SHAKER,
  'Sleigh Bells': JINGLE_BELL,
  'Snare Drum': {
    36: ACOUSTIC_SNARE,
    59: ACOUSTIC_SNARE,
    60: ACOUSTIC_SNARE
  },
  'Splash Cymbal': SPLASH_CYMBAL,
  'Static FX': CASTANETS,
  'Suspended Cymbal': CRASH_CYMBAL_1,
  'Tambourine': TAMBOURINE,
  'Tamtam': CHINESE_CYMBAL,
  'Temple Blocks': {
    36: LOW_WOODBLOCK,
    47: LOW_WOODBLOCK,
    57: LOW_WOODBLOCK,
    63: HIGH_WOODBLOCK,
    70: HIGH_WOODBLOCK,
    76: HIGH_WOODBLOCK,
    77: LOW_WOODBLOCK,
  },
  'Timbales': {
    65: HIGH_TIMBALE,
    66: LOW_TIMBALE,
    70: LOW_TIMBALE,
    71: HIGH_TIMBALE,
    72: LOW_TIMBALE
  },
  'Toms': {
    42: LOW_TOM,
    43: LOW_MID_TOM,
    44: LOW_MID_TOM,
    46: HI_MID_TOM,
    48: LOW_TOM,
    52: LOW_TOM,
    55: LOW_MID_TOM,
    59: LOW_MID_TOM,
    62: HI_MID_TOM,
    65: HI_MID_TOM,
    68: LOW_MID_TOM,
    69: HIGH_TOM,
    70: HI_MID_TOM,
    72: HIGH_TOM
  },
  'Triangle': {
    80: MUTE_TRIANGLE,
    81: OPEN_TRIANGLE,
    82: OPEN_TRIANGLE
  },
  'VibraSlap': VIBRASLAP,
  'Whip': SLAP_NOISE,
  'Wind Chimes': BELL_TREE,
  'Wood Block': HIGH_WOODBLOCK,
  'Wood Blocks': {
    62: HIGH_WOODBLOCK,
    63: LOW_WOODBLOCK
  }
}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
overwrite = True
new_file_location = 'Modified'
game_acronym = 'MDTDS'
game_name = 'Pokemon Mystery Dungeon Explorers of Time Darkness'
track_names = [
  'Sealed Ruin Pit'
]

for track_name in track_names:
  if type(track_name) is tuple:
    short_name = track_name[1]
    track_name = track_name[0]
  else:
    short_name = track_name

  short_name = '{} {}'.format(game_acronym, short_name)
  long_name = '{} ({})'.format(track_name, game_name)

  file_name = '{}.midi'.format(long_name)
  file_location = os.path.join(parts_folder, short_name, file_name)
  new_file_name = file_name
  # file_name = '{}.midi'.format(short_name)
  # file_location = os.path.join(parts_folder, file_name)
  # new_file_name = '{}.midi'.format(long_name)

  mid = MidiFile(file_location)
  for i, track in enumerate(mid.tracks):
    track_name = track.name
    if len(track_name) == 0:
      continue

    track_name = re.sub(r' [\dIV]{1,3}$', '', track_name)

    percussion = track_name in percussion_parts
    for msg in track:
      if percussion and hasattr(msg, 'channel'):
        msg.channel = 9
        if msg.type == 'note_on' or msg.type == 'note_off':
          if percussion_parts[track_name] is not None:
            mapping = percussion_parts[track_name]
            if isinstance(mapping, int):
              msg.note = percussion_parts[track_name]
            else:
              if msg.note in mapping:
                msg.note = mapping[msg.note]
              else:
                print('Encountered unmapped percussion note:', track.name, msg.note)
      elif msg.type == 'program_change':
        if msg.program == 45:
          # Pizzicato strings
          msg.program = 46
        elif track_name in midi_instruments:
          msg.program = midi_instruments[track_name]
        else:
          print('Encountered unmapped track:', track_name)
  if overwrite:
    new_file_path = file_location
  else:
    new_file_path = os.path.join(new_file_location, new_file_name)
  print('Saving file to', new_file_path)
  mid.save(new_file_path)
