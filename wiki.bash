#!/bin/bash

WIKI_PATH=.wiki/Home.md

for path in $(ls compass/compass-data/data/card/*.json); do
    num=$(echo ${path##*/} | sed "s/\.[^\.]*$//")
    if ! grep -q $num $WIKI_PATH; then
        name=$(cat $path | jq -r .name)
        rarity=$(cat $path | jq -r .rarity)
        attr=$(cat $path | jq -r .attribute)
        echo "| $num | $rarity | $attr | $name | |" >> $WIKI_PATH
    fi
done
