#!/bin/bash

#CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
CURRENT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

UBT=$UE4_ROOT/Engine/Build/BatchFiles/Linux/Build.sh
SCRIPT=$CURRENT_DIR/GenerateQtProject.py 
relative=false
build=true
add='%s'

while getopts ":p:b:a:r:" opt; do
  case $opt in
    p) project="$OPTARG"
    ;;
    b) build="$OPTARG"
    ;;
    a) add="$OPTARG"
    ;;
    r) relative="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
    :) echo "Option -$OPTARG requires an argument." >&2
    exit 1
    ;;
  esac
done

if [[ $project =~ \.uproject$ ]];then
    printf "file project found: %s\n" "$project"
    PROJECT_PATH="$(cd "$( dirname "$project" )" && pwd )"
    printf "Project path: %s\n" $PROJECT_PATH
else
    printf "UE4 file project not found\n"
    exit 1;
fi

if [ ! -f $PROJECT_PATH/CMakeLists.txt ];then
$UBT -makefile -project=$project -game -engine -progress
fi

python3 $SCRIPT -e $UE4_ROOT -p $project -b $build -a $add -r $relative -d $CURRENT_DIR

#if [ -z "$relative" ];then
#    python3 $SCRIPT -e $UE4_ROOT -p $project -b $build -a $add
#else
#    python3 $SCRIPT -e $UE4_ROOT -p $project -b $build -a $add -r $relative
#fi 


printf "UE4QtCreator SUCCESS!!\n"

exit 0
