from collections import defaultdict
from typing import Dict
from mido import MidiFile
from dataclasses import dataclass
from map_midi_settings_mdbsl import *
import os;

dry_run = False
overwrite = False
new_file_location = 'Modified'
track_names = [
  'dun_forest_1',
  # 'dun_forest_2',
  # 'dun_grassy',
  # 'dun_grassy_1',
  # 'dun_grassy_2',
  # 'dun_sea',
  # 'dun_sea_1',
  # 'dun_sea_2',
  # 'sys_map'
]

unmapped_programs = set()
unmapped_percussion_notes = set()
percussion_transpose = -12

default_to_percussion = False

@dataclass
class Channel:
  current_program: int = None
  percussion: bool = default_to_percussion
  found_note: bool = False

for track_name in track_names:
  print('Converting', track_name)
  file_name = '{}.mid'.format(track_name)
  file_location = os.path.join(parts_folder, file_name)
  new_file_name = file_name
  channels: Dict[int, Channel] = defaultdict(Channel)

  mid = MidiFile(file_location)
  for i, track in enumerate(mid.tracks):
    for msg in track:
      if hasattr(msg, 'channel'):
        channel = channels[msg.channel]
        if msg.type == 'program_change':
          channel.current_program = msg.program
          if msg.program in percussion_programs:
            channel.percussion = True
            msg.program = PERCUSSION
          else:
            channel.percussion = False
            if msg.program in program_mapping:
              msg.program = program_mapping[msg.program]
            else:
              unmapped_programs.add(msg.program)
        else:
          if channel.percussion and channel.found_note:
            msg.channel = 9
          if msg.type == 'note_on' or msg.type == 'note_off':
            channel.found_note = True
            if channel.percussion:
              note = msg.note + percussion_transpose
              if note in percussion_parts:
                mapped_note = percussion_parts[note]
                if isinstance(mapped_note, int):
                  msg.note = percussion_parts[note]
                elif mapped_note is None:
                  msg.velocity = 0
                elif channel.current_program in mapped_note:
                  msg.note = mapped_note[channel.current_program]
                else:
                  unmapped_percussion_notes.add((channel.current_program, note))
              else:
                unmapped_percussion_notes.add(note)
            elif channel.current_program in program_transpose:
              msg.note += program_transpose[channel.current_program]

  if len(unmapped_programs):
    print('Encountered unmapped programs:', sorted(list(unmapped_programs)))
  if len(unmapped_percussion_notes):
    print('Encountered unmapped percussion notes:', sorted(list(unmapped_percussion_notes)))

  if overwrite:
    new_file_path = file_location
  else:
    sep_index = new_file_name.rfind(os.sep)
    if sep_index >= 0:
      new_file_name = new_file_name[sep_index + 1:]
    new_file_path = os.path.join(new_file_location, new_file_name)
  print('Saving file to', new_file_path)
  if not dry_run:
    mid.save(new_file_path)
