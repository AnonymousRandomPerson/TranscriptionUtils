# <orig_video> <start_time> <orig_audio> <final_name>

set -e

while getopts s:t:e:u: option
do
	case "${option}"
		in
		s) file_1=${OPTARG};;
		t) time_1=${OPTARG};;
		e) file_2=${OPTARG};;
		u) time_2=${OPTARG};;
	esac
done

file_1=/Users/chenghanngan/Movies/OBS/"$file_1".mov
file_2=/Users/chenghanngan/Movies/OBS/"$file_2".mov
cut_file_1=/Users/chenghanngan/Movies/OBS/temp1.mov
cut_file_2=/Users/chenghanngan/Movies/OBS/temp2.mov
file_list=/Users/chenghanngan/Movies/OBS/temp.txt
output_name=/Users/chenghanngan/Movies/OBS/spliced.mov

echo "${file_1}"
echo "${time_1}"
echo "${file_2}"
echo "${time_2}"
echo "${output_name}"

RED='\033[0;31m'
if [ ! -f "$file_1" ]; then
    echo "${RED}\"$file_1\" does not exist."
    exit 1
fi

if [ ! -f "$file_2" ]; then
    echo "${RED}\"$file_2\" does not exist."
    exit 1
fi

# Cut first file up to time 1.
ffmpeg -i "$file_1" -ss 0 -async 1 -t $time_1 "$cut_file_1"

# Cut second file from time 2 onwards.
ffmpeg -i "$file_2" -ss $time_2 -async 1 "$cut_file_2"

echo "file '$cut_file_1'\nfile '$cut_file_2'" >> "$file_list"

# Splice two cut videos together.
ffmpeg -f concat -safe 0 -i "$file_list" -c copy "$output_name"

trash "$cut_file_1"
trash "$cut_file_2"
trash "$file_list"