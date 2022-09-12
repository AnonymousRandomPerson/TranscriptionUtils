def fix_custom(combined_name, msg, instrument_name):
  if instrument_name == 'Harp' and hasattr(msg, 'note') and msg.note == 2:
    msg.velocity = 0
