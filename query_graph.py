import networkx as nx
import json
import csv
import os
from mylog import logger
from graph import Graph


class QueryGraph(Graph):
    def __init__(self, query_data):
        Graph.__init__(self)
        # if isinstance(query_data. dict):
        self.query_data = query_data
        self.relation = query_data.setdefault('relation', list())
        self.entity = query_data.setdefault('entity', list())


if __name__ == '__main__':
    data_dict = {
        "entity": [{"type": "NAME",
                    "value": "张三",
                    "code": 0}, ],
        "relation": [{"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0},
                     ],
        "intent": 0
    }
    data_dict_1 = {
        "entity": [{"type": "NAME",
                    "value": "张三",
                    "code": 0}, ],
        "relation": [{"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0},
                     {"type": "HusbandToWife",
                      "value": "妻子",
                      "offset": 3,
                      "code": 0},
                     ],
        "intent": 0
    }
    qg = QueryGraph(data_dict_1)
    print(qg.relation)
    print(qg.entity)

