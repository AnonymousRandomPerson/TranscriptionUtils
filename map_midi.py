from mido import MidiFile
import os;

program_mapping = {
  7: 57,
  45: 41,
  52: 81,
  54: 41,
  83: 81,
  95: 41,
  102: 17,
  119: 81
}

program_transpose = {
  54: 12,
  95: 12,
  102: 24
}

percussion_parts = {
  24: 35,
  29: 38,
  31: 39,
  32: 42,
  33: 38,
  39: 44,
  40: 46,
  49: 61,
  50: 60,
  51: 63,
  52: 64,
  57: 70,
  68: 80,
  69: 81
}

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Library', 'Audio', 'Sounds', 'Banks', 'Sf2', 'Pokémon Mystery Dungeon Blue Rescue Team', 'Mapped')

overwrite = True
new_file_location = 'Modified'
track_names = [
  'Battle With Rayquaza'
]

unmapped_programs = set()
unmapped_percussion_notes = set()
percussion_transpose = -12

for track_name in track_names:
  file_name = '{}.midi'.format(track_name)
  file_location = os.path.join(parts_folder, file_name)
  new_file_name = file_name

  mid = MidiFile(file_location)
  for i, track in enumerate(mid.tracks):
    for msg in track:
      if msg.type == 'program_change':
        current_program = msg.program
        if msg.program == 127:
          percussion = True
        else:
          percussion = False
          if msg.program in program_mapping:
            msg.program = program_mapping[msg.program]
          else:
            unmapped_programs.add(msg.program)
      elif hasattr(msg, 'channel'):
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
    new_file_path = os.path.join(new_file_location, new_file_name)
  print('Saving file to', new_file_path)
  mid.save(new_file_path)
