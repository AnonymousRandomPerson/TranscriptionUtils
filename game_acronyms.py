import os

game_acronyms = {
  'AM': 'Kirby & the Amazing Mirror',
  'B2W2': 'Pokemon Black White 2',
  'BB': 'Kirby\'s Blowout Blast',
  'BBT': 'BattleBlock Theater',
  'BDSP': 'Pokemon Brilliant Diamond Shining Pearl',
  'BIS': 'Mario & Luigi Bowser\'s Inside Story',
  'BISBJJ': 'Mario & Luigi Bowser\'s Inside Story Bowser Jr\'s Journey',
  'BR': 'Pokemon Battle Revolution',
  'BW': 'Pokemon Black White',
  'C': 'Pokemon Colosseum',
  'COH': 'Cadence of Hyrule',
  'CS': 'Paper Mario Color Splash',
  'CT': 'Chrono Trigger',
  'CTTT': 'Captain Toad Treasure Tracker',
  'CW': 'Yoshi\'s Crafted World',
  'DL3': 'Kirby\'s Dream Land 3',
  'DPP': 'Pokemon Diamond Pearl',
  'DR': 'Deltarune',
  'DT': 'Mario & Luigi Dream Team',
  'E': 'Pokemon Emerald',
  'EB': 'EarthBound',
  'EY': 'Kirby\'s Epic Yarn',
  'FL': 'Kirby and the Forgotten Land',
  'FO BD': 'Bouncedown',
  'FO CC': 'Crazy Crystals',
  'FO DB': 'Deko Bloko',
  'FO EV': 'Escape Vector',
  'FO G': 'Geoblox',
  'FO MD': 'Miner Disturbance',
  'FO OD': 'Orb Defence',
  'FO SC': 'StarCannon',
  'FRLG': 'Pokemon FireRed LeafGreen',
  'HGSS': 'Pokemon HeartGold SoulSilver',
  'ITM': 'Sid & Al\'s Incredible Toons',
  'IWBTG': 'Guilty Gear Isuka',
  'K64': 'Kirby 64 The Crystal Shards',
  'KSSq': 'Kirby Squeak Squad',
  'KSSt': 'Kirby Super Star',
  'LA': 'Pokemon Legends Arceus',
  'LF2': 'Little Fighter 2',
  'LGPE': 'Pokemon Let\'s Go Pikachu Eevee',
  'LTTP': 'The Legend of Zelda A Link to the Past',
  'MBG': 'Marble Blast Gold',
  'MBP': 'PlatinumQuest',
  'MDB': 'Pokemon Mystery Dungeon Blue Rescue Team',
  'MDBSL': 'Pokemon Mystery Dungeon Blazing Stormy Light Adventure Squad',
  'MDGTI': 'Pokemon Mystery Dungeon Gates to Infinity',
  'MDR': 'Pokemon Mystery Dungeon Red Rescue Team',
  'MDRTDX': 'Pokemon Mystery Dungeon Rescue Team DX',
  'MDS': 'Pokemon Mystery Dungeon Explorers of Sky',
  'MDTDS': 'Pokemon Mystery Dungeon Explorers of Time Darkness',
  'MK8': 'Mario Kart 8',
  'MK8D': 'Mario Kart 8 Deluxe',
  'MKDS': 'Mario Kart DS',
  'MLSS': 'Mario & Luigi Superstar Saga',
  'MLSSBM': 'Mario & Luigi Superstar Saga Bowser\'s Minions',
  'MPDS': 'Mario Party DS',
  'MRKB': 'Mario Rabbids Kingdom Battle',
  'MRSOH': 'Mario Rabbids Sparks of Hope',
  'NID': 'Kirby Nightmare in Dream Land',
  'Pt': 'Pokemon Platinum',
  'SMD': 'Pokemon Super Mystery Dungeon',
}

drive_folders = {
  'BIS': 'Mario & Luigi: Bowser\'s Inside Story',
  'BISBJJ': 'Mario & Luigi: Bowser\'s Inside Story + Bowser Jr.\'s Journey',
  'CS': 'Paper Mario: Color Splash',
  'CTTT': 'Captain Toad: Treasure Tracker',
  'DT': 'Mario & Luigi: Dream Team',
  'FO BD': os.path.join('FunOrb', 'Bouncedown'),
  'FO CC': os.path.join('FunOrb', 'Crazy Crystals'),
  'FO DB': os.path.join('FunOrb', 'Deko Bloko'),
  'FO EV': os.path.join('FunOrb', 'Escape Vector'),
  'FO G': os.path.join('FunOrb', 'Geoblox'),
  'FO MD': os.path.join('FunOrb', 'Miner Disturbance'),
  'FO OD': os.path.join('FunOrb', 'Orb Defence'),
  'FO SC': os.path.join('FunOrb', 'StarCannon'),
  'IWBTG': 'Guilty Gear Isuka',
  'K64': 'Kirby 64: The Crystal Shards',
  'KSSq': 'Kirby: Squeak Squad',
  'LA': 'Pokemon Legends: Arceus',
  'LGPE': 'Pokemon: Let\'s Go, Pikachu Eevee!',
  'LTTP': 'The Legend of Zelda: A Link to the Past',
  'MDB': 'Pokemon Mystery Dungeon: Blue Rescue Team',
  'MDBSL': 'Pokemon Mystery Dungeon: Blazing Stormy Light Adventure Squad',
  'MDGTI': 'Pokemon Mystery Dungeon: Gates to Infinity',
  'MDR': 'Pokemon Mystery Dungeon: Red Rescue Team',
  'MDRTDX': 'Pokemon Mystery Dungeon: Rescue Team DX',
  'MDS': 'Pokemon Mystery Dungeon: Explorers of Sky',
  'MDTDS': 'Pokemon Mystery Dungeon: Explorers of Time Darkness',
  'MLSS': 'Mario & Luigi: Superstar Saga',
  'MLSSBM': 'Mario & Luigi: Superstar Saga + Bowser\'s Minions',
  'MRKB': 'Mario + Rabbids: Kingdom Battle',
  'MRSOH': 'Mario + Rabbids: Sparks of Hope',
  'NID': 'Kirby: Nightmare in Dream Land',
}

special_track_names = {
  'B2W2 Filming Underway at Pokestar Studios!': 'Filming Underway at Pokéstar Studios!',
  'B2W2 Pokestar Studios Battle': 'Pokéstar Studios: Battle',
  'B2W2 Pokestar Studios Horror': 'Pokéstar Studios: Horror',
  'B2W2 Pokestar Studios Weird': 'Pokéstar Studios: Weird',
  'BDSP Mt Coronet': 'Mt. Coronet',
  'C Battle! (Miror B)': 'Battle! (Miror B.)',
  'DL3 Ripple Field Ocean Waves': 'Ripple Field: Ocean Waves',
  'DPP Mt Coronet': 'Mt. Coronet',
  'DR A CYBER\'S WORLD': 'A CYBER\'S WORLD?',
  'DT Try Try Again': 'Try, Try Again',
  'FL Burning Churning Power Plant': 'Burning, Churning Power Plant',
  'FRLG Road to Cerulean City Leaving Mt Moon': 'Road to Cerulean City: Leaving Mt. Moon',
  'FRLG Road to Fuschia City Leaving Lavender Town': 'Road to Fuschia City: Leaving Lavender Town',
  'HGSS Pokegear Radio Route 201': 'Pokégear Radio: Route 201',
  'HGSS SS Aqua': 'S.S. Aqua',
  'LA Mt Coronet': 'Mt. Coronet',
  'LGPE Road to Cerulean City Leaving Mt Moon': 'Road to Cerulean City: Leaving Mt. Moon',
  'LGPE Road to Lavender Town Leaving Vermilion City': 'Road to Lavender Town: Leaving Vermilion City',
  'LGPE Road to Viridian City Leaving Pallet Town': 'Road to Viridian City: Leaving Pallet Town',
  'MDB Mt Blaze': 'Mt. Blaze',
  'MDB Mt Blaze Peak': 'Mt. Blaze Peak',
  'MDB Mt Freeze': 'Mt. Freeze',
  'MDB Mt Steel': 'Mt. Steel',
  'MDB Mt Thunder': 'Mt. Thunder',
  'MDGTI Pokemon Friends Arrangement': 'Pokémon Friends: Arrangement',
  'MDGTI Stirrings of Hope March': 'Stirrings of Hope: March',
  'MDGTI Stop Thief!': 'Stop, Thief!',
  'MDR Mt Blaze': 'Mt. Blaze',
  'MDR Mt Blaze Peak': 'Mt. Blaze Peak',
  'MDR Mt Freeze': 'Mt. Freeze',
  'MDR Mt Steel': 'Mt. Steel',
  'MDR Mt Thunder': 'Mt. Thunder',
  'MDRTDX Mt Blaze': 'Mt. Blaze',
  'MDRTDX Mt Blaze Peak': 'Mt. Blaze Peak',
  'MDRTDX Mt Freeze': 'Mt. Freeze',
  'MDRTDX Mt Steel': 'Mt. Steel',
  'MDRTDX Mt Thunder': 'Mt. Thunder',
  'MDTDS Mt Bristle': 'Mt. Bristle',
  'MDTDS Mt Horn': 'Mt. Horn',
  'MDTDS Mt Travail': 'Mt. Travail',
  'MRKB Cold Start Hot Finish': 'Cold Start, Hot Finish',
  'MRKB Hot Start Cold Finish': 'Hot Start, Cold Finish',
  'MRSOH Cold Dark Mask of the Mountain Pt I': 'Cold, Dark Mask of the Mountain, Pt. I',
  'MRSOH Daphne\'s Trap Pt I': 'Daphne\'s Trap, Pt. I',
  'MRSOH For the Galaxy! Pt I': 'For the Galaxy! Pt. I',
  'MRSOH For the Galaxy! Pt II': 'For the Galaxy! Pt. II',
  'MRSOH Root of Corruption Pt I': 'Root of Corruption, Pt. I',
  'MRSOH Root of Corruption Pt II': 'Root of Corruption, Pt. II',
  'SMD Air Continent Baram Town': 'Air Continent: Baram Town',
  'SMD Boss Battle Children\'s Adventure!': 'Boss Battle: Children\'s Adventure!',
  'SMD Boss Battle Expedition Society Fight': 'Boss Battle: Expedition Society Fight',
  'SMD Grass Continent Capim Town': 'Grass Continent: Capim Town',
  'SMD Legendary Boss Battle Rock Version!': 'Legendary Boss Battle: Rock Version!',
  'SMD Onward Expedition Society!': 'Onward, Expedition Society!',
  'SMD Tree of Life Roots': 'Tree of Life: Roots',
}

def split_track_name(track_name: str):
  if track_name.startswith('FO '):
    split = track_name.split(' ', 2)
    game_acronym = split[0] + ' ' + split[1]
    track_name = split[2]
  else:
    split = track_name.split(' ', 1)
    if len(split) < 2:
      return (None, None, None)
    game_acronym = split[0]
    track_name = split[1]
  return (game_acronym, track_name, game_acronyms[game_acronym])

def get_drive_track_name(game_acronym: str, track_name: str):
  full_name = game_acronym + ' ' + track_name
  if full_name in special_track_names:
    drive_track_name = special_track_names[full_name]
  else:
    drive_track_name = track_name
  drive_track_name = drive_track_name.replace('Pokemon', 'Pokémon')

  if game_acronym in drive_folders:
    drive_folder = drive_folders[game_acronym]
  else:
    drive_folder = game_acronyms[game_acronym]
  drive_folder = drive_folder.replace('Pokemon', 'Pokémon')

  return drive_track_name, drive_folder
