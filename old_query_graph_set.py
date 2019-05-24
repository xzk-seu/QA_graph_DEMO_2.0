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

        self.person_relation_list = list()
        self.init_person_relation_list()

        # 以人物关系构造链条
        self.person_relation_chain = nx.MultiDiGraph()
        self.init_person_relation_chain()

    def init_person_relation_list(self):
        relation_path = os.path.join(os.getcwd(), 'ontology', 'relation.json')
        with open(relation_path, 'r') as fr:
            relation = json.load(fr)

        for r in self.relation:
            if r['type'] in relation.keys():
                if relation[r['type']]['domain'] == relation[r['type']]['range'] == 'PERSON':
                    self.person_relation_list.append(r)

    def init_person_relation_chain(self):
        for n, r in enumerate(self.person_relation_list):
            self.person_relation_chain.add_edge('person%d' % n, 'person%d' % (n + 1), r['type'])

        for n in self.person_relation_chain.nodes:
            self.person_relation_chain.node[n]['label'] = 'concept'
            self.person_relation_chain.node[n]['type'] = 'PERSON'


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
    qg = QueryGraph(data_dict)
    gr = qg.person_relation_chain
    g = Graph(gr)
    print('=========chain=====')
    # g.show()

    co = QueryGraphComponent(data_dict['entity'][0], 'person0')
    c = Graph(co)
    print('=========component=====')
    # c.show()

    # t = nx.compose(gr, nx.MultiDiGraph(co))
    t = nx.compose(gr, co)

    t = Graph(t)
    t.show()

    t = nx.relabel.relabel_nodes(t, {'person0_name': 'person0'})

    t = Graph(t)
    t.show()

    # print(qg.relation)
    # print(qg.entity)

