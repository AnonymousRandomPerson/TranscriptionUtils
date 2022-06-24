from tkinter import N
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
            xml_header = xml_string[0:xml_string.find('<score-partwise'.encode('utf-8'))]

            credit_remove = [child for child in xml_root.findall('credit') if child.attrib['page'] != '1' and child.find('credit-type').text == 'title']
            [xml_root.remove(credit) for credit in credit_remove]

            parts = {}
            open_hi_hat_ids = set()
            for part_info in xml_root.find('part-list').findall('score-part'):
              part_name = part_info.find('part-name').text
              instrument_name = get_instrument_name(part_name)
              program = None
              #print(item.filename, part_name)

              percussion = instrument_name in mxl_percussion_override
              if not percussion:
                for midi_instrument in part_info.findall('midi-instrument'):
                  if midi_instrument.find('midi-unpitched') is not None:
                    percussion = True

              if percussion:
                if not instrument_name in ignore_unmapped_percussion:
                  percussion_instruments = {}
                  for score_instrument in part_info.findall('score-instrument'):
                    percussion_instrument_name = score_instrument.find('instrument-name').text.strip().replace('%g', '')
                    percussion_instruments[score_instrument.attrib['id']] = percussion_instrument_name
                  for midi_instrument in part_info.findall('midi-instrument'):
                    percussion_instrument_name = percussion_instruments[midi_instrument.attrib['id']]
                    midi_unpitched = midi_instrument.find('midi-unpitched')
                    if instrument_name in mxl_percussion_override:
                      midi_unpitched = ElementTree.Element('midi-unpitched')
                      midi_instrument.insert(2, midi_unpitched)
                      midi_unpitched.text = str(mxl_percussion_override[instrument_name] + 1)
                    elif midi_unpitched is None:
                      if full_score and not percussion_instrument_name in ignore_unmapped_percussion:
                        print('Encountered unmapped percussion note', percussion_instrument_name, 'in', instrument_name)
                    else:
                      current_note = int(midi_unpitched.text) - 1
                      percussion_mapping = get_percussion_mapping(game_acronym, track_name, instrument_name, current_note)
                      if percussion_mapping is None:
                        if full_score and not percussion_instrument_name in ignore_unmapped_percussion:
                          print('Encountered unmapped percussion note', current_note, 'in', instrument_name)
                      else:
                        midi_unpitched.text = str(percussion_mapping + 1)

              else:
                program = get_mapped_program(game_acronym, full_file_name, instrument_name, part_name)
                if program is not None:
                  part_info.find('midi-instrument').find('midi-program').text = str(program + 1)

                  if program in mxl_instruments:
                    score_instrument = part_info.find('score-instrument')
                    instrument_sound = score_instrument.find('instrument-sound')
                    if instrument_sound is None:
                      instrument_sound = ElementTree.SubElement(score_instrument, 'instrument-sound')
                    instrument_sound.text = mxl_instruments[program]
              parts[part_info.attrib['id']] = (part_name, instrument_name, program)

              open_hi_hat = False
              cross_stick = False
              for midi_instrument in part_info.findall('midi-instrument'):
                midi_unpitched = midi_instrument.find('midi-unpitched')
                if midi_unpitched is not None:
                  if midi_unpitched.text == str(OPEN_HI_HAT + 1):
                    open_hi_hat = True
                    open_hi_hat_ids.add(midi_instrument.attrib['id'])
                  cross_stick = cross_stick or midi_unpitched.text == str(SIDE_STICK + 1)


              if full_score:
                if open_hi_hat:
                  print('Found open hi-hat in', part_name)
                if cross_stick:
                  print('Found cross-stick in', part_name)

            for part in xml_root.findall('part'):
              part_name, instrument_name, program = parts[part.attrib['id']]

              if program is None:
                transpose_offset = 0
              else:
                transpose_offset = get_transpose_offset(game_acronym, program, track_name, part_name)
                octave_change = 0
                if transpose_offset != 0:
                  octave_change = abs(transpose_offset) // 12
                  if transpose_offset < 0:
                    octave_change = -octave_change

                  chromatic_change = transpose_offset % 12
                  if chromatic_change != 0 and full_score:
                    print('Found non-octave tranposition', transpose_offset, 'for', part_name)

              found_breath_mark = None
              for measure in part.findall('measure'):
                measure_number = measure.attrib['number']

                print_page = measure.find('print')
                if print_page is not None and 'new-page' in print_page.attrib:
                  measure.remove(print_page)

                if transpose_offset != 0:
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

                if full_score:
                  for direction in measure.findall('direction'):
                    direction_type = direction.find('direction-type')
                    if program == STRING_ENSEMBLE_1:
                      words = direction_type.find('words')
                      if words is not None and (words.text == 'pizz.' or words.text == 'arco'):
                        print('Found {} in {}, measure {}'.format(words.text, part_name, measure_number))

                    octave_shift = direction_type.find('octave-shift')
                    if octave_shift is not None:
                      shift_type = octave_shift.attrib['type']
                      if shift_type == 'down' or shift_type == 'up':
                        print('Found ottava {} in {}, measure {}'.format(shift_type, part_name, measure_number))

                tuplet_number = None
                tuplet_type = None
                for note in measure.findall('note'):
                  if instrument_name in unpitched_instruments:
                    unpitched = note.find('unpitched')
                    if unpitched is not None:
                      print('Found unpitched instrument', instrument_name)
                      # unpitched.find('display-step').text = 'F'
                      # unpitched.find('display-octave').text = '5'

                  elif instrument_name == 'Drum Set' or instrument_name == 'Snare Drum':
                    notehead = note.find('notehead')
                    if notehead is not None and notehead.text == 'back slashed':
                      note.remove(notehead)

                    if len(open_hi_hat_ids) > 1:
                      note_instrument = note.find('instrument')
                      if note_instrument is not None and note_instrument.attrib['id'] in open_hi_hat_ids:
                        unpitched = note.find('unpitched')
                        if unpitched is not None:
                          unpitched.find('display-step').text = 'G'
                          unpitched.find('display-octave').text = '5'

                  if full_score and not found_breath_mark:
                    notations = note.find('notations')
                    if notations is not None:
                      articulations = notations.find('articulations')
                      if articulations is not None:
                        breath_mark = articulations.find('breath-mark')
                        if breath_mark is not None:
                          found_breath_mark = measure_number

                  time_modification = note.find('time-modification')
                  notations = note.find('notations')
                  beams = note.findall('beam')
                  if len(beams) == 3 and time_modification is not None and notations is not None:
                    tuplet = notations.find('tuplet')
                    tuplet_normal = tuplet.find('tuplet-normal')
                    if tuplet_normal is not None:
                      tuplet_number = tuplet_normal.find('tuplet-number').text
                      tuplet_type = tuplet_normal.find('tuplet-type').text

                    target_type = None
                    if tuplet_number == '1' and tuplet_type == 'half' or tuplet_number == '3' and tuplet_type == 'quarter':
                      target_type = 'half'

                    if target_type is not None:
                      time_modification.find('actual-notes').text = '2'
                      time_modification.find('normal-notes').text = '1'
                      time_modification.remove(time_modification.find('normal-type'))
                      note.find('type').text = target_type
                      for beam in beams:
                        note.remove(beam)

                      if beams[0].text == 'begin':
                        tremolo_type = 'start'
                      else:
                        tremolo_type = 'stop'
                      notations = note.find('notations')
                      notations.remove(tuplet)
                      ornaments = ElementTree.SubElement(notations, 'ornaments')
                      tremolo = ElementTree.SubElement(ornaments, 'tremolo')
                      tremolo.attrib['type'] = tremolo_type
                      tremolo.text = '3'
                    elif full_score and tuplet_number is not None:
                      print('Found unknown tremolo {} {} in {}, measure {}'.format(tuplet_number, tuplet_type, part_name, measure_number))

              if found_breath_mark is not None:
                print('Found breath mark in {}, measure {}.'.format(part_name, found_breath_mark))

            newZip.writestr(item, xml_header + ElementTree.tostring(xml_root))
          else:
            newZip.writestr(item, origZip.read(item.filename))
    print('Saving file to', new_file_location)
