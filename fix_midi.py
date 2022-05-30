from mido import MidiFile
from finale_remap import *
from game_acronyms import *
import os;

remap_channels = {
}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
scores_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Scores')
raw_midi_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Raw MIDIs')
overwrite = False
new_file_location = 'Modified'

search_tracks = set()
search_instruments = set([])

for file in sorted(os.listdir(scores_folder)):
  if file.endswith('.mid'):
    print('Fixing', file)
    full_file_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_file_name)
    file_location = os.path.join(scores_folder, file)
    remap_results = {}

    mid = MidiFile(file_location)
    for i, track in enumerate(mid.tracks):
      orig_instrument_name = track.name
      if len(orig_instrument_name) == 0:
        continue

      instrument_name = get_instrument_name(orig_instrument_name)

      percussion = instrument_name in percussion_parts
      current_program = None
      for msg in track:
        if percussion and hasattr(msg, 'channel'):
          msg.channel = 9
          if msg.type == 'note_on' or msg.type == 'note_off':
            if percussion_parts[instrument_name] is not None:
              mapping = get_percussion_mapping(instrument_name, msg.note)
              if mapping is None:
                print('Encountered unmapped percussion note:', track.name, msg.note)
              else:
                msg.note = mapping
        elif msg.type == 'program_change':
          if msg.program != PIZZICATO_STRINGS:
            mapped_program = get_mapped_program(game_acronym, full_file_name, instrument_name, orig_instrument_name)
            if mapped_program is None:
              print('Encountered unmapped track:', instrument_name)
            else:
              msg.program = mapped_program
          current_program = msg.program
          if current_program in search_instruments:
            search_tracks.add(track_name)
        elif msg.type == 'note_on' or msg.type == 'note_off':
          transpose_offset = get_transpose_offset(game_acronym, current_program, track_name, orig_instrument_name)
          msg.note = msg.note + transpose_offset
        if not percussion and hasattr(msg, 'channel') and msg.channel == 9:
          new_channel = 15
          if track_name in remap_channels:
            remap_data = remap_channels[track_name]
            if i in remap_data:
              new_channel = remap_data[i]
          msg.channel = new_channel
          remap_results[i] = (instrument_name, new_channel)

    if len(remap_results) > 0:
      for i, entry in remap_results.items():
        print('Remapped track %d (%s) to %s' % (i, entry[0], entry[1]))

    new_file_path = os.path.join(new_file_location, file)
    print('Saving file to', new_file_path)
    mid.save(new_file_path)


if len(search_tracks) > 0:
  print(list(sorted(search_tracks)))