from graph import Graph
from static_graph import StaticGraph
import networkx as nx
import os
import json


# 查询“张三的父亲是谁”
# 意图类型:0、查人；1、查公司；2、查地址


data_dict = {
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


# 获取和实体信息相关的子图
def get_entity_component(entity, temp_name):
    static_graph = StaticGraph()
    graph_component = None
    if entity['type'] == 'NAME':
        static_graph_component = static_graph.graph.edge_subgraph([('人', '文本:姓名', '姓名'), ])
        edge_attr = static_graph_component.get_edge_data('人', '文本:姓名', '姓名')
        graph_component = nx.MultiDiGraph()
        graph_component.add_edge(temp_name, entity['value'], '姓名', **edge_attr)

        temp_node_attr = static_graph_component.node['人']
        temp_node_attr['type'] = '人'
        attrs = {
            temp_name: temp_node_attr,
            entity['value']: static_graph_component.node['文本:姓名']
        }
        nx.set_node_attributes(graph_component, attrs)

    return graph_component


# def relation_process(relation_list):
#     for n, relation in enumerate(relation_list):


def entity_process(entity, n):
    # print(entity)
    if entity['type'] == 'NAME':
        temp_name = 'person_%d' % n
    elif entity['type'] == 'COMPANY':
        temp_name = 'company_%d' % n
    else:
        temp_name = 'entity_%d' % n
    c = get_entity_component(entity, temp_name)

    t = Graph(graph=c)
    t.show()
    t.export('example')


def get_person_chain(person_rel_list):
    person_chain = nx.MultiDiGraph()
    for n, r in enumerate(person_rel_list):
        person_chain.add_edge('person%d' % n, 'person%d' % (n+1), r['type'])

    for n in person_chain.nodes:
        person_chain.node[n]['label'] = 'concept'
        person_chain.node[n]['type'] = 'PERSON'

    return person_chain


def run():
    # entity_list = data_dict['entity']
    # entity_process(entity_list[0], 0)

    relation_path = os.path.join(os.getcwd(), 'ontology', 'relation.json')
    with open(relation_path, 'r') as fr:
        relation = json.load(fr)
    rels = data_dict['relation']
    person_rel_list = list()
    for r in rels:
        if r['type'] in relation.keys():
            person_rel_list.append(r)

    p = get_person_chain(person_rel_list)
    g = Graph(p)
    g.show()


if __name__ == '__main__':
    run()
