from collections import defaultdict
from mido import MidiFile
import os
from file_locations import *
from general_midi import *
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
import editdistance

track_name = 'Sojourn'

midi_file_1 = track_name + '.mid'
midi_file_2 = midi_file_1
midi_path_1 = os.path.join(sf2_folder, 'RuneScape', 'RuneScape HD', midi_file_1)
midi_path_2 = os.path.join(sf2_folder, 'RuneScape', 'Old School RuneScape', midi_file_2)

equal_programs = {}
equal_percussion = {
  1: 24,
  3: 27,
  7: 28,
  8: 32,
  10: 34,
  11: 35,
  12: 36,
  13: 24,
  24: 37,
  25: 24,
}
percussion_program = 0
transpose = 0

@dataclass
class Note:
  note: int
  time: int

def get_midi_data(midi_path: str) -> Dict[str, List[Note]]:
  mid = MidiFile(midi_path)

  midi_data: Dict[str, List[Note]] = defaultdict(list)
  channel_programs = defaultdict(int)
  for track in mid.tracks:
    current_time = 0
    for msg in track:
      if hasattr(msg, 'time'):
        current_time += msg.time
      if msg.type == 'program_change':
        program = msg.program
        if program in equal_programs:
          program = equal_programs[program]
        channel_programs[msg.channel] = program
      if msg.type == 'note_on' and msg.velocity > 0:
        program_key = str(channel_programs[msg.channel]) + '_' + str(msg.channel)
        program_data = midi_data[program_key]
        same_time_notes: List[Note] = []
        same_note = False
        msg_note = msg.note
        if channel_programs[msg.channel] == percussion_program and msg_note in equal_percussion:
            msg_note = equal_percussion[msg_note]
        for note in reversed(program_data):
          if note.time == current_time:
            if note.note == msg_note:
              same_note = True
              break
            same_time_notes.append(note)
          else:
            break
        if same_note:
          continue

        for _ in range(len(same_time_notes)):
          program_data.pop()

        same_time_notes.append(Note(msg_note, current_time))
        same_time_notes.sort(key = lambda note: note.note)

        for note in same_time_notes:
          #if len(program_data) == 0 or program_data[-1].note != note.note:
            program_data.append(note)

  return midi_data

def get_sorted_data(data: Dict[str, Any]) -> List[Tuple[str, Any]]:
  return sorted(data.items(), key = lambda item: item[0])

def print_midi_data(midi_data: Dict[str, List[Note]]):
  for i, track in get_sorted_data(midi_data):
    print(i, [note.note for note in track])
    print()

midi_data_1 = get_midi_data(midi_path_1)
midi_data_2 = get_midi_data(midi_path_2)

# print_midi_data(midi_data_1)
# print_midi_data(midi_data_2)

@dataclass
class Difference:
  program: str
  num_differences: int
  track_1: List[Note]
  track_2: List[Note]

differences: Dict[str, Difference] = {}

def find_differences(offset):
  for program_1, track_1 in get_sorted_data(midi_data_1):
    for program_2, track_2 in get_sorted_data(midi_data_2):
      if program_1 in differences and differences[program_1].num_differences == 0:
        continue
      num_differences = editdistance.distance([note.note for note in track_1], [note.note + offset for note in track_2])
      if num_differences == 1:
        print()
      if program_1 not in differences or differences[program_1].num_differences > num_differences:
        differences[program_1] = Difference(program_2, num_differences, track_1, track_2)

for i in range(0, 5):
  if i == 0 and transpose == 0:
    find_differences(i)
  else:
    find_differences(i * 12 + transpose)
    find_differences(-i * 12 + transpose)

no_differences = True
for program, difference in get_sorted_data(differences):
  if difference.num_differences > 0:
    print(program, difference.program, difference.num_differences)
    print([note.note for note in difference.track_1])
    print([note.note for note in difference.track_2])
    print()
    no_differences = False

if no_differences:
  print('No differences found.')
