#!/bin/bash

DEV_SIZE=2000
TEST_SIZE=$DEV_SIZE

# https://stackoverflow.com/questions/5914513/shuffling-lines-of-a-file-with-a-fixed-seed
get_seeded_random()
{
  seed="$1"
    openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}

tmp=`mktemp`

shuf --random-source=<(get_seeded_random 42) > "$tmp"

head -n $DEV_SIZE "$tmp" > "$1".dev.tsv
tail -n +$(( DEV_SIZE+1 )) "$tmp" | head -n $TEST_SIZE > "$1".test.tsv
tail -n +$(( DEV_SIZE+TEST_SIZE+1 )) "$tmp" > "$1".train.tsv
