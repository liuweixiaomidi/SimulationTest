import json
import uuid
import requests

import Lib.config as config


def get_random_str():
    """
    用于生成唯一的订单或动作块 id
    :return:
    """
    return str(uuid.uuid1())


def set_target_list(start: int, end: int, single=None, title: str = "AP", fill: bool = None):
    """
    用于生成库位或工作站集合
    例: set_target_list(1, 3, ["LM5", "LM7"], "AP")
    返回 ["AP1", "AP2", "AP3", "LM5", "LM7"]
    :param fill:  是否要对 10 以下的库位自动补0 缺省为否
    :param title: 站点名前缀 缺省为 “AP”
    :param start: 连续点位的起始 包含该值
    :param end:   连续点位的结束值 包含该值
    :param single:不在连续点位内的点位 缺省为空
    :return: list[str]
    """
    result = []
    if fill is None:
        fill = False
    if single is None:
        single = []
    for i in range(start, end + 1):
        if fill and 0 < i < 10:
            result.append(title + "0" + str(i))
        else:
            result.append(title + str(i))
    if type(single) == str:
        result.append(single)
    elif len(single):
        for i in single:
            result.append(i)
    return result


def set_order(order: dict, ip: str = None):
    """
    发送订单
    :param order: 订单报文数据
    :param ip: 服务器 ip, 默认为 Lib.config.py 文件里的 ip
    :return: 无
    """
    if ip is None:
        ip = config.ip
    requests.post("http://" + ip + ":8088/setOrder", json.dumps(order))


def set_vehicle(start: int, end: int, single=None, title: str = "sim_"):
    """
    用于生成机器人 list
    例: set_vehicle(1, 3, "Fork-01")
    返回 ["sim_01", "sim_02, "sim_03", "Fork-01"]
    :param start: 起始值 包含该值
    :param end:   终止值 包含该值
    :param single: 不在起始值与终止值之间的名称 缺省为空
    :param title:  机器人名称前缀 默认为 “sim_”
    :return: list[str]
    """
    result = []
    if single is not None:
        for i in single:
            result.append(i)
    for i in range(start, end + 1):
        if 0 < i < 10:
            result.append(title + "0" + str(i))
        else:
            result.append(title + str(i))
    return result


def get_block_data(location: str, block_id: str = None, operation: str = None, operation_args: dict = None):
    """
    用于生成动作块报文数据
    :param location: 目标点
    :param block_id: 动作块 id, 缺省则随机生成
    :param operation: 到点动作, 缺省为 Wait
    :param operation_args: 到点动作, 缺省为空
    :return: dict
    """
    if block_id is None:
        block_id = get_random_str()
    if operation is None:
        operation = "Wait"
    result = {
        "blockId": block_id,
        "location": location,
        "operation": operation,
        "operation_args": ("" if operation_args is None else operation_args)
    }
    return result


def get_order_data(blocks: list[dict], order_id: str = None, vehicle: str = None, group: str = None, label: str = None,
                   complete: bool = None):
    """
    用于生成订单报文数据
    :param blocks: 动作块 list 不可缺省
    :param order_id: 订单 ID 缺省则随机生成
    :param vehicle: 执行机器人 缺省则随机分配
    :param group: 在此机器人组内分配任务 可缺省
    :param label: 在此标签内分配任务 可缺省
    :param complete: 是否封口 缺省则封口
    :return: dict
    """
    if order_id is None:
        order_id = get_random_str()
    if complete is None:
        complete = True
    data = {
        "id": order_id,
        "blocks": blocks,
        "vehicle": ("" if vehicle is None else vehicle),
        "group": ("" if group is None else group),
        "label": ("" if label is None else label),
        "complete": complete
    }
    return data


def get_distribute_order_data(fromLoc: str, toLocList: list, returnLoc: str, ordered: bool, order_id: str = None,
                              group: str = None, label: str = None, vehicle: str = None):
    """
    生成分拨单订单报文数据
    :param fromLoc: 取货点
    :param toLocList: 分拨点 list
    :param returnLoc: 归还点
    :param ordered: 是否按顺序分拨 false为不按顺序
    :param order_id: 订单 id 缺省则随机生成
    :param group: 机器人组，可缺省
    :param label: 标签，可缺省
    :param vehicle: 执行机器人，可缺省
    :return: dict
    """
    if order_id is None:
        order_id = get_random_str()
    data = {
        "id": order_id,
        "fromLoc": fromLoc,
        "toLocList": toLocList,
        "returnLoc": returnLoc,
        "ordered": ordered,
        "group": ("" if group is None else group),
        "label": ("" if label is None else label),
        "vehicle": ("" if vehicle is None else vehicle)
    }
    return data


def set_goods_shape(robot: str, xmin: float, ymin: float, xmax: float, ymax: float, angle: float = None,
                    ip: str = None):
    """
    设置货物形状
    :param ymax: 货物 ymax
    :param xmax: 货物 xmax
    :param ymin: 货物 ymin
    :param xmin: 货物 xmin
    :param robot: 机器人名称
    :param ip: 服务器ip，默认为 Lib.config.py 里的 ip
    :param angle: 货物与机器人弧度，缺省为 0
    :return: 无
    """
    if angle is None:
        angle = 0
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "goods_shape": str([xmin, ymin, xmax, ymax]),
        "goods_vehicle_angle": angle
    }
    requests.post("http://" + ip + ":8088/updateSimRobotState", json.dumps(data))


def dis_point_path(point: list[str] = None, path: list[str] = None):
    """
    禁用点位线路
    :param point: 禁用点位表，缺省为空，例["LM1", "LM2"]
    :param path: 禁用路段表，缺省为空，例["LM1-LM2", "LM2-LM3"]
    :return: 禁用成功: True，禁用失败: False
    """
    result = False
    if point is None and path is None:
        return False
    if point is not None:
        for m_point in point:
            data_point = {
                "id": m_point
            }
            msg_point = requests.post('http://' + config.ip + ':8088/disablePoint', json.dumps(data_point))
            if msg_point.status_code == 200:
                result = True
    if path is not None:
        for m_path in path:
            data_path = {
                "id": m_path
            }
            msg_path = requests.post('http://' + config.ip + ':8088/disablePath', json.dumps(data_path))
            if msg_path.status_code == 200:
                result = True
    if result:
        return True
    return False


def move_robot(agv: str, position: str, angle: float = None, ip: str = None):
    """
    移动机器人到指定位置
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param angle: 新位置弧度，缺省为 0
    :param agv: 机器人名称
    :param position: 移动至点位名称
    :return: 无
    """
    if ip is None:
        ip = config.ip
    if angle is None:
        angle = 0
    data = {
        "vehicle_id": agv,
        "position_by_name": position,
        "angle": angle
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def goto_order(location, vehicle: str = None, order_id: str = None, group: str = None, label: str = None,
               complete: bool = None, ip: str = None):
    """
    发送订单
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param order_id: 订单 id，缺省则随机生成
    :param location: 目标点: 可以为单个目标点 str; 也可以是有顺序的多个目标点 list[str]
    :param vehicle: 机器人，缺省则随机分配
    :param group: 机器人组，缺省为空
    :param label: 标签，缺省为空
    :param complete: 是否封口，缺省则封口
    :return: 无
    """
    data = {}
    if ip is None:
        ip = config.ip
    if order_id is None:
        order_id = get_random_str()
    if complete is None:
        complete = True
    if type(location) == str:
        data = {
            "id": order_id,
            "blocks": [{
                "blockId": get_random_str(),
                "location": location,
                "operation": "Wait"
            }],
            "vehicle": ("" if vehicle is None else vehicle),
            "group": ("" if group is None else group),
            "label": ("" if label is None else label),
            "complete": complete
        }
    elif type(location) == list:
        blocks = []
        for loc in location:
            blocks.append(get_block_data(loc))
        data = {
            "id": order_id,
            "blocks": blocks,
            "vehicle": ("" if vehicle is None else vehicle),
            "group": ("" if group is None else group),
            "label": ("" if label is None else label),
            "complete": complete
        }
    print(data)
    requests.post('http://' + ip + ':8088/setOrder', json.dumps(data))


def move_robot_by_xy(robot: str, x: float, y: float, ip: str = None):
    """
    移动机器人到指定坐标
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :param x: 坐标 x
    :param y: 坐标 y
    :return: 无
    """
    if ip is None:
        ip = config.ip
    xy = {
        "x": x,
        "y": y
    }
    transfer_xy = str(xy).replace('\'', '\"')
    data = {
        "vehicle_id": robot,
        "position": transfer_xy
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def set_robot_angle(robot: str, angle: float, ip: str = None):
    """
    设置机器人朝向
    :param robot: 机器人名称
    :param angle: 朝向 0, ±1.75, ±3.14
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :return: None
    """
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "angle": angle
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def set_robot_blocked(robot: str, ip: str = None):
    """
    将机器人设置为阻挡状态
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :return: None
    """
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "blocked": True
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def set_robot_error(robot: str, error: any, ip: str = None):
    """
    将机器人设置为阻挡状态
    :param error: 报错信息
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :return: None
    """
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "error": str(error).replace('\'', '\"')
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def load_unload_order(location: [str, str], vehicle: str = None, order_id: str = None, group: str = None,
                      label: str = None, complete: bool = None, ip: str = None):
    """
    发送订单
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param order_id: 订单 id，缺省则随机生成
    :param location: 目标点: 输入两个目标点，第一个执行 load; 第二个执行 unload
    :param vehicle: 机器人，缺省则随机分配
    :param group: 机器人组，缺省为空
    :param label: 标签，缺省为空
    :param complete: 是否封口，缺省则封口
    :return: 无
    """
    data = {}
    if ip is None:
        ip = config.ip
    if order_id is None:
        order_id = get_random_str()
    if complete is None:
        complete = True
    blocks = [get_block_data(location[0], operation="ForkLoad"), get_block_data(location[1], operation="ForkUnload")]
    data = {
        "id": order_id,
        "blocks": blocks,
        "vehicle": ("" if vehicle is None else vehicle),
        "group": ("" if group is None else group),
        "label": ("" if label is None else label),
        "complete": complete
    }
    print(data)
    requests.post('http://' + ip + ':8088/setOrder', json.dumps(data))
