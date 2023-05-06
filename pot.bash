#!/bin/bash

if [[ ! $(ls | grep pot.bash) ]]; then
    echo "Error: Move to the directory where pot.bash is located."
    exit 1
fi

PYTHON=$(which python3.10)

for file in ./compass/*.py; do
    basename=${file##*/}
    domain=${basename%.*}

    # creates .po files
    $PYTHON i18n/pygettext.py -d $domain -p compass/locale $file
done
