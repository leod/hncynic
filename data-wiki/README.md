# Wiki Data 
Here, we prepare training data from an English Wikipedia data dump.
Nothing too interesting, just a series of tedious steps because I don't know any better tools for this.

## Steps
### Download
Download a dump of the English Wikipedia in XML format.
This can be done here for example:
[https://dumps.wikimedia.org/backup-index.html](https://dumps.wikimedia.org/backup-index.html).
What we are interested in is a file like `enwiki-lates-pages-articles.xml.bz2`,
which currently has a size of about 15GB.

### Split
I use [xmldump2files.py](https://github.com/adamwulf/wikipedia2text/blob/master/xmldump2files.py) 
to split the XML dump into individual files, one per document:
```
bzcat enwiki-lates-pages-articles.xml.bz2 | ./xmldump2files.py /dev/stdin docs
```
Documents will be saved in some kind of hash tree in the `docs/` directory.
For example, there will be the file `docs/2f/7c/Abraham_Lincoln.txt`.

## Filter Documents
I get about 10M extracted documents, as `xmldump2files.log` shows:
```
Redirects 8465477  Deleted 0  Disambigs 271019  Lists 231905  Skipped 0  Wrote 10200000 50.01GiB  Total 10200000 50.01GiB  (185%)
```
The official
[Wikipedia statistics](https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia#Annual_growth_rate_for_the_English_Wikipedia)
say that there are currently about 5.8M articles.
The dump that I downloaded contains a lot of non-articles.
The most serious offenders can be found like this:
```
find docs/ -name '*.txt' \
  | grep -o '/[^/%]*%3' \
  | sort \
  | uniq -c \
  | awk '{print $1,$2}' \
  | sort -k1,1 -n \
  | tail -n20
```
I've collected them in `doc-list-filter.grep` to filter the document list:
```
find docs -name '*.txt' | grep -vF -f doc-list-filter.grep > docs.txt
```
I'm left with 5.78M of 10.2M documents.

### Convert to Markdown
We convert from the MediaWiki markup to Markdown using [pandoc](https://pandoc.org/),
together with a custom filter [filter_markdown.py](filter_markdown.py) written with
[panflute](http://scorreia.com/software/panflute/)
that removes content that is not useful for us.

Here's how to convert and filter one document:
```
pandoc --wrap=none -f mediawiki -t markdown < test/out/7a/77/Astronomer.txt \
  | pandoc --filter filter_markdown.py -t markdown
```
