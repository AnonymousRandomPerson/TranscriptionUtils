from collections import defaultdict
from mido import MidiFile
from finale_remap import *
from game_acronyms import *
from file_locations import *
from fix_config import *
from fix_midi_custom import fix_custom
import os;

remap_channels = {
}

for file in sorted(os.listdir(search_folder)):
  if file.endswith('.mid'):
    print('Fixing', file)
    full_file_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_file_name)
    combined_name = game_acronym + ' ' + track_name
    file_location = os.path.join(search_folder, file)
    remap_results = {}
    percussion_sequence_parts = defaultdict(PercussionSequencePart)
    remove_tracks = []

    mid = MidiFile(file_location)
    for i, track in enumerate(mid.tracks):
      device_name = None
      orig_instrument_name = track.name
      if len(orig_instrument_name) == 0:
        continue

      if track.name.endswith('(hidden)'):
        remove_tracks.append(track)
        continue

      instrument_name = get_instrument_name(orig_instrument_name)
      if instrument_name in search_instruments:
        search_tracks.add(combined_name)

      percussion = instrument_name in percussion_parts
      current_program: int = None
      remove_messages = []
      for msg in track:
        if msg.type == 'device_name':
          device_name = msg
        mapped_program = get_mapped_program(game_acronym, full_file_name, instrument_name, orig_instrument_name)
        if percussion and hasattr(msg, 'channel') and mapped_program != MELODIC_TOM:
          msg.channel = 9
          if msg.type == 'note_on' or msg.type == 'note_off':
            if percussion_parts[instrument_name] is not None:
              if len(search_percussion) > 0:
                search_percussion_note = (instrument_name, msg.note)
                if search_percussion_note in search_percussion:
                  search_tracks.add(combined_name)
              if instrument_name in percussion_sequence_mappings:
                fill_percussion_sequence_parts(instrument_name, msg.note, msg, percussion_sequence_parts)
              else:
                mapping = get_percussion_mapping(game_acronym, track_name, instrument_name, msg.note)
                if mapping is None:
                  print('Encountered unmapped percussion note:', track.name, msg.note)
                else:
                  msg.note = mapping
          if msg.type == 'program_change':
            remove_messages.append(msg)
        elif msg.type == 'program_change':
          if msg.program != PIZZICATO_STRINGS and not msg.program == SLAP_BASS_1:
            if mapped_program is None:
              print('Encountered unmapped track:', instrument_name)
            else:
              msg.program = mapped_program
          current_program = msg.program
          if current_program in search_instruments:
            search_tracks.add(combined_name)
        elif msg.type == 'note_on' or msg.type == 'note_off':
          if current_program == ORCHESTRAL_HARP and msg.note == 2:
            print('Removed invalid harp note', msg)
            msg.note = 0
            msg.velocity = 0
          else:
            transpose_offset = get_transpose_offset(game_acronym, current_program, track_name, instrument_name, orig_instrument_name)
            transposed_note = msg.note + transpose_offset
            if transposed_note < 0:
              msg.note = 0
              msg.velocity = 0
              print('Removed tranposed note out of range for', instrument_name)
            else:
              msg.note = transposed_note
        if not percussion and hasattr(msg, 'channel') and msg.channel == 9:
          new_channel = 15
          if track_name in remap_channels:
            remap_data = remap_channels[track_name]
            if i in remap_data:
              new_channel = remap_data[i]
          msg.channel = new_channel
          remap_results[i] = (instrument_name, new_channel)
          device_name.name += '-' + str(i)
        fix_custom(combined_name, msg, instrument_name)
      for msg in remove_messages:
        track.remove(msg)

    for instrument_name, sequence_part in percussion_sequence_parts.items():
      for msg in sequence_part.messages:
        msg.note = map_percussion_sequence_note(instrument_name, msg.note, sequence_part)

    for track in remove_tracks:
      print('Removing track:', track.name)
      mid.tracks.remove(track)

    if len(remap_results) > 0:
      for i, entry in remap_results.items():
        print('Remapped track %d (%s) to %s.' % (i, entry[0], entry[1]))

    if not dry_run and (not save_search or combined_name in search_tracks):
      new_file_path = os.path.join(modified_folder, file)
      print('Saving file to', new_file_path)
      mid.save(new_file_path)

if len(search_tracks) > 0:
  print(list(sorted(search_tracks)))
