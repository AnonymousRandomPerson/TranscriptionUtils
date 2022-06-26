from finale_remap import *
from game_acronyms import *
import os;
import zipfile
import xml.etree.ElementTree as ElementTree

parts_folder = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Music', 'Transcription', 'Parts')

for folder in sorted(os.listdir(parts_folder)):
  folder = os.path.join(parts_folder, folder)
  if os.path.isdir(folder):
    for file in os.listdir(folder):
      if file.endswith('.mxl'):
        full_file_name = file[:-4]

        file_location = os.path.join(folder, file)
        with zipfile.ZipFile(file_location, 'r') as origZip:
          for item in origZip.infolist():
            if item.filename.endswith('.musicxml') and not item.filename.startswith('p'):
              full_score = item.filename.startswith(full_file_name)

              xml_string = origZip.read(item)
              xml_root = ElementTree.fromstring(xml_string)

              breath_mark_parts = []
              parts = {}
              for part_info in xml_root.find('part-list').findall('score-part'):
                part_name = part_info.find('part-name').text
                instrument_name = get_instrument_name(part_name)
                parts[part_info.attrib['id']] = part_name

              for part in xml_root.findall('part'):
                part_name = parts[part.attrib['id']]

                found_breath_mark = False
                for measure in part.findall('measure'):
                  measure_number = measure.attrib['number']
                  for note in measure.findall('note'):
                    notations = note.find('notations')
                    if notations is not None:
                      articulations = notations.find('articulations')
                      if articulations is not None:
                        breath_mark = articulations.find('breath-mark')
                        if breath_mark is not None:
                          found_breath_mark = True
                          break
                  if found_breath_mark:
                    break
                if found_breath_mark:
                  breath_mark_parts.append(part_name)

              if len(breath_mark_parts) > 0:
                print(full_file_name, breath_mark_parts)

