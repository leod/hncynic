# Wiki Data 
Here, we prepare training data from an English Wikipedia data dump.

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

### Convert to Markdown
We convert from the MediaWiki markup to Markdown using [pandoc](https://pandoc.org/),
together with a custom filter written with [panflute](http://scorreia.com/software/panflute/)
that removes content that is not useful for us.

Here's how to convert and filter one document:
```
pandoc --wrap=none -f mediawiki -t markdown < test/out/7a/77/Astronomer.txt \
  | pandoc --filter filter_test.py -t markdown
```
