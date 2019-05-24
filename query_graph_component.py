import networkx as nx
from graph import Graph


class QueryGraphComponent(nx.MultiDiGraph):
    """
    获取实体，生成相对应的子图组件
    """
    def __init__(self, entity):
        nx.MultiDiGraph.__init__(self)
        if entity['type'] == 'NAME':
            self.add_edge('p', 'p_name', 'HAS_NAME')
            self.node['p']['label'] = 'concept'
            self.node['p']['type'] = 'PERSON'
            self.node['p_name']['label'] = 'literal'
            self.node['p_name']['value'] = entity['value']


if __name__ == '__main__':
    e = {"type": "NAME", "value": "张三", "code": 0}
    c = QueryGraphComponent(e)
    g = Graph(c)
    g.show()
