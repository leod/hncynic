#!/usr/bin/env python3
"""
Do stuff
"""

import sys

from panflute import *

# Sections that we filter out completely
SECTION_IGNORE = [
  'See also',
  'Notes',
  'References',
  'External links',
  'Gallery',
]

# Some more candidates for ignoring:
# - Partial filmography as director

# Elements that we ignore
ELEMENT_IGNORE = [
  Image,
  Note, # footnotes and endnotes
  Table,
  RawBlock,
  RawInline,
  SmallCaps,
  Strikeout,
  Subscript,
  Superscript,
]

def prepare(doc):
  doc.my_current_section = None

def action(elem, doc):
  # We must not filter out Doc, that leads to errors
  if isinstance(elem, Doc):
    return elem

  # Filter certain sections
  if doc.my_current_section is not None and doc.my_current_section in SECTION_IGNORE:
    return []

  if isinstance(elem, Link):
    sys.stderr.write(stringify(elem) + ': ' + str(elem) +  '\n')
    # For links, only keep the description text
    descr = elem.content.list

    # Filter links that don't have any description
    if len(descr) == 0:
      return []

    # Filter strange thumbnail links
    #
    # E.g. there is a link whose description is:
    # [Str(thumb|upright=1.1|),
    #  Emph(Str([The) Space Str(Astronomer](The_Astronomer_(Vermeer)) Space Str("wikilink"))),
    #  Space, Str(by), Space, Str([Johannes), Space, Str(Vermeer](Johannes_Vermeer), Space,
    #  Str("wikilink"))]
    if (isinstance(descr[0], Str) and 'thumb|' in descr[0].text) or 'thumb|' in stringify(elem):
      return []

    # Also ignore links to Wikipedia media
    if stringify(elem).startswith('File:'):
      return []

    return descr
  elif any([isinstance(elem, t) for t in ELEMENT_IGNORE]):
    return []
  elif isinstance(elem, Header):
    if elem.level == 2:
      doc.my_current_section = stringify(elem)
      if doc.my_current_section in SECTION_IGNORE:
        return []
  elif isinstance(elem, Strong):
    # Hacker News only has Emph
    return Emph(*elem.content)

def main(doc=None):
  return run_filter(action, prepare=prepare, doc=doc) 

if __name__ == '__main__':
  main()
