#!/bin/bash

mydir=$(dirname $BASH_SOURCE)

tokenize() {
  $mydir/normalize_links.sh | $mydir/../mosesdecoder/scripts/tokenizer/tokenizer.perl -protected $mydir/moses_tokenizer_protected.txt -no-escape
}

cut -f4 $1.tsv | tokenize > $1.tok.comments
cut -f3 $1.tsv | tokenize > $1.tok.titles
