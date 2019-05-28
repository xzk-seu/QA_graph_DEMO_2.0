import os
import json


"""
生成测试用例的脚本
"""


data_dict = {
        "entity": [{"type": "NAME",
                    "value": "张三",
                    "offset": 0}, ],
        "relation": [{"type": "ParentToChild",
                      "value": "父亲",
                      "offset": 3,
                      "code": 0},
                     ],
        "intent": 'PERSON'
    }


def case1():
    query = '烽火科技大厦的张三'
    entity = [{'type': 'ADDRESS', 'value': '烽火科技大厦', 'offset': 0}, {'type': 'NAME', 'value': '张三', 'offset': 7}]
    relation = []
    intent = 'PERSON'
    case1_dict = dict(query=query, entity=entity, relation=relation, intent=intent)
    with open('case1.json', 'w') as fw:
        json.dump(case1_dict, fw)


def case2():
    query = '15195919704的同学有哪些'
    entity = [{'type': 'TEL', 'value': '15195919704', 'offset': 0}]
    relation = [{'type': 'SchoolMate', 'value': '同学', 'offset': 12}]
    intent = 'PERSON'
    case_dict = dict(query=query, entity=entity, relation=relation, intent=intent)
    with open('case2.json', 'w') as fw:
        json.dump(case_dict, fw)


def case3():
    query = '15195919704的同学中名字叫张三的手机号'
    entity = [{'type': 'TEL', 'value': '15195919704', 'offset': 0}, {'type': 'NAME', 'value': '张三', 'offset': 18}]
    relation = [{'type': 'SchoolMate', 'value': '同学', 'offset': 12}]
    intent = 'TEL'
    case_dict = dict(query=query, entity=entity, relation=relation, intent=intent)
    with open('case3.json', 'w') as fw:
        json.dump(case_dict, fw)


def case4():
    query = '父亲为张三的15195919704的同事有哪些'
    entity = [{'type': 'NAME', 'value': '张三', 'offset': 3}, {'type': 'TEL', 'value': '15195919704', 'offset': 6}, ]
    relation = [{'type': 'ParentToChild', 'value': '父亲', 'offset': 0},
                {'type': 'COLLEAGUE', 'value': '同事', 'offset': 18}]
    intent = 'PERSON'
    case_dict = dict(query=query, entity=entity, relation=relation, intent=intent)
    with open('case4.json', 'w') as fw:
        json.dump(case_dict, fw)


def case5():
    query = '新城科技园张三的同事有哪些'
    entity = [{'type': 'ADDRESS', 'value': '新城科技园', 'offset': 0}, {'type': 'NAME', 'value': '张三', 'offset': 5}]
    relation = [{'type': 'COLLEAGUE', 'value': '同事', 'offset': 8}]
    intent = 'PERSON'
    case_dict = dict(query=query, entity=entity, relation=relation, intent=intent)
    with open('case5.json', 'w') as fw:
        json.dump(case_dict, fw)


if __name__ == '__main__':
    case5()
