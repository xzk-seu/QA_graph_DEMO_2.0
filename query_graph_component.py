import networkx as nx
from graph import Graph


class QueryGraphComponent(Graph):
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
            self.node['p_name']['type'] = 'string'
            self.node['p_name']['entity'] = entity


if __name__ == '__main__':
    e = [{"type": "NAME", "value": "张三", "code": 0}, {"type": "NAME", "value": "李四", "code": 0}]
    c0 = QueryGraphComponent(e[0])
    c0.show()
    c1 = QueryGraphComponent(e[1])
    c1.show()

    g = nx.disjoint_union_all([Graph(c0), Graph(c1)])
    # c = QueryGraphComponent(e)
    # g = Graph(c)
    g.show()
