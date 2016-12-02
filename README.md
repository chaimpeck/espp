# espp
Elasticsearch Postprocessing Service

This is a tool that accepts JSONPath's in the headers to do interesting things with the results of an Elasticsearch query, such as reshaping, joining with other results, and even outputting a csv/tsv.

Here is an example:

 ```
 curl -s 'localhost:9998/test-index/_search?doc_type=tweet' -H 'x-espp-iterating-base-path: $.hits.hits[*]._source' | jq .
[
  {
    "text": "Elasticsearch: cool. bonsai cool.",
    "author": "kimchy",
    "timestamp": "2016-12-01T11:39:33.093311"
  }
]
```

Compare to the actual output of the query:
```
{
  "hits": {
    "hits": [
      {
        "_score": 1,
        "_type": "tweet",
        "_id": "1",
        "_source": {
          "text": "Elasticsearch: cool. bonsai cool.",
          "author": "kimchy",
          "timestamp": "2016-12-01T11:39:33.093311"
        },
        "_index": "test-index"
      }
    ],
    "total": 1,
    "max_score": 1
  },
  "_shards": {
    "successful": 5,
    "failed": 0,
    "total": 5
  },
  "took": 4,
  "timed_out": false
}
```

This project has only just begun and there is still much to implement.
