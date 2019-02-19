perl -pe 'BEGIN{undef $/;} s#<gallery>.*</gallery>##s' \
  | sed -e 's/{{abbr|[^|]*|\([^}]\+\)}}/\1/g' \
  | pandoc --wrap=none -f mediawiki --filter filter_markdown.py -t markdown
