from Lib.function import *

full_data = [{
    "name": "m1",           # str: 仿真机器名称
    "online": True,         # bool: 在线状态
    "emergency": False,     # bool: 急停状态
    "max_capacity": 10,     # int: 最大容量
    "process_time": 120.0,  # double: 加工时间
    "upper_machine": "",    # str: 上位机名称
    "lower_machine": "m2",  # str: 下位机名称
    "pickup_workstations": [{
        "name": "w1",       # str: 工作站名称
        "type": 0,          # int: 0表示取货工作站, 1表示放货工作站
        "label": "label-1", # str: 负责此工作站任务的机器人标签
        "online": True,     # bool: 在线状态
        "emergency": False, # bool: 急停状态
        "dock_time": 3.0,   # double: 机器人到达工作站后的对接时间
        "machine_name": "m1",  # str: 所属机器名称 TODO: 这个可以优化掉, 因为他已经在机器字段下了, 不需要重复填写
        "bins": [{
            "name": "b1",   # str: 库位名称
            "online": True, # bool: 在线状态
            "state": 0,     # int: 0表示Free, 1表示Occupy, 2表示Full
            "emergency": False,       # bool: 急停状态
            "workstation_name": "w1"  # str: 所属工作站名称 TODO: 这个可以优化掉, 因为他已经在工作站字段下了, 不需要重复填写
        }]     # array_list: 库位
    }], # array_list: 取货工作站列表 TODO: 工作站下有 type 字段, 所以可以优化将 取放货工作站 合并到一个字段里
    "unload_workstations": [{
        "name": "w1",       # str: 工作站名称
        "type": 0,          # int: 0表示取货工作站，1表示放货工作站
        "label": "label-1", # str: 负责此工作站任务的机器人标签
        "online": True,     # bool: 在线状态
        "emergency": False, # bool: 急停状态
        "dock_time": 3.0,   # double: 机器人到达工作站后的对接时间
        "machine_name": "m1",  # str: 所属机器名称 TODO: 这个可以优化掉, 因为他已经在机器字段下了, 不需要重复填写
        "bins": [{
            "name": "b1",  # str: 库位名称
            "online": True,# bool: 在线状态
            "state": 0,    # int: 0表示Free, 1表示Occupy, 2表示Full
            "emergency": False,       # bool: 急停状态
            "workstation_name": "w1"  # 所属工作站名称 TODO: 这个可以优化掉, 因为他已经在工作站字段下了, 不需要重复填写
        }]     # array_list: 库位
    }]  # array_list: 放货工作站列表 TODO: 工作站下有 type 字段, 所以可以优化将 取放货工作站 合并到一个字段里
}]


def set_single_bin(name: str, w_name: str, state: int=0):
    data = {
        'name': name,
        'state': state,
        'workstation_name': w_name
    }
    return data


def generate_xsim_order_data():
    area_1 = set_target_list(1, 3)
    area_2 = set_target_list(4, 6)
    area_3 = set_target_list(7, 9)
    area_4 = set_target_list(10, 12)
    m1, m2, m3 = 'm1', 'm2', 'm3'
    w1, w2_1, w2_2, w3 = 'w1', 'w2_1', 'w2_2', 'w3'
    data = [
        {
            'name': m1,
            'max_capacity': 5,
            'process_time': 15,
            'lower_machine': m2,
            'pickup_workstations': [{
                'name': w1,
                'type': 0,
                'label': 'L1',
                'dock_time': 5,
                'machine_name': m1,
                'bins': [
                    set_single_bin(area_1[0], w1),
                    set_single_bin(area_1[1], w1),
                    set_single_bin(area_1[2], w1)
                ]
            }]
        },
        {
            'name': m2,
            'max_capacity': 4,
            'process_time': 15,
            'upper_machine': m1,
            'lower_machine': m3,
            'pickup_workstations': [{
                'name': w2_2,
                'type': 1,
                'label': 'L2',
                'dock_time': 5,
                'machine_name': m2,
                'bins': [
                    set_single_bin(area_3[0], w2_2),
                    set_single_bin(area_3[1], w2_2),
                    set_single_bin(area_3[2], w2_2)
                ]
            }],
            'unload_workstations': [{
                'name': w2_1,
                'type': 0,
                'label': 'L1',
                'dock_time': 5,
                'machine_name': m2,
                'bins': [
                    set_single_bin(area_2[0], w2_1),
                    set_single_bin(area_2[1], w2_1),
                    set_single_bin(area_2[2], w2_1)
                ]
            }]
        },
        {
            'name': m3,
            'max_capacity': 3,
            'process_time': 15,
            'upper_machine': m2,
            'unload_workstations': [{
                'name': w3,
                'type': 1,
                'label': 'L2',
                'dock_time': 5,
                'machine_name': m3,
                'bins': [
                    set_single_bin(area_4[0], w3),
                    set_single_bin(area_4[1], w3),
                    set_single_bin(area_4[2], w3)
                ]
            }]
        }
    ]
    print(data)
    requests.post('http://127.0.0.1:8088/updateXSimOrder', json=data)

def set_operation_time():
    data = {
        'vehicle_id': 'sim_01',
        'operation_time': json.dumps(
            [
                {
                    'operation': 'gao_lei',
                    'time': 10
                },
                {
                    'operation': 'ding_yu_bo',
                    'time': 5
                }
            ]
        )
    }
    order_data = {
        'id': get_random_str(),
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'AP1',
                'operation': 'gao_lei'
            },
            {
                'blockId': get_random_str(),
                'location': 'AP5',
                'operation': 'ding_yu_bo'
            }
        ],
        'vehicle': 'sim_01',
        'complete': True
    }
    r1 = requests.post('http://127.0.0.1:8088/updateSimRobotState', json.dumps(data))
    time.sleep(10)
    r2 = requests.post('http://127.0.0.1:8088/setOrder', json.dumps(order_data))
    print(r1.json(), r2.json())


if __name__ == '__main__':
    generate_xsim_order_data()
