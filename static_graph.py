import networkx as nx
import json
import csv
import os
from graph import Graph
from mylog import logger


# 从ontology文件夹导入数据
def load_data(ontology_dir):
    dir_path = os.path.join(os.getcwd(), ontology_dir)
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
def graph_generation(ontology_dir):
    temp_graph = nx.MultiDiGraph()
    data = load_data(ontology_dir)

    # 导入对象属性边
    for i in data['object_attribute']:
        relation_name, label, successor, predecessors = i
        temp_graph.add_edge(successor, predecessors, label, label=label, type='object', relation_name=relation_name)
    # 导入值属性边
    for i in data['valued_attribute']:
        label, successor, value_type = i
        predecessors = '%s:%s' % (value_type, label)
        temp_graph.add_edge(successor, predecessors, label, label=label, type='value')

    # 为节点导入属性
    for n in temp_graph.nodes:
        if ':' in n:
            temp_graph.node[n]['label'] = 'literal'
        else:
            temp_graph.node[n]['label'] = 'concept'
    # 使graph不能再被修改
    nx.freeze(temp_graph)
    # self.graph = temp_graph
    return temp_graph


class StaticGraph(Graph):
    def __init__(self, ontology_dir=None, graph=None):
        if ontology_dir:
            # 如果指定了本体文件
            graph = graph_generation(ontology_dir)
            Graph.__init__(self, graph=graph)
        else:
            # self.load_from_file('static_graph')
            Graph.__init__(self, file_name='static_graph')


if __name__ == '__main__':
    # static_graph = StaticGraph("ontology")
    static_graph = StaticGraph()
    static_graph.show()
    static_graph.export('static_graph')
