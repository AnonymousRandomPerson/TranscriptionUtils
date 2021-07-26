# <orig_video> <start_time> <orig_audio> <final_name>

set -e

orig_video_suffix=$1
orig_video=/Users/chenghanngan/Movies/OBS/"$orig_video_suffix".mov

start_time=00:00:$2

orig_audio_suffix=$3
orig_audio=/Users/chenghanngan/Documents/Programs/iOS/LoopMusic/Tracks/"$orig_audio_suffix".m4a

final_name_suffix=$4
if [ -z "$final_name_suffix" ]; then
    final_name_suffix=$3
fi
final_name=/Users/chenghanngan/Documents/Music/Transcription/Videos/"$final_name_suffix".mp4
final_name_delayed=/Users/chenghanngan/Documents/Music/Transcription/Videos/"$final_name_suffix"\ delayed.mp4

fade_out_time=3

fade=true
if [ $fade_out_time = 0 ]; then
    fade=false
fi

cut_temp_file=/Users/chenghanngan/Documents/Music/Transcription/Videos/temp.mp4

splice_output=/Users/chenghanngan/Documents/Music/Transcription/Videos/temp2.mp4

if [ "$fade" = false ]; then
    splice_output="$final_name"
fi

valid=true
RED='\033[0;31m'

if [ ! -f "$orig_video" ]; then
    echo "${RED}\"$orig_video_suffix\" does not exist."
    valid=false
fi

if [ ! -f "$orig_audio" ]; then
    echo "${RED}\"$orig_audio_suffix\" does not exist."
    valid=false
fi

if [ "$valid" = true ]; then

    ffmpeg -i "$orig_video" -ss $start_time -async 1 "$cut_temp_file"

    ffmpeg -i "$cut_temp_file" -i "$orig_audio" -c:v copy -c:a aac -shortest -map 0:v:0 -map 1:a:0 "$splice_output"

    if [ "$fade" = true ]; then
        video_length=`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$splice_output"`
        fade_start=`echo "$video_length - $fade_out_time" | bc`

        ffmpeg -i "$splice_output" -af 'afade=out:st='$fade_start':d='$fade_out_time "$final_name"

        trash "$splice_output"
    fi

    # ffmpeg -i "$final_name" -itsoffset 0.3 -i "$final_name" -map 0:v -map 1:a -vcodec copy -acodec copy "$final_name_delayed"

    trash "$cut_temp_file"

fi