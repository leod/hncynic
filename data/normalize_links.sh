#!/bin/bash

sed -e 's#\[[^]]\+\](\([^)]\+\))#\1#g' -e 's#<\(http://[^>]*\)>#\1#g' -e 's#<\(https://[^>]*\)>#\1#g'
