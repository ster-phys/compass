#!/bin/bash

WIKI_PATH=.wiki/Home.md
ABBS_JSON=compass/data/abbs.json

json="{ "

while read line; do
    if [[ $line =~ ^\|\ ([0-9]{6,})\ \|\ [NRSU]{1,2}\ \|\ .\ \|\ .+\ \|\ (.*)\ \|$ ]]; then
        json="$json\"${BASH_REMATCH[1]}\":[\"${BASH_REMATCH[2]//, /\",\"}\"],"
    fi
done < $WIKI_PATH

json=${json/%?/}}

echo $json | jq "." > $ABBS_JSON
