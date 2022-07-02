import os
import binascii

base_path = os.path.join(os.sep, 'Users', 'chenghanngan', 'Documents', 'Programs', 'Reverse Engineering', 'Support', 'Adventure Squad WAD', 'Pokemon Fushigi no Dungeon - Ikuzo! Arashi no Boukendan (Japan) (WiiWare)', '00000002_app_OUT', 'content')

file_names = [
  'dun_boss.smd',
  'dun_bossfloor.smd',
  'dun_mount_1.smd',
  'dun_mount_2.smd',
  'dun_mount.smd',
  'endroll.smd',
  'ev_1.smd',
  'ev_2.smd',
  'ev_3.smd',
  'ev_4.smd',
  'ev_5.smd',
  'ev_ed.smd',
  'ev_fear.smd',
  'ev_op.smd',
  'gameclear.smd',
  'gameover.smd',
  'me_dunopen.smd',
  'me_evolution_e.smd',
  'me_evolution.smd',
  'me_exclude.smd',
  'me_item.smd',
  'me_join.smd',
  'me_lankup.smd',
  'me_lvup.smd',
  'me_reward.smd',
  'me_system.smd',
  'me_wave_m.smd',
  'me_wave_s.smd',
  'me_wind_m.smd',
  'me_wind_s.smd',
  'no_sound.smd',
  'sys_bazar.smd',
  'sys_clear.smd',
  'sys_map.smd',
  'sys_menu.smd',
  'sys_monster.smd',
  'sys_shop.smd',
  'sys_steal.smd'
]

def flip_bytes(data, offset, count):
  for i in range(count // 2):
    start = offset + i
    end = offset + count - i - 1
    temp = data[start]
    data[start] = data[end]
    data[end] = temp

for file_name in file_names:
  file_path = os.path.join(base_path, file_name)
  with open(file_path, 'rb') as smd_file:
    data = bytearray(smd_file.read())

  data[3] = 0x6C

  flip_bytes(data, 0x8, 4)
  flip_bytes(data, 0xC, 2)
  flip_bytes(data, 0xE, 2)
  flip_bytes(data, 0x30, 2)
  flip_bytes(data, 0x46, 2)
  flip_bytes(data, 0x4C, 4)
  flip_bytes(data, 0x50, 2)
  flip_bytes(data, 0x52, 2)
  flip_bytes(data, 0x62, 2)
  flip_bytes(data, 0x64, 2)
  flip_bytes(data, 0x66, 2)
  for i in range(0x84, len(data), 4):
    if data[i : i + 4] == bytearray([0, 0, 1, 0]):
      flip_bytes(data, i + 2, 2)
      flip_bytes(data, i + 8, 4)

  new_file_path = os.path.join(base_path, 'Modified', file_name)
  with open(new_file_path, 'wb+') as new_file:
    new_file.write(data)

