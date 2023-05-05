#!/bin/bash

if [[ ! $(ls | grep mo.bash) ]]; then
    echo "Error: Move to the directory where mo.bash is located."
fi

PYTHON=$(which python3.10)

# creates .mo files
$PYTHON i18n/msgfmt.py compass/locale/*/LC_MESSAGES/*.po
