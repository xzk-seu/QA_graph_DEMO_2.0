import networkx as nx
import json
import os
from mylog import logger


class Graph:
    def __init__(self, graph=None):
        self.graph = None
        if graph:
            self.graph = graph

    def load_from_file(self, file_name):
        path = os.path.join(os.getcwd(), 'export', '%s.json' % file_name)
        try:
            with open(path, 'r', encoding='utf-8') as fr:
                data = json.load(fr)
            self.graph = nx.node_link_graph(data)
        except Exception as e:
            logger.error(e)

    def export(self, file_name):
        data = nx.node_link_data(self.graph)
        dir_path = os.path.join(os.getcwd(), 'export')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, '%s.json' % file_name)
        with open(file_path, 'w', encoding='utf-8') as fw:
            json.dump(data, fw)

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
    test_graph = nx.complete_graph(5)
    g = Graph(test_graph)
    g.show()
