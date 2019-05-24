import networkx as nx
import json
import os
from mylog import logger
from graph import Graph
from query_graph_component import QueryGraphComponent


class QueryGraph:
    def __init__(self, query_data):
        self.relation = query_data.setdefault('relation', list())
        self.entity = query_data.setdefault('entity', list())
        self.intent = query_data.setdefault('entity', 0)

        self.component_list = list()
        self.init_relation_component()

        self.disconnected_graph = nx.disjoint_union_all(self.component_list)

        # self.component_list.extend()

    def init_relation_component(self):
        relation_path = os.path.join(os.getcwd(), 'ontology', 'relation.json')
        with open(relation_path, 'r') as fr:
            relation_data = json.load(fr)
        for r in self.relation:
            if r['type'] in relation_data.keys():
                relation_component = nx.MultiDiGraph()
                relation_component.add_edge('temp_0', 'temp_1', r['type'], **r)
                for n in relation_component.nodes:
                    relation_component.node[n]['label'] = 'concept'
                    relation_component.node[n]['type'] = 'PERSON'
                self.component_list.append(relation_component)


if __name__ == '__main__':
    data_dict = {
        "entity": [{"type": "NAME",
                    "value": "张三",
                    "code": 0}, ],
        "relation": [{"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0},
                     {"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0}
                     ],
        "intent": 0
    }
    qg = QueryGraph(data_dict)

    g = Graph(qg.disconnected_graph)
    g.show()


