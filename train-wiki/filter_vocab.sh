#!/bin/bash

# IDK

grep -vP '[\p{Han}]' vocab.no-new.comments \
  | grep -vP '[\p{Hiragana}]' \
  | grep -vP '[\p{Katakana}]' \
  | grep -vP '[\p{Hebrew}]' \
  | grep -vP '[\p{Cyrillic}]' \
  | grep -vP '[\p{Arabic}]' 
