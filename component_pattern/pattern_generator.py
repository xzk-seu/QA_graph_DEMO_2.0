import json
import networkx as nx


def name_pattern():
    pattern = nx.MultiDiGraph()
    pattern.add_edge('p', 'p_name', 'PERSON_NAME')
    pattern.node['p']['label'] = 'concept'
    pattern.node['p']['type'] = 'PERSON'
    pattern.node['p_name']['label'] = 'literal'
    pattern.node['p_name']['type'] = 'string'
    return nx.node_link_data(pattern)


def company_pattern():
    pattern = nx.MultiDiGraph()
    pattern.add_edge('p', 'p_name', 'CPNY_NAME')
    pattern.node['p']['label'] = 'concept'
    pattern.node['p']['type'] = 'COMPANY'
    pattern.node['p_name']['label'] = 'literal'
    pattern.node['p_name']['type'] = 'string'
    return nx.node_link_data(pattern)


def addr_pattern():
    pattern = nx.MultiDiGraph()
    pattern.add_edge('p', 'p_name', 'CPNY_NAME')
    pattern.node['p']['label'] = 'concept'
    pattern.node['p']['type'] = 'COMPANY'
    pattern.node['p_name']['label'] = 'literal'
    pattern.node['p_name']['type'] = 'string'
    return nx.node_link_data(pattern)


if __name__ == '__main__':
    entity_type_list = ['NAME', 'COMPANY', 'ADDR', 'DATE', 'Qiu',
                        'Tel', 'Ftel', 'Idcard', 'MblogUid', 'Email',
                        'WechatNum']



