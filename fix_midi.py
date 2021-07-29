from mido import MidiFile
import os;
import re;

midi_instruments = {
  'Piano': 1,
  'Electric Piano': 6,
  'Harpsichord': 7,
  'Clavinet': 8,
  'Celesta': 9,
  'Glass Harmonica': 9,
  'Crotales': 10,
  'Glockenspiel': 10,
  'Music Box': 11,
  'Bonang': 12,
  'Handbells': 12,
  'Vibraphone': 12,
  'Balafon': 13,
  'Marimba': 13,
  'Saron': 14,
  'Xylophone': 14,
  'Chimes': 15,
  'Dulcimer': 16,
  'Organ': 18,
  'Accordion': 22,
  'Harmonica': 23,
  'Acoustic Guitar': 25,
  'Mandolin': 25,
  'Ukulele': 25,
  'Muted Electric Guitar': 29,
  'Electric Guitar': 31,
  'Electric Bass': 34,
  'Electric Bass (Slap)': 37,
  'Slap Bass': 37,
  'Synth Bass': 39,
  'Harp': 47,
  'Timpani': 48,
  'Violin': 49,
  'Viola': 49,
  'Cello': 49,
  'Double Bass': 49,
  'Alto': 53,
  'Baritone': 53,
  'Bass': 53,
  'Choir': 53,
  'Laugh FX': 53,
  'Soprano': 53,
  'Tenor': 53,
  'Vocals': 54,
  'Orchestra Hit': 56,
  'Trumpet': 57,
  'Muted Trombone': 58,
  'Trombone': 58,
  'Muted Trumpet': 60,
  'Euphonium': 70,
  'Tuba': 59,
  'Flugelhorn': 61,
  'Horn': 61,
  'Synth Brass': 63,
  'Soprano Sax': 65,
  'Alto Sax': 66,
  'Tenor Sax': 67,
  'Oboe': 69,
  'English Horn': 70,
  'Bassoon': 71,
  'Contrabassoon': 71,
  'Didgeridoo': 71,
  'Clarinet': 72,
  'Piccolo': 73,
  'Alto Flute': 74,
  'Flute': 74,
  'Soprano Recorder': 75,
  'Fife': 76,
  'Pan Flute': 76,
  'Tin Whistle': 76,
  'Synth Lead': 81,
  'Synth Pad': 89,
  'Sound FX': 97,
  'Wind FX': 100,
  'Static FX': 103,
  'Sitar': 105,
  'Kalimba': 109,
  'Bagpipes': 110,
  'Steel Drums': 115,
}

percussion_parts = {
  'Agogo Bells': {
    58: 67,
    60: 68
  },
  'Bass Drum': 35,
  'Bell': 53,
  'Bodhr\x87n': 61,
  'Bongo Drums': {
    45: 61,
    47: 61,
    48: 60,
    50: 60,
    60: 60
  },
  'Cabasa': 69,
  'Castanets': 85,
  'Clap': 39,
  'Claves': 75,
  'Click FX': 85,
  'Conga Drums': {
    54: 64,
    55: 63,
    61: 63,
    63: 63,
    64: 64,
    75: 64,
  },
  'Cowbell': 56,
  'Crash Cymbal': 49,
  'Drum Set': None,
  'Field Drum': 38,
  'Finger Cymbals': 81,
  'Floor Tom': {
    42: 41,
    66: 41
  },
  'Goblet Drum': {
    58: 64,
    60: 63
  },
  'Guiro': 74,
  'Hand Castanets': 85,
  'Hi-Hat Cymbal': {
    42: 42,
    44: 4,
    46: 46,
    89: 42
  },
  'Kick Drum': 35,
  'Machine Castanets': 85,
  'Maracas': 70,
  'Ratchet': 74,
  'Ride Cymbal': {
    92: 51,
    93: 53
  },
  'Sand Block': 69,
  'Scratching': 69,
  'Shaker': 82,
  'Sleigh Bells': 83,
  'Snare Drum': {
    36: 38,
    59: 38,
    60: 38
  },
  'Splash Cymbal': 55,
  'Static FX': 85,
  'Suspended Cymbal': 49,
  'Tambourine': 54,
  'Tamtam': 52,
  'Temple Blocks': {
    36: 77,
    47: 77,
    57: 77,
    63: 76,
    70: 76,
  },
  'Timbales': {
    70: 66,
    71: 65,
    72: 66
  },
  'Toms': {
    42: 45,
    43: 47,
    44: 47,
    46: 48,
    48: 45,
    52: 45,
    55: 47,
    59: 47,
    62: 48,
    65: 48,
    68: 47,
    69: 50,
    70: 48,
    72: 50
  },
  'Triangle': {
    80: 80,
    81: 81,
    82: 81
  },
  'VibraSlap': 58,
  'Whip': 28,
  'Wind Chimes': 84,
  'Wood Block': 76,
  'Wood Blocks': {
    62: 76,
    63: 77
  }
}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
overwrite = True
new_file_location = 'Modified'
game_acronym = 'EY'
game_name = 'Kirby\'s Epic Yarn'
track_names = [
  'Rainbow Falls'
]

for track_name in track_names:
  short_name = '{} {}'.format(game_acronym, track_name)
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
