from collections import defaultdict
from mido import MidiFile
import os
from file_locations import *
from typing import Any, Dict, List, Tuple

midi_file_1 = 'A New Adventure.mid'
midi_file_2 = midi_file_1
midi_path_1 = os.path.join(sf2_folder, 'Pokémon Mystery Dungeon Red Rescue Team', midi_file_1)
midi_path_2 = os.path.join(sf2_folder, 'Pokémon Mystery Dungeon Blue Rescue Team', midi_file_2)

def get_midi_data(midi_path: str) -> Dict[int, List[int]]:
  mid = MidiFile(midi_path)

  midi_data = defaultdict(list)
  last_notes: Dict[Tuple(int, int)] = {}
  current_time = 0
  for track in mid.tracks:
    for msg in track:
      if hasattr(msg, 'time'):
        current_time += msg.time
      if msg.type == 'note_on' and msg.velocity > 0:
        if msg.channel in last_notes:
          last_note = last_notes[msg.channel]
          if last_note[0] == msg.note and last_note[1] == current_time:
            continue

        midi_data[msg.channel].append(msg.note)
        last_notes[msg.channel] = (msg.note, current_time)
  return midi_data

def get_sorted_data(data: Dict[int, Any]) -> List[Tuple[int, Any]]:
  return sorted(data.items(), key = lambda item: item[0])

def print_midi_data(midi_data: Dict[int, List[int]]):
  for i, track in get_sorted_data(midi_data):
    print(i, track)
    print()

midi_data_1 = get_midi_data(midi_path_1)
midi_data_2 = get_midi_data(midi_path_2)

differences: Dict[int, Tuple[int, int]] = {}

def find_differences(offset):
  for i, track_1 in get_sorted_data(midi_data_1):
    for j, track_2 in get_sorted_data(midi_data_2):
      if i in differences and differences[i][1] == 0:
        continue
      num_differences = 0
      for k in range(min(len(track_1), len(track_2))):
        if track_1[k] != track_2[k] + offset:
          num_differences += 1
      num_differences += abs(len(track_1) - len(track_2))
      if i not in differences or differences[i][1] > num_differences:
        differences[i] = (j, num_differences, track_1, track_2)

find_differences(0)
find_differences(12)
find_differences(-12)

for i, difference in get_sorted_data(differences):
  if difference[1] > 0:
    print(i, difference[0], difference[1])
    print(difference[2])
    print(difference[3])
    print()
