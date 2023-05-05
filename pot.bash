#!/bin/bash

if [[ ! $(ls | grep po.bash) ]]; then
    echo "Error: Move to the directory where po.bash is located."
fi

PYTHON=$(which python3.10)

for file in ./compass/*.py; do
    basename=${file##*/}
    domain=${basename%.*}

    # creates .po files
    $PYTHON i18n/pygettext.py -d $domain -p compass/locale $file

    # copys to LC_MESSAGES
    cp compass/locale/$domain.pot compass/locale/en/LC_MESSAGES/$domain.po
    cp compass/locale/$domain.pot compass/locale/ja/LC_MESSAGES/$domain.po
    cp compass/locale/$domain.pot compass/locale/zh-TW/LC_MESSAGES/$domain.po
done
