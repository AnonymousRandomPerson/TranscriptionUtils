from collections import defaultdict
from typing import Dict
from mido import MidiFile
from dataclasses import dataclass
from map_midi_settings_mdbsl import *
from split_type0_midi import subdivide_midi_tracks
import os;

dry_run = False
overwrite = False
new_file_location = 'Modified'
track_names = [
  'dun_boss',
  'dun_bossfloor',
  'dun_forest_1',
  'dun_forest_2',
  'dun_forest',
  'dun_grassy_1',
  'dun_grassy_2',
  'dun_grassy',
  'dun_mount_1',
  'dun_mount_2',
  'dun_mount',
  'dun_sea_1',
  'dun_sea_2',
  'dun_sea',
  'endroll',
  'ev_1',
  'ev_2',
  'ev_3',
  'ev_4',
  'ev_5',
  'ev_ed',
  'ev_fear',
  'ev_op',
  'gameclear',
  'gameover',
  'me_dunopen',
  'me_evolution_e',
  'me_evolution',
  'me_exclude',
  'me_item',
  'me_join',
  'me_lankup',
  'me_lvup',
  'me_reward',
  'me_system',
  'me_wave_m',
  'me_wave_s',
  'me_wind_m',
  'me_wind_s',
  'no_sound',
  'sys_bazar',
  'sys_clear',
  'sys_map',
  'sys_menu',
  'sys_monster',
  'sys_shop',
  'sys_steal',
]

percussion_transpose = -12

default_to_percussion = False

def get_mapping(mapping, key, inner_key):
  if key not in mapping:
    return None
  value = mapping[key]
  if isinstance(value, dict):
    if inner_key in value:
      return value[inner_key]
    elif 'Default' in value:
      return value['Default']
    else:
      return None
  return value

@dataclass
class Channel:
  found_program: bool = False
  current_program: int = None
  current_mapped_program: int = None
  has_non_percussion: bool = False
  current_percussion: bool = default_to_percussion
  found_note: bool = False
  num_notes: int = 0
  first_volume = None
  volume_changes = None

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
  type0 = len(mid.tracks) == 1
  for i, track in enumerate(mid.tracks):
    remove_messages = []
    for msg in track:
      if msg.type == 'sysex':
        remove_messages.append(msg)
      if hasattr(msg, 'channel'):
        used_channels.add(msg.channel)
        channel = channels[msg.channel]
        if channel.volume_changes is None:
          channel.volume_changes = []
        if msg.type == 'program_change':
          channel.found_program = True
          channel.current_program = msg.program
          if msg.program in percussion_programs:
            channel.current_percussion = True
            msg.program = PERCUSSION
          else:
            channel.current_percussion = False
            if msg.program in program_mapping:
              mapped_program = get_mapping(program_mapping, msg.program, track_name)
              if mapped_program is None:
                remove_messages.append(msg)
              else:
                msg.program = mapped_program
            else:
              unmapped_programs.add(msg.program)
          channel.current_mapped_program = msg.program
    for msg in track:
      if msg.type != 'program_change' and hasattr(msg, 'channel'):
        channel = channels[msg.channel]
        if channel.found_program and channel.current_mapped_program is None:
          remove_messages.append(msg)
        else:
          if msg.type == 'note_on' or msg.type == 'note_off':
            if msg.type == 'note_on':
              channel.num_notes += 1
            if channel.current_percussion:
              note = msg.note + percussion_transpose
              if note in percussion_parts:
                mapped_note = percussion_parts[note]
                found_note = False
                if isinstance(mapped_note, int):
                  msg.note = percussion_parts[note]
                  found_note = True
                elif mapped_note is None:
                  msg.velocity = 0
                  found_note = True
                else:
                  if channel.current_program in mapped_note:
                    mapped_note = mapped_note[channel.current_program]
                    found_note = True
                  elif 'Default' in mapped_note:
                    mapped_note = mapped_note['Default']
                    found_note = True
                  if mapped_note is None:
                    msg.velocity = 0
                  elif found_note:
                    msg.note = mapped_note
                if not found_note:
                  unmapped_percussion_notes.add(note)
              else:
                unmapped_percussion_notes.add(note)
            else:
              channel.has_non_percussion = True
              current_transpose = get_mapping(program_transpose, channel.current_program, channel.current_mapped_program)
              if current_transpose:
                msg.note += current_transpose
          if msg.type == 'control_change' and (msg.control == 7 or msg.control == 10):
            channel.volume_changes.append(msg)
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
      if remap_percussion_channel is None:
        print('No channel found to remap percussion.')

    primary_percussion_channel: Channel = None
    for channel in channels.values():
      if channel.current_percussion and (not primary_percussion_channel or primary_percussion_channel.num_notes < channel.num_notes):
        primary_percussion_channel = channel
    for i, channel in channels.items():
      if channel.current_percussion and channel is not primary_percussion_channel:
        print('Removing volume changes for channel %d.' % i)
        for msg in channel.volume_changes:
          msg.control = 0
          msg.value = 0

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

    if type0:
      subdivide_midi_tracks(new_file_path).save(new_file_path)
