from collections import defaultdict
from file_locations import *
from general_midi import *
from mido import MidiFile
import os

search_folder = os.path.join(sf2_folder, 'Pokémon Mystery Dungeon Explorers of Time and Darkness')

instrument_tracks = defaultdict(list)

remap_names = {
  ACOUSTIC_GRAND_PIANO: 'GRAND_PIANO',
  ACOUSTIC_GUITAR_NYLON: 'ACOUSTIC_GUITAR',
  ACOUSTIC_GUITAR_STEEL: 'ACOUSTIC_GUITAR',
  ALTO_SAX: 'SAX',
  ELECTRIC_BASS_FINGER: 'ELECTRIC_BASS',
  FIDDLE: 'VIOLIN',
  KALIMBA: 'MARIMBA',
  SOPRANO_SAX: 'SAX',
  TENOR_SAX: 'SAX',
}

percussion_remap_names = {
  ACOUSTIC_BASS_DRUM: 'BASS_DRUM',
  ACOUSTIC_SNARE: 'SNARE',
  CLOSED_HI_HAT: 'HI_HAT',
  ELECTRIC_BASS_DRUM: 'BASS_DRUM',
  ELECTRIC_SNARE: 'SNARE',
  HIGH_AGOGO: 'AGOGO',
  HIGH_BONGO: 'BONGO',
  HIGH_FLOOR_TOM: 'TOM',
  HIGH_TIMBALE: 'TIMBALE',
  HIGH_TOM: 'TOM',
  HIGH_WOODBLOCK: 'WOODBLOCK',
  HI_MID_TOM: 'TOM',
  LONG_GUIRO: 'GUIRO',
  LONG_WHISTLE: 'WHISTLE',
  LOW_AGOGO: 'AGOGO',
  LOW_BONGO: 'BONGO',
  LOW_CONGA: 'CONGA',
  LOW_FLOOR_TOM: 'TOM',
  LOW_MID_TOM: 'TOM',
  LOW_TIMBALE: 'TIMBALE',
  LOW_WOODBLOCK: 'WOODBLOCK',
  MUTE_CUICA: 'CUICA',
  MUTE_HIGH_CONGA: 'CONGA',
  MUTE_SURDO: 'SURDO',
  MUTE_TRIANGLE: 'TRIANGLE',
  OPEN_CUICA: 'CUICA',
  OPEN_HI_HAT: 'HI_HAT',
  OPEN_HIGH_CONGA: 'CONGA',
  OPEN_SURDO: 'SURDO',
  OPEN_TRIANGLE: 'TRIANGLE',
  PEDAL_HI_HAT: 'HI_HAT',
  RIDE_BELL: 'RIDE_CYMBAL',
  SHORT_GUIRO: 'GUIRO',
  SHORT_WHISTLE: 'WHISTLE',
  SIDE_STICK: 'SNARE',
}

for file in sorted(os.listdir(search_folder)):
  if file.endswith('.mid'):
    file_location = os.path.join(search_folder, file)
    mid = MidiFile(file_location)
    instruments = set()
    for i, track in enumerate(mid.tracks):
      for msg in track:
        if msg.type == 'program_change' and msg.channel != PERCUSSION_CHANNEL:
          if msg.program in remap_names:
            instruments.add(remap_names[msg.program])
          else:
            name = GENERAL_MIDI_NAMES[msg.program]
            if name.endswith('_1') or name.endswith('_2'):
              name = name[:-2]
            instruments.add(name)
        elif msg.type == 'note_on' and msg.channel == PERCUSSION_CHANNEL and msg.note in GENERAL_MIDI_PERCUSSION_NAMES:
          if msg.note in percussion_remap_names:
            instruments.add(name)
          elif msg.note in GENERAL_MIDI_PERCUSSION_NAMES:
            name = GENERAL_MIDI_PERCUSSION_NAMES[msg.note]
            if name.endswith('_1') or name.endswith('_2'):
              name = name[:-2]
            instruments.add(name)

    for instrument in instruments:
      instrument_tracks[instrument].append(file)

instrument_tracks_list = [(instrument, tracks) for instrument, tracks in instrument_tracks.items()]
for count in reversed(sorted(instrument_tracks_list, key=lambda count: len(count[1]))):
  print(f'{count[0]}: {len(count[1])}')
