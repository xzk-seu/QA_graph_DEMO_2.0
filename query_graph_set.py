import networkx as nx
import json
import os
import itertools
import copy
from graph import Graph
from query_graph_component import QueryGraphComponent


class QueryGraph:
    def __init__(self, query_data):
        self.relation = query_data.setdefault('relation', list())
        self.entity = query_data.setdefault('entity', list())
        self.intent = query_data.setdefault('intent', 'PERSON')

        self.relation_component_list = list()
        self.entity_component_list = list()
        # 获取实体和关系对应的子图组件
        self.init_relation_component()
        self.init_entity_component()
        # 得到子图组件构成的集合，用图表示
        self.disconnected_graph = nx.disjoint_union_all(self.relation_component_list+self.entity_component_list)
        self.query_graph = copy.deepcopy(self.disconnected_graph)
        self.old_query_graph = copy.deepcopy(self.disconnected_graph)

        self.node_type_dict = dict()
        self.node_type_statistic()
        self.component_assemble()

        while len(self.query_graph.nodes) != len(self.old_query_graph.nodes) \
                and not nx.algorithms.is_weakly_connected(self.query_graph):
            # 节点一样多说明上一轮没有合并
            # 图已连通也不用合并
            self.old_query_graph = copy.deepcopy(self.query_graph)
            self.node_type_dict = dict()
            self.node_type_statistic()
            self.component_assemble()
        self.add_intention()

    def add_intention(self):
        # 也需要依存分析,待改进
        for n in self.query_graph.nodes:
            if self.query_graph.node[n]['label'] == 'concept':
                node_type = self.query_graph.node[n]['type']
                if node_type == self.intent:
                    self.query_graph.node[n]['intent'] = True
                    break

    """
    统计每种类型的节点的个数
    """
    def node_type_statistic(self):
        node_type_dict = dict()
        for n in self.query_graph.nodes:
            if self.query_graph.node[n]['label'] == 'concept':
                node_type = self.query_graph.node[n]['type']
                if node_type not in node_type_dict.keys():
                    node_type_dict[node_type] = list()
                node_type_dict[node_type].append(n)
        self.node_type_dict = node_type_dict

    def component_assemble(self):
        # 之后根据依存分析来完善
        for k, v in self.node_type_dict.items():
            if len(v) > 2:
                combinations = itertools.combinations(v, 2)
                for pair in combinations:
                    # 若存在这两条边，则跳过，不存在则合并
                    if self.query_graph.has_edge(pair[0], pair[1]) or\
                            self.query_graph.has_edge(pair[1], pair[0]):
                        continue
                    else:
                        mapping = {pair[0]: pair[1]}
                        nx.relabel_nodes(self.query_graph, mapping, copy=False)
                        break

    def init_entity_component(self):
        for e in self.entity:
            component = QueryGraphComponent(e)
            self.entity_component_list.append(nx.MultiDiGraph(component))

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

                relation_component.node['temp_0']['type'] = relation_data[r['type']]['domain']
                relation_component.node['temp_1']['type'] = relation_data[r['type']]['range']
                self.relation_component_list.append(relation_component)


if __name__ == '__main__':
    data_dict = {
        "entity": [{"type": "NAME",
                    "value": "张三",
                    "code": 0},
                   {"type": "TEL", "value": "139999999999", "code": 0}],
        "relation": [{"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0},
                     ],
        "intent": 'PERSON'
    }
    qg = QueryGraph(data_dict)

    g = Graph(qg.query_graph)
    g.show()
    g.export('query_graph')


