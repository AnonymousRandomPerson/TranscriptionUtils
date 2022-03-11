from mido import MidiFile
from map_midi_settings_dl3 import program_mapping, program_transpose, percussion_parts, parts_folder, percussion_programs
import os;

overwrite = False
new_file_location = 'Modified'
join_name = 'Gourmet Race'
track_names = [
  os.path.join(join_name, join_name)
]

unmapped_programs = set()
unmapped_percussion_notes = set()
percussion_transpose = -12

for track_name in track_names:
  file_name = '{}.mid'.format(track_name)
  file_location = os.path.join(parts_folder, file_name)
  new_file_name = file_name

  mid = MidiFile(file_location)
  for i, track in enumerate(mid.tracks):
    current_program = None
    for msg in track:
      if msg.type == 'program_change':
        current_program = msg.program
        if current_program not in percussion_programs:
          if msg.program in program_mapping:
            msg.program = program_mapping[msg.program]
          else:
            unmapped_programs.add(msg.program)
      elif hasattr(msg, 'channel'):
        percussion = current_program in percussion_programs
        if percussion:
          msg.channel = 9
        if msg.type == 'note_on' or msg.type == 'note_off':
          if percussion:
            note = msg.note + percussion_transpose
            if note in percussion_parts:
              msg.note = percussion_parts[note]
            else:
              unmapped_percussion_notes.add(note)
          elif current_program in program_transpose:
            msg.note += program_transpose[current_program]

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
  mid.save(new_file_path)
