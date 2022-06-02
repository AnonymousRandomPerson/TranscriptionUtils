from finale_remap import *
from game_acronyms import *
import os;
import zipfile
import xml.etree.ElementTree as ElementTree

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')
scores_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Scores')
new_file_folder = os.path.join('.', 'Modified')

for file in sorted(os.listdir(scores_folder)):
  if file.endswith('.mxl'):
    print('Fixing', file)
    full_file_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_file_name)

    file_location = os.path.join(scores_folder, file)
    new_file_location = os.path.join(new_file_folder, file)
    with zipfile.ZipFile(file_location, 'r') as origZip:
      with zipfile.ZipFile(new_file_location, 'w') as newZip:
        for item in origZip.infolist():
          if item.filename.endswith('.musicxml'):
            full_score = item.filename.startswith(full_file_name)

            xml_string = origZip.read(item)
            xml_root = ElementTree.fromstring(xml_string)

            credit_remove = [child for child in xml_root.findall('credit') if child.attrib['page'] != '1' and child.find('credit-type').text == 'title']
            [xml_root.remove(credit) for credit in credit_remove]

            parts = {}
            for part_info in xml_root.find('part-list').findall('score-part'):
              part_name = part_info.find('part-name').text
              instrument_name = get_instrument_name(part_name)

              percussion = False
              for midi_instrument in part_info.findall('midi-instrument'):
                if midi_instrument.find('midi-unpitched') is not None:
                  percussion = True
                  break

              if percussion:
                if not instrument_name in ignore_unmapped_percussion:
                  percussion_instruments = {}
                  for score_instrument in part_info.findall('score-instrument'):
                    percussion_instrument_name = score_instrument.find('instrument-name').text.strip().replace('%g', '')
                    percussion_instruments[score_instrument.attrib['id']] = percussion_instrument_name
                  for midi_instrument in part_info.findall('midi-instrument'):
                    percussion_instrument_name = percussion_instruments[midi_instrument.attrib['id']]
                    midi_unpitched = midi_instrument.find('midi-unpitched')
                    if midi_unpitched is None:
                      if full_score and not percussion_instrument_name in ignore_unmapped_percussion:
                        print('Encountered unmapped percussion note', percussion_instrument_name, 'in', instrument_name)
                    else:
                      current_note = int(midi_unpitched.text) - 1
                      percussion_mapping = get_percussion_mapping(instrument_name, current_note)
                      if percussion_mapping is None:
                        if full_score and not percussion_instrument_name in ignore_unmapped_percussion:
                          print('Encountered unmapped percussion note', current_note, 'in', instrument_name)
                      else:
                        midi_unpitched.text = str(percussion_mapping + 1)

              else:
                program = get_mapped_program(game_acronym, full_file_name, instrument_name, part_name)
                if program is not None:
                  parts[part_info.attrib['id']] = (part_name, instrument_name, program)
                  part_info.find('midi-instrument').find('midi-program').text = str(program + 1)

                  if program in mxl_instruments:
                    part_info.find('score-instrument').find('instrument-sound').text = mxl_instruments[program]

            for part in xml_root.findall('part'):
              part_id = part.attrib['id']
              if part_id not in parts:
                continue

              part_name, instrument_name, program = parts[part.attrib['id']]

              transpose_offset = get_transpose_offset(game_acronym, program, track_name, part_name)
              if transpose_offset != 0:
                octave_change = abs(transpose_offset) // 12
                if transpose_offset < 0:
                  octave_change = -octave_change

                chromatic_change = transpose_offset % 12
                if chromatic_change != 0 and full_score:
                  print('Found non-octave tranposition', transpose_offset, 'for', part_name)

                for measure in part.findall('measure'):
                  attributes = measure.find('attributes')
                  if attributes is not None:
                    transpose = attributes.find('transpose')
                    if transpose is None:
                      transpose = ElementTree.SubElement(attributes, 'transpose')
                    octave_change_tag = transpose.find('octave-change')
                    if octave_change_tag is None:
                      ElementTree.SubElement(transpose, 'diatonic').text = '0'
                      ElementTree.SubElement(transpose, 'chromatic').text = '0'
                      octave_change_tag = ElementTree.SubElement(transpose, 'octave-change')
                      octave_change_text = '0'
                    else:
                      octave_change_text = octave_change_tag.text

                    octave_change_tag.text = str(int(octave_change_text) + octave_change)

              if program == STRING_ENSEMBLE_1 and full_score:
                for measure in part.findall('measure'):
                  for direction in measure.findall('direction'):
                    words = direction.find('direction-type').find('words')
                    if words is not None and (words.text == 'pizz.' or words.text == 'arco'):
                      print('Found', words.text, 'in', part_name)

              if instrument_name in unpitched_instruments:
                for measure in part.findall('measure'):
                  for note in measure.findall('note'):
                    unpitched = note.find('unpitched')
                    if unpitched is not None:
                      unpitched.find('display-step').text = 'F'
                      unpitched.find('display-octave').text = '5'

            newZip.writestr(item, ElementTree.tostring(xml_root))
          else:
            newZip.writestr(item, origZip.read(item.filename))
    print('Saving file to', new_file_location)
