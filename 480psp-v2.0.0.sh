#!/bin/bash

# DEFAULT VALUES FOR THE VARIABLES USED ARE STORED HERE.
y=0
a=128
r=16
s=9
k=480
j=720

# Video bitrate change function
function vbitrate() { y=1; read -p "What bitrate for video? (kbps): " p; }

# Video File input function
function file_in() {
    local success="FALSE"
    until [[ "$success" == "TRUE" ]]; do
        read -p "Please enter location of input file: " i
        [[ "$i" == "~/"* ]] && i="/home/$(whoami)/${i:2}"
        if [[ ! -f "$i" ]]; then
            echo "ERROR: '$i': No such file. Please choose a valid video file."
        elif [[ "$(file -b --mime-type "$i")" != "video/"* ]]; then
            echo "ERROR: '$i' is not a valid video file."
        else
            success="TRUE"
        fi
    done
}

# Output file path function
function file_out() {
    local success="FALSE"
    until [[ "$success" == "TRUE" ]]; do
        read -p "Please enter location of output file: " o
        [[ "$o" == "~/"* ]] && o="/home/$(whoami)/${o:2}"
        if [[ ! -d "$(dirname "$o")" ]]; then
            echo "ERROR: '$(dirname "$o")' does not exist."
        elif [[ -f "$o" ]]; then
            echo "ERROR: '$o' already exists."
        else
            success="TRUE"
        fi
    done
}

# Factory function for creating presets
function preset_factory() {
    case "$1" in
        "F"|"f") a=128; r=4; s=3; k=240; j=320 ;;
        "0") a=256; r=16; s=9; k=480; j=720 ;;
        "1") a=192; r=16; s=9; k=480; j=720 ;;
        "2") a=160; r=16; s=9; k=480; j=720 ;;
        "3") a=128; r=16; s=9; k=480; j=720 ;;
        "4") a=256; r=4; s=3; k=480; j=640 ;;
        "5") a=192; r=4; s=3; k=480; j=640 ;;
        "6") a=160; r=4; s=3; k=480; j=640 ;;
        "7") a=128; r=4; s=3; k=480; j=640 ;;
        "8") a=256; r=16; s=9; k=272; j=480 ;;
        "9") a=192; r=16; s=9; k=272; j=480 ;;
        "A"|"a") a=160; r=16; s=9; k=272; j=480 ;;
        "B"|"b") a=128; r=16; s=9; k=272; j=480 ;;
        "C"|"c") a=256; r=4; s=3; k=240; j=320 ;;
        "D"|"d") a=192; r=4; s=3; k=240; j=320 ;;
        "E"|"e") a=160; r=4; s=3; k=240; j=320 ;;
        *) echo "Invalid preset. Using default values." ;;
    esac
}

# Function that creates the command
function create_command() {
    if [[ "$y" == "1" ]]; then
        cmd="ffmpeg -i ${i} -vcodec libx264 -b:v ${p}k -s ${j}x${k} -aspect ${r}:${s} -profile:v main -level:v 2.1 -x264-params ref=3:bframes=1 -acodec aac -b:a ${a}k -ac 2 -movflags +faststart ${o}"
    else
        cmd="ffmpeg -i ${i} -vcodec libx264 -s ${j}x${k} -aspect ${r}:${s} -profile:v main -level:v 2.1 -x264-params ref=3:bframes=1 -acodec aac -b:a ${a}k -ac 2 -movflags +faststart ${o}"
    fi
    echo "Generated command: $cmd"
    read -p "Would you like to run this command now? [y/N]: " run_cmd_now
    if [[ "$run_cmd_now" == "Y" ]] || [[ "$run_cmd_now" == "y" ]]; then
        echo "RUNNING COMMAND..."
        eval "$cmd"
    fi
}

# Main script execution starts here
echo "
PSP ffmpeg Encoder Script 1.3
Refactored with Factory Design Pattern
"

if [[ "$1" == "help" ]] || [[ "$1" == "--help" ]]; then
    echo "Available functions:
    file_in: Select input file
    file_out: Select output file
    preset_factory: Select preset configuration
    create_command: Generate and run the ffmpeg command"
else
    file_in
    file_out
    read -p "Would you like to enter advanced mode? [y/N]: " advanced_mode
    if [[ "$advanced_mode" == "Y" ]] || [[ "$advanced_mode" == "y" ]]; then
        read -p "Set video bitrate? [y/N]: " v_bit
        [[ "$v_bit" == "Y" || "$v_bit" == "y" ]] && vbitrate
        read -p "Choose a preset (e.g., 0, 1, A, B): " preset
        preset_factory "$preset"
    fi
    create_command
fi
