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
  'MBP': 'Marble Blast Platinum',
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
  'NSLT': 'New Super Lucky\'s Tale',
  'NSMBU': 'New Super Mario Bros U',
  'NSMBW': 'New Super Mario Bros Wii',
  'ORAS': 'Pokemon Omega Ruby Alpha Sapphire',
  'OSRS': 'Old School RuneScape',
  'Pt': 'Pokemon Platinum',
  'RS': 'RuneScape',
  'RSE': 'Pokemon Ruby Sapphire',
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
  'NSMBU': 'New Super Mario Bros. U',
  'NSMBW': 'New Super Mario Bros. Wii',
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
  'MRSOH Phantom Razzmatazz': 'Phantom, Razzmatazz',
  'MRSOH Phantom The Diva Delivers': 'Phantom, The Diva Delivers',
  'MRSOH Root of Corruption Pt I': 'Root of Corruption, Pt. I',
  'MRSOH Root of Corruption Pt II': 'Root of Corruption, Pt. II',
  'NSMBW Lava Cave Underground Ruins Theme': 'Lava Cave   Underground Ruins Theme',
  'ORAS Mt Pyre': 'Mt. Pyre',
  'ORAS Mt Pyre Exterior': 'Mt. Pyre Exterior',
  'RSE Mt Chimney': 'Mt. Chimney',
  'RSE Mt Pyre Exterior': 'Mt. Pyre Exterior',
  'SMD Air Continent Baram Town': 'Air Continent: Baram Town',
  'SMD Boss Battle Children\'s Adventure!': 'Boss Battle: Children\'s Adventure!',
  'SMD Boss Battle Expedition Society Fight': 'Boss Battle: Expedition Society Fight',
  'SMD Grass Continent Capim Town': 'Grass Continent: Capim Town',
  'SMD Legendary Boss Battle Rock Version!': 'Legendary Boss Battle: Rock Version!',
  'SMD Onward Expedition Society!': 'Onward, Expedition Society!',
  'SMD Tree of Life Roots': 'Tree of Life: Roots',
}

special_track_game_names = {
  'BBT PDA Game': 'Alien Hominid',
  'NSLT Fretting Yeti': 'Super Lucky\'s Tale',
  'OSRS Assault and Battery': 'RuneScape 2',
  'OSRS Darkmeyer': 'Old School RuneScape',
  'OSRS Ready for Battle': 'RuneScape 2',
  'OSRS Roots and Flutes': 'Old School RuneScape',
  'OSRS Scape Soft': 'RuneScape 2',
  'RS A Pirate\'s Life for Me': 'RuneScape 3',
  'RS Alone': 'RuneScape 3',
  'RS Assault and Battery': 'RuneScape 3',
  'RS Assault and Battery (original)': 'RuneScape HD',
  'RS Attack I': 'RuneScape 3',
  'RS Attack II': 'RuneScape 3',
  'RS Attack III': 'RuneScape 3',
  'RS Attack IV': 'RuneScape 3',
  'RS Attack V': 'RuneScape 3',
  'RS Attack VI': 'RuneScape 3',
  'RS Battle of Souls (original)': 'RuneScape HD',
  'RS Big Chords': 'RuneScape 3',
  'RS Castle Wars': 'RuneScape 3',
  'RS Dagannoth Dawn': 'RuneScape 3',
  'RS Dance of the Undead': 'RuneScape 3',
  'RS Dominion Tower I (original)': 'RuneScape HD',
  'RS Dominion Tower I': 'RuneScape 3',
  'RS Dominion Tower II (original)': 'RuneScape HD',
  'RS Dominion Tower II': 'RuneScape 3',
  'RS Dominion Tower IV (original)': 'RuneScape HD',
  'RS Dominion Tower V (original)': 'RuneScape HD',
  'RS Dominion Tower V': 'RuneScape 3',
  'RS Dragontooth Island': 'RuneScape 3',
  'RS Eruption (original)': 'RuneScape HD',
  'RS Exposed': 'RuneScape 3',
  'RS Fight or Flight': 'RuneScape 3',
  'RS Have an Ice Day': 'RuneScape 3',
  'RS Horizon': 'RuneScape 3',
  'RS Insect Queen': 'RuneScape 3',
  'RS Jungle Hunt': 'RuneScape 3',
  'RS Karamja Jam': 'RuneScape 3',
  'RS Labyrinth': 'RuneScape 3',
  'RS Mellow': 'RuneScape 3',
  'RS Monster Melee': 'RuneScape 3',
  'RS Newbie Melody': 'RuneScape 3',
  'RS Null and Void': 'RuneScape 3',
  'RS On the Wing': 'RuneScape 3',
  'RS Pathways': 'RuneScape 3',
  'RS Pest Control': 'RuneScape 3',
  'RS Ready for Battle': 'RuneScape 3',
  'RS Ready for Battle (original)': 'RuneScape HD',
  'RS Roots and Flutes': 'RuneScape 2',
  'RS Scape Soft': 'RuneScape HD',
  'RS Sojourn': 'RuneScape HD',
}

drive_path_omit_suffix = set([
  'RS Roots and Flutes',
  'RS Scape Soft',
  'RS Sojourn',
])

def get_game_name(game_acronym: str, full_track_name: str):
  if full_track_name in special_track_game_names:
    return special_track_game_names[full_track_name]
  if game_acronym == 'RS' and full_track_name.endswith('(original)'):
    return 'RuneScape 2'
  return game_acronyms[game_acronym]

def split_track_name(full_track_name: str):
  if full_track_name.startswith('FO '):
    split = full_track_name.split(' ', 2)
    game_acronym = split[0] + ' ' + split[1]
    track_name = split[2]
  else:
    split = full_track_name.split(' ', 1)
    if len(split) < 2:
      return (None, None, None)
    game_acronym = split[0]
    track_name = split[1]

    if game_acronym == 'RS' and track_name.endswith('(original)'):
      track_name = track_name.replace(' (original)', '')
  return (game_acronym, track_name, get_game_name(game_acronym, full_track_name))

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
    drive_folder = get_game_name(game_acronym, full_name)
  drive_folder = drive_folder.replace('Pokemon', 'Pokémon')
  if 'RuneScape' in drive_folder:
    drive_folder = 'RuneScape'

  return drive_track_name, drive_folder
