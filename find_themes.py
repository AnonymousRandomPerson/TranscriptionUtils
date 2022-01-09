from mido import MidiFile
from dataclasses import dataclass
from typing import List
import os

midi_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Explorers of Time and Darkness')
theme = [55, 62, 60, 65, 62]
# Amount of beat separation before discarding a sequence.
separation_tolerance = 4

@dataclass
class NoteSequence:
  channel: int
  sequence: List[str]
  time: int
  end_time: int

theme_offsets = []
prev_note = None
for note in theme:
  if prev_note is not None:
    offset = note - prev_note
    if offset != 0:
      theme_offsets.append(note - prev_note)
  prev_note = note

os.chdir(midi_folder)
for file in sorted(os.listdir(os.getcwd())):
  if file.endswith('.mid'):
    current_time = 0
    mid = MidiFile(os.path.join(midi_folder, file))
    channels = {}
    for track in mid.tracks:
      for msg in track:
        matching_channel = None
        if hasattr(msg, 'time'):
          current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
          if msg.channel not in channels:
            channels[msg.channel] = NoteSequence(msg.channel, [], current_time, current_time)
          note_sequence = channels[msg.channel]
          sequence = channels[msg.channel].sequence
          if len(sequence) == 0:
            sequence.append(msg.note)
            note_sequence.time = current_time
            note_sequence.end_time = current_time
          else:
            note_offset = msg.note - sequence[-1]
            if note_offset != 0:
              if note_offset == theme_offsets[len(sequence) - 1] and current_time - note_sequence.end_time <= mid.ticks_per_beat * separation_tolerance:
                sequence.append(msg.note)
                note_sequence.end_time = current_time
                if len(sequence) > len(theme_offsets):
                  matching_channel = note_sequence
                  break
              else:
                sequence.clear()
    if matching_channel is not None:
      print('Found theme match in %s, channel %s, beat %s' % (file, matching_channel.channel, matching_channel.time / mid.ticks_per_beat))
