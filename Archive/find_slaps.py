from finale_remap import *
from game_acronyms import *
from file_locations import *
import os;
import zipfile
import xml.etree.ElementTree as ElementTree

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

              slap_parts = []
              parts = {}
              for part_info in xml_root.find('part-list').findall('score-part'):
                part_name = part_info.find('part-name').text
                instrument_name = get_instrument_name(part_name)
                parts[part_info.attrib['id']] = part_name

              for part in xml_root.findall('part'):
                part_name = parts[part.attrib['id']]

                found_slap = False
                if 'Bass' in part_name:
                  for measure in part.findall('measure'):
                    measure_number = measure.attrib['number']
                    for direction in measure.findall('direction'):
                      direction_type = direction.find('direction-type')
                      words = direction_type.find('words')
                      if words is not None and ('Slap' in words.text or 'Pick' in words.text):
                        found_slap = True
                        print('Found {} in {}, measure {}'.format(words.text, part_name, measure_number))
                if found_slap:
                  slap_parts.append(part_name)

              if len(slap_parts) > 0:
                print(full_file_name, slap_parts)
