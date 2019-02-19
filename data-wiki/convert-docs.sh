#!/bin/bash

while read doc
do
  echo $doc
  cat $doc \
    | perl -pe 'BEGIN{undef $/;} s#<gallery>.*</gallery>##s' \
    | pandoc --wrap=none -f mediawiki -t markdown \
    | pandoc --filter filter_markdown.py -t markdown \
    > $doc.md
done
