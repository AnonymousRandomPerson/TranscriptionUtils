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
  'dun_boss'
]

percussion_transpose = -12

default_to_percussion = False

@dataclass
class Channel:
  found_program: bool = False
  current_program: int = None
  current_mapped_program: int = None
  has_non_percussion: bool = False
  current_percussion: bool = default_to_percussion
  found_note: bool = False

for track_name in track_names:
  print('Converting', track_name)

  unmapped_programs = set()
  unmapped_percussion_notes = set()

  file_name = '{}.mid'.format(track_name)
  file_location = os.path.join(parts_folder, file_name)
  new_file_name = file_name
  channels: Dict[int, Channel] = defaultdict(Channel)
  used_channels = set()

  mid = MidiFile(file_location)
  for i, track in enumerate(mid.tracks):
    remove_messages = []
    for msg in track:
      if msg.type == 'sysex':
        remove_messages.append(msg)
      if hasattr(msg, 'channel'):
        used_channels.add(msg.channel)
        channel = channels[msg.channel]
        if msg.type == 'program_change':
          channel.found_program = True
          channel.current_program = msg.program
          channel.current_mapped_program = msg.program
          if msg.program in percussion_programs:
            channel.current_percussion = True
            msg.program = PERCUSSION
            #remove_messages.append(msg)
          else:
            channel.current_percussion = False
            if msg.program in program_mapping:
              channel.current_mapped_program = program_mapping[msg.program]
              if channel.current_mapped_program is None:
                remove_messages.append(msg)
              else:
                msg.program = program_mapping[msg.program]
            else:
              unmapped_programs.add(msg.program)
    for msg in track:
      if msg.type != 'program_change' and hasattr(msg, 'channel'):
        channel = channels[msg.channel]
        if channel.found_program and channel.current_mapped_program is None:
          remove_messages.append(msg)
        else:
          if msg.type == 'note_on' or msg.type == 'note_off':
            if channel.current_percussion:
              note = msg.note + percussion_transpose
              if note in percussion_parts:
                mapped_note = percussion_parts[note]
                if isinstance(mapped_note, int):
                  msg.note = percussion_parts[note]
                elif mapped_note is None:
                  remove_messages.append(msg)
                elif channel.current_program in mapped_note:
                  msg.note = mapped_note[channel.current_program]
                else:
                  unmapped_percussion_notes.add((channel.current_program, note))
              else:
                unmapped_percussion_notes.add(note)
            else:
              channel.has_non_percussion = True
              if channel.current_program in program_transpose:
                msg.note += program_transpose[channel.current_program]
    for msg in remove_messages:
      track.remove(msg)

    remap_percussion_channel = None
    if channels[PERCUSSION_CHANNEL].has_non_percussion:
      for i in range(0, 15):
        if i not in channels:
          remap_percussion_channel = i
          print('Remapping channel', PERCUSSION_CHANNEL, 'to', remap_percussion_channel)
          break
      if remap_percussion_channel is None:
        for i in range(0, 15):
          if channels[i].current_percussion:
            remap_percussion_channel = i
            print('Remapping channel', PERCUSSION_CHANNEL, 'to', remap_percussion_channel)
            break

    for msg in track:
      if hasattr(msg, 'channel'):
        channel = channels[msg.channel]
        if msg.type == 'note_on':
          channel.found_note = True

        if msg.channel == PERCUSSION_CHANNEL and remap_percussion_channel is not None:
          msg.channel = remap_percussion_channel
        elif channel.current_percussion and (channel.found_note or not default_to_percussion):
          msg.channel = PERCUSSION_CHANNEL

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
