import os

directory = '/Users/chenghanngan/Library/Audio/Sounds/Banks/Pokémon Black and White'
for file_name in os.listdir(directory):
    if file_name.endswith('sfz'):
        file_name = directory + '/' + file_name
        with open(file_name, 'r') as sfz_file:
            sfz = sfz_file.read()

        current_index = 0
        END = ' end='
        LOOP_END = ' loop_end='
        while current_index > -1:
            current_index = sfz.find(END, current_index)
            if current_index > -1:
                loop_end = int(sfz[current_index + len(END) : sfz.find('\n', current_index)]) - 1
                current_index = sfz.find(LOOP_END, current_index)
                sfz = sfz[:current_index] + LOOP_END + str(loop_end) + sfz[sfz.find('\n', current_index):]

        with open(file_name, 'w') as sfz_file:
            sfz_file.write(sfz)