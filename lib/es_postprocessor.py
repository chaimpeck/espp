"""es_postprocessor.py"""

from jsonpath_rw import jsonpath, parse

class EsPostprocessor:
    def __init__(self, iterating_base_path):
        self.jsonpath_expr = parse(iterating_base_path)

    def process(self, data):
        res = []

        for match in self.jsonpath_expr.find(data):
            res.append(match.value)

        return res
