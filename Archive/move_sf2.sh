# <dest_path> <converted_path> <dest_name>

set -e

dest_path_suffix=$1
dest_path=/Users/chenghanngan/Library/Audio/Sounds/Banks/"$dest_path_suffix"

converted_path_suffix=$2
converted_path=/Users/chenghanngan/Library/Audio/Sounds/Banks/Sforzando/ARIAConverted/sf2/"$converted_path_suffix"_sf2

dest_name=$3

if [ -z "$dest_name" ]; then
	dest_name="${2//_/ }"
	sed_remove_underscores=s/_/\ /g
	dest_name=`echo "$dest_name" | sed -e "$sed_remove_underscores"`
fi

dest_sfz="$dest_path"/"$dest_name".sfz
dest_wav="$dest_path"/Wav/"$dest_name".wav

converted_sfz=`ls "$converted_path" | grep '^000_.\+\.sfz$'`

converted_sfz="$converted_path"/"$converted_sfz"
converted_wav="$converted_path"/../sf2_smpl.wav

sed_replace_wav_name=s/sf2_smpl\.wav/Wav\\/"$dest_name"\\.wav/g

sed -i -e "$sed_replace_wav_name" "$converted_sfz"

mv "$converted_sfz" "$dest_sfz"
mv "$converted_wav" "$dest_wav"

trash "$converted_path"