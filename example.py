from graph import Graph
from static_graph import StaticGraph
import networkx as nx


# 查询“张三的父亲是谁”
# 意图类型:0、查人；1、查公司；2、查地址


data_dict = {
    "entity": [{"type": "NAME",
                "value": "张三",
                "code": 0}, ],
    "relation": [{"type": "ParentToChild",
                  "value": "父亲",
                  "offset": 3,
                  "code": 0}, ],
    "intent": 0
}

data_seq = {
    "seq": [{"isEntity": True, "type": "NAME", "value": "张三", "code": 0},
            {"isEntity": False, "type": "ParentToChild", "value": "父亲", "offset": 3, "code": 0}],
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
        temp_name = 'somebody_%d' % n
    elif entity['type'] == 'COMPANY':
        temp_name = 'company_%d' % n
    else:
        temp_name = 'entity_%d' % n
    c = get_entity_component(entity, temp_name)

    t = Graph(graph=c)
    t.show()
    t.export('example')


def seq_process(seq):
    # seq = data_seq['seq']
    for n, item in enumerate(seq):
        if item['isEntity']:
            entity_process(item, n)


def run():
    entity_list = data_dict['entity']
    entity_process(entity_list)


if __name__ == '__main__':
    run()

    # c = get_component("NAME")
    # t = Graph(graph=c)
    # t.show()
    # t = nx.is_frozen(c)
    # print(t)

    # static_graph = StaticGraph()
    # # static_graph.show()
    # # for r in data_dict['relation']:
    # #     print(r['type'])
    #
    # e = static_graph.graph.edges
    # print(e)
