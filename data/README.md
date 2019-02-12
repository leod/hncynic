# Data
This directory contains some simple tools for analyzing and transforming
the HN data dump data.

## Format
A brief look into the format of the HN data dump.

Each line is one JSON object. Each object has an ID, by which the lines are sorted.
This is the first line, representing a story, pretty-printed:
```
 $ head -n1 14m_hn_comments_sorted.json | jq
 {
 	"body": {
 		"kids": [
 			487171,
 			15,
 			234509,
 			454410,
 			82729
 		],
 		"descendants": 15,
 		"url": "http://ycombinator.com",
 		"title": "Y Combinator",
 		"by": "pg",
 		"score": 61,
 		"time": 1160418111,
 		"type": "story",
 		"id": 1
 	},
 	"source": "firebase",
 	"id": 1,
 	"retrieved_at_ts": 1435938464
 }
```

This is a comment:
```
{
  "body": {
    "kids": [
      455092
    ],
    "parent": 534,
    "text": "which ones are you thinking about? ",
    "id": 586,
    "time": 1172193356,
    "type": "comment",
    "by": "gustaf"
  },
  "source": "firebase",
  "id": 586,
  "retrieved_at_ts": 1435974128
}
```
