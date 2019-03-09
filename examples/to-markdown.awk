#!/usr/bin/awk -f

BEGIN {
  FS="\t"
} {
  if ((NR-1) % 5 == 0)
    print "## " $1
  gsub(/<NL>/, "\n  >", $2)
  print "- > " $2
  print "\n"
}
