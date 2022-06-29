from collections import defaultdict
from finale_remap import *
from game_acronyms import *
from file_locations import *
import os;
import zipfile
import xml.etree.ElementTree as ElementTree

for file in sorted(os.listdir(finale_scores_folder)):
  if file.endswith('.mxl'):
    print('Fixing', file)
    full_file_name = file[:-4]
    game_acronym, track_name, game_name = split_track_name(full_file_name)

    file_location = os.path.join(finale_scores_folder, file)
    new_file_location = os.path.join(modified_folder, file)
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
            percussion_to_non_percussion = set()
            percussion_sequence_parts = defaultdict(PercussionSequencePart)
            for part_info in xml_root.find('part-list').findall('score-part'):
              part_name = part_info.find('part-name').text
              instrument_name = get_instrument_name(part_name)
              program = None
              #print(item.filename, part_name)

              if full_score and instrument_name in mxl_manual_remap:
                print('Manually remap', instrument_name)

              midi_instruments = part_info.findall('midi-instrument')
              for midi_instrument in midi_instruments:
                midi_instrument.find('volume').text = '80'

              percussion = instrument_name in mxl_percussion_override
              if not percussion:
                for midi_instrument in midi_instruments:
                  midi_unpitched = midi_instrument.find('midi-unpitched')
                  if midi_unpitched is not None:
                    if instrument_name in mxl_percussion_to_non_percussion:
                      percussion_to_non_percussion.add(instrument_name)
                      midi_instrument.remove(midi_unpitched)
                    else:
                      percussion = True

              if percussion:
                for score_instrument in part_info.findall('score-instrument'):
                  instrument_name_element = score_instrument.find('instrument-name')
                  instrument_name_element.text = instrument_name_element.text.strip().replace('%g', '')
                if not instrument_name in ignore_unmapped_percussion:
                  percussion_instruments = {}
                  for score_instrument in part_info.findall('score-instrument'):
                    percussion_instruments[score_instrument.attrib['id']] = score_instrument.find('instrument-name').text
                  for midi_instrument in midi_instruments:
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
                      if instrument_name in percussion_sequence_mappings:
                        fill_percussion_sequence_parts(instrument_name, current_note, midi_unpitched, percussion_sequence_parts)
                      else:
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
                      instrument_sound = ElementTree.Element('instrument-sound')
                      score_instrument.insert(1, instrument_sound)
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

            for instrument_name, sequence_part in percussion_sequence_parts.items():
              for msg in sequence_part.messages:
                current_note = int(msg.text) - 1
                mapped_note = map_percussion_sequence_note(instrument_name, current_note, sequence_part)
                msg.text = str(mapped_note + 1)

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
              rim_shot = None
              bongo_slap = None
              unpitched_clef = False
              for measure in part.findall('measure'):
                measure_number = measure.attrib['number']

                print_page = measure.find('print')
                if print_page is not None and 'new-page' in print_page.attrib:
                  measure.remove(print_page)

                attributes = measure.find('attributes')
                if attributes is not None:
                  if transpose_offset != 0:
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

                  clef = attributes.find('clef')
                  if clef is not None:
                    staff_details = attributes.find('staff-details')
                    unpitched_clef = staff_details is not None and clef.find('sign').text == 'percussion' and staff_details.find('staff-lines') is not None

                  if instrument_name in percussion_to_non_percussion:
                    key_element = attributes.find('key')
                    if key_element is not None:
                      key_element.attrib['print-object'] = 'no'
                      key_element.find('fifths').text = '0'
                      key_element.find('mode').text = 'major'

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

                  for direction in measure.findall('direction'):
                    bracket = direction.find('direction-type').find('bracket')
                    if bracket is not None and bracket.attrib['type'] == 'start':
                      print('Found bracket in {}, measure {}.'.format(part_name, measure_number))

                tuplet_number = None
                tuplet_type = None
                for note in measure.findall('note'):
                  if unpitched_clef and instrument_name not in percussion_parts:
                    unpitched = note.find('unpitched')
                    if unpitched is not None:
                      display_step = unpitched.find('display-step')
                      display_octave = unpitched.find('display-octave')
                      if display_step.text == 'E' and display_octave.text == '4':
                        display_step.text = 'F'
                        display_octave.text = '5'
                      elif display_step.text == 'D' and display_octave.text == '4':
                        display_step.text = 'E'
                        display_octave.text = '5'
                      elif display_step.text == 'F' and display_octave.text == '4':
                        display_step.text = 'G'
                        display_octave.text = '5'

                  if instrument_name == 'Drum Set' and len(open_hi_hat_ids) > 1:
                    note_instrument = note.find('instrument')
                    if note_instrument is not None and note_instrument.attrib['id'] in open_hi_hat_ids:
                      unpitched = note.find('unpitched')
                      if unpitched is not None:
                        unpitched.find('display-step').text = 'G'
                        unpitched.find('display-octave').text = '5'

                  notehead = note.find('notehead')
                  if full_score and notehead is not None:
                    if rim_shot is None and (instrument_name == 'Drum Set' or instrument_name == 'Snare Drum') and notehead.text == 'back slashed':
                      rim_shot = measure_number
                    elif bongo_slap is None and instrument_name == 'Bongo Drums' and notehead.text == 'x':
                      bongo_slap = measure_number

                  notations = note.find('notations')
                  if notations is not None:
                    if full_score and not found_breath_mark:
                      articulations = notations.find('articulations')
                      if articulations is not None:
                        breath_mark = articulations.find('breath-mark')
                        if breath_mark is not None:
                          found_breath_mark = measure_number

                    time_modification = note.find('time-modification')
                    beams = note.findall('beam')
                    if len(beams) == 3 and time_modification is not None:
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
                        print('Found unknown tremolo {} {} in {}, measure {}.'.format(tuplet_number, tuplet_type, part_name, measure_number))

                    if full_score:
                      tied = notations.find('tied')
                      slur = notations.find('slur')
                      if tied is not None and slur is not None and tied.attrib['type'] == 'start' and slur.attrib['type'] == 'start':
                        print('Found combined slur/tie in {}, measure {}.'.format(part_name, measure_number))

                  cue = note.find('cue')
                  if cue is not None and note.find('grace') is None:
                    note.remove(cue)

                  if instrument_name in percussion_to_non_percussion:
                    instrument_element = note.find('instrument')
                    if instrument_element is not None:
                      note.remove(instrument_element)

                    unpitched_element = note.find('unpitched')
                    if unpitched_element is not None:
                      pitch_element = ElementTree.Element('pitch')
                      note.insert(0, pitch_element)
                      pitch_step = ElementTree.SubElement(pitch_element, 'step')
                      pitch_step.text = unpitched_element.find('display-step').text
                      pitch_octave = ElementTree.SubElement(pitch_element, 'octave')
                      pitch_octave.text = unpitched_element.find('display-octave').text
                      note.remove(unpitched_element)

                    if note.find('duration') is None:
                      duration = ElementTree.SubElement(note, 'duration')
                      duration.text = '1'

              if found_breath_mark is not None:
                print('Found breath mark in {}, measure {}.'.format(part_name, found_breath_mark))
              if rim_shot is not None:
                print('Found rim shot in {}, measure {}.'.format(part_name, rim_shot))
              if bongo_slap is not None:
                print('Found bongo slap in {}, measure {}.'.format(part_name, bongo_slap))

            newZip.writestr(item, xml_header + ElementTree.tostring(xml_root))
          else:
            newZip.writestr(item, origZip.read(item.filename))
    print('Saving file to', new_file_location)
