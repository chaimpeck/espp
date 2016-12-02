#!/usr/bin/env python

"""
Proxy requests to an elasticsearch instance, reading special 
postprocessing instructions from headers and reshaping the output.

Some features include:
- reshape json output
- csv output
- join/merge multiple queries
"""


import sys
import logging
import json
from datetime import datetime
import requests
from bottle import default_app, route, run, request, response, abort
from lib.es_request import EsRequest
from lib.es_postprocessor import EsPostprocessor


@route('/')
def index():
    return '<pre>%s</pre>' % 'It works!'

@route('/<indices>/_search', method="ANY")
@route('/<indices>/<types>/_search', method="ANY")
def search(indices, types=None):
    # curl -s 'localhost:9998/test-index/_search?doc_type=tweet' -H 'x-espp-iterating-base-path: $.hits.hits[*]._source' | jq .
    
    es_request = EsRequest(indices, types, request.query_string)

    res = es_request.request(request.method, request.body.read())

    iterating_base_path = request.headers.get('x-espp-iterating-base-path')

    if iterating_base_path:
        es_postprocessor = EsPostprocessor(iterating_base_path)
        res = es_postprocessor.process(res)

    response.content_type = 'application/json'
    return json.dumps(res)


def setup():
    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)


def main(argv=None):
    # Start our bottle web server
    port = int(argv[1]) if len(argv) > 1 else 9998

    run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
