import networkx as nx
import json
import csv
import os
from mylog import logger


# 从ontology文件夹导入数据
def load_data():
    dir_path = os.path.join(os.getcwd(), 'ontology')
    object_attribute_path = os.path.join(dir_path, 'object_attribute.csv')
    valued_attribute_path = os.path.join(dir_path, 'valued_attribute.csv')
    object_attribute_list = list()
    valued_attribute_list = list()

    # 导入对象属性
    with open(object_attribute_path, 'r', encoding='utf-8') as csv_file:
        csv_file.readline()
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            object_attribute_list.append(i)
    # 导入值属性
    with open(valued_attribute_path, 'r', encoding='utf-8') as csv_file:
        csv_file.readline()
        csv_reader = csv.reader(csv_file)
        for i in csv_reader:
            valued_attribute_list.append(i)

    return dict(object_attribute=object_attribute_list, valued_attribute=valued_attribute_list)


# 静态问答图生成
def graph_generation():
    graph = nx.MultiDiGraph()
    data = load_data()

    # 导入对象属性边
    for i in data['object_attribute']:
        label, successor, predecessors = i
        graph.add_edge(successor, predecessors, label, label=label, type='object')
    # 导入值属性边
    for i in data['valued_attribute']:
        label, successor, value_type = i
        predecessors = '%s:%s' % (value_type, label)
        graph.add_edge(successor, predecessors, label, label=label, type='value')

    # 为节点导入属性
    for n in graph.nodes:
        if ':' in n:
            graph.node[n]['label'] = 'literal'
        else:
            graph.node[n]['label'] = 'concept'
    # 使graph不能再被修改
    nx.freeze(graph)
    # export_graph(graph, 'all_graph')
    return graph


#
class QueryGraph:
    def __init__(self, generate_by_ontology=False):
        self.graph = None
        if generate_by_ontology:
            self.graph = graph_generation()

    def load_from_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as fr:
                data = json.load(fr)
            self.graph = self.load_from_data(data)
        except Exception as e:
            # print(e)
            logger.error(e)
        else:
            return self.graph

    def load_from_data(self, data):
        if type(data) != dict:
            logger.info('%s object can not be load as a graph, please load a dict' % str(type(data)))
            return
        try:
            self.graph = nx.node_link_graph(data)
        except Exception as e:
            logger.error(e)
        else:
            return self.graph

    # def export(self, path):
    #     data = nx.node_link_data(self.graph)
    #     with open(path, 'w') as fw:

    def show(self):
        if not self.graph:
            print("There is nothing to show!")
            return
        flag = True
        if not self.graph.is_multigraph():
            flag = False
        print('=================The graph have %d nodes==================' % len(self.graph.nodes))
        for n in self.graph.nodes:
            data = self.graph.node[n]
            print(str(n).ljust(30), '\t', str(data).ljust(30))
        # print('=================The graph have %d edges==================' % len(self.graph.edges))
        print('The graph have %d edges'.center(100, '=') % len(self.graph.edges))
        for e in self.graph.edges:
            # multigraph的边结构为(u, v, k)
            # 非multigraph的边结构为(u, v)
            if flag:
                data = self.graph.get_edge_data(e[0], e[1], e[2])
            else:
                data = self.graph.get_edge_data(e[0], e[1])
            print(str(e).ljust(30), '\t', str(data).ljust(30))


if __name__ == '__main__':
    # g = QueryGraph(generate_by_ontology=True)
    # graph_path = os.path.join(os.getcwd(), 'export', 'all_graph.json')
    g = QueryGraph()
    graph_path = os.path.join(os.getcwd(), 'export', '2_sub_graph.json')
    with open(graph_path, 'r') as fr:
        d = json.load(fr)
    g.load_from_data(d[1])
    g.show()

