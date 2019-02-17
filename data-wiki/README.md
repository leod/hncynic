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
I use [https://github.com/adamwulf/wikipedia2text/blob/master/xmldump2files.py](xmldump2files.py) 
to split the XML dump into individual files, one per document:
```
bzcat enwiki-lates-pages-articles.xml.bz2 | ./xmldump2files.py /dev/stdin docs
```
Documents will be saved in some kind of hash tree in the `docs/` directory.
For example, there will be the file `docs/2f/7c/Abraham_Lincoln.txt`.

### Convert to Markdown
