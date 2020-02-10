#! /bin/bash

# direcotry of the script (https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# if the above command doesn't work just hardcode the DIR-var

# cd into ffapi-updater dir
cd $DIR || exit

# activate venv
source venv/bin/activate

# run ffapi-updater
python3 ffapi-updater.py > ffapi-updater.log

# deactivate venv
deactivate

# only keep last 1000 lines of lof
echo "$(tail -1000 ffapi-updater.log)" > ffapi-updater.log