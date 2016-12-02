"""es_request.py"""

# https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html

import requests

ES_BASE_URL = 'http://localhost:9200/'

class EsRequest:
    def __init__(self, indices, types=None, query_string=None):
        url = ES_BASE_URL + indices

        if types:
            url += '/' + types

        url += '/_search?' + query_string

        self.url = url

    def request(self, method, data=None):
        if method == "GET":
            r = requests.get(self.url)
        else:
            r = requests.post(self.url, data=data)

        return r.json()