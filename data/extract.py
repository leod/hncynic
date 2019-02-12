#!/usr/bin/env python3
"""
Extract only the top-level comments from a HN data dump.

The dump is read from STDIN in the JSON format (see README.md).
Extracted comments are written to STDOUT in TSV, with the following columns:
1. ID
3. Time
4. Story Title
5. Text

Statistics are written on STDERR.
"""

import argparse
import sys
import json
import html

def normalize_text(text):
  return html.escape(text).replace('\r', '').replace('\n', ' <n> ').replace('\t', ' <t> ')

class Converter(object):
  def __init__(self):
    # We remember a mapping from object IDs to the titles of stories.
    # This way we can tell if a comment is top-level by checking if its parent is a story.
    # This works in a single pass since the input lines are sorted by ID.
    self.story_titles = {}

    # Let's keep some stats
    self.n_total = 0
    self.n_comments = 0
    self.n_top_level_comments = 0
    self.n_unexpected_format = 0
    self.n_ignored = 0
 
  def _process_object(self, obj, f_out):
    body = obj['body']
    object_type = body['type']

    if object_type == 'story':
      self.story_titles[body['id']] = body['title']
    elif object_type == 'comment':
      self.n_comments += 1 

      story_title = self.story_titles[body['parent']]

      if story_title is not None:
        # Yay, got one!
        self.n_top_level_comments += 1

        f_out.write(str(body['id']))
        f_out.write('\t')
        f_out.write(str(body['time']))
        f_out.write('\t')
        f_out.write(story_title)
        f_out.write('\t')
        f_out.write(normalize_text(body['text']))
        f_out.write('\n')
    else:
      self.n_ignored += 1

  def process_object(self, obj, f_out):
    try:
      self.n_total += 1
      self._process_object(obj, f_out)
    except KeyError as e:
      # Not sure why this happens, but some lines in the input seem to be missing fields
      self.n_unexpected_format += 1

  def write_stats(self, f_out):
    f_out.write('stories:\t{}\n'.format(len(self.story_titles)))
    if len(self.story_titles) > 0:
      f_out.write('comments/story:\t{:.2f}\n'.format(self.n_comments / float(len(self.story_titles))))
    f_out.write('comments:\t{}\n'.format(self.n_comments))
    if self.n_comments > 0:
      f_out.write('top-level:\t{} ({:.4f}%)\n'.format(self.n_top_level_comments, self.n_top_level_comments / float(self.n_comments) * 100.0))
    f_out.write('ignored:\t{:.4f}%\n'.format(self.n_ignored / float(self.n_total) * 100.0))
    f_out.write('invalid:\t{:.4f}%\n'.format(self.n_unexpected_format / float(self.n_total) * 100.0))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  args = parser.parse_args()

  converter = Converter()

  for n, line in enumerate(sys.stdin):
    converter.process_object(json.loads(line), f_out=sys.stdout)
    if (n+1) % 500_000 == 0:
      sys.stderr.write('[{:.1f}M]\n'.format((n+1) / float(1_000_000)))
      converter.write_stats(sys.stderr)

  converter.write_stats(f_out=sys.stderr)
