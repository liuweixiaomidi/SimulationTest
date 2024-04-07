import csv
import glob
import math
import os
import json
import re
import uuid
import time
import random
import datetime

import pandas.core.series
import requests
import urllib.parse

import Lib.config
import numpy as np
import pandas as pd
import networkx as nx
import Lib.config as config
import matplotlib.pyplot as plt


def get_random_str():
    """
    用于生成唯一的订单或动作块 id
    :return:
    """
    return str(uuid.uuid1())


def set_target_list(start: int, end: int, single=None, title: str = "AP", fill: bool = None, remove=None):
    """
    用于生成库位或工作站集合
    例: set_target_list(1, 3, ["LM5", "LM7"], "AP")
    返回 ["AP1", "AP2", "AP3", "LM5", "LM7"]
    :param remove: 需要从连续点位中移除的点位 缺省为空
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
    if remove is None:
        remove = []
    for i in range(start, end + 1):
        if fill and 0 < i < 10:
            result.append(title + "0" + str(i))
        else:
            result.append(title + str(i))
    if type(single) is str:
        result.append(single)
    elif len(single):
        for i in single:
            result.append(i)
    for i in remove:
        if i in result:
            result.remove(i)
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


def get_block_data(location: str, block_id: str = None, operation: str = None, operation_args: dict = None,
                   speed: float = None):
    """
    用于生成动作块报文数据
    :param location: 目标点
    :param block_id: 动作块 id, 缺省则随机生成
    :param operation: 到点动作, 缺省为 Wait
    :param operation_args: 到点动作, 缺省为空
    :param speed: 机器人最大速度
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
    if speed is not None:
        result["robotMotionProfile"] = {
            "max_speed": speed
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
    result = requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))
    print(result, agv, position)


def goto_order(location, vehicle: str = None, order_id: str = None, group: str = None, label: str = None,
               complete: bool = None, ip: str = None, prepoint_redo: bool = None, speed: float = None,
               recognize: bool = False):
    """
    发送订单
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param order_id: 订单 id，缺省则随机生成
    :param location: 目标点: 可以为单个目标点 str; 也可以是有顺序的多个目标点 list[str]
    :param vehicle: 机器人，缺省则随机分配
    :param group: 机器人组，缺省为空
    :param label: 标签，缺省为空
    :param complete: 是否封口，缺省则封口
    :param prepoint_redo: 订单需要重做时, 是否先回到前置点, 缺省则为 false
    :param speed: 动作块信息里的 max_speed
    :param recognize: 是否是识别任务, 缺省为否
    :return: 无
    """
    data = {}
    if ip is None:
        ip = config.ip
    if order_id is None:
        order_id = get_random_str()
    if complete is None:
        complete = True
    if prepoint_redo is None:
        prepoint_redo = False
    if type(location) is str:
        data = {
            "id": order_id,
            "blocks": [{
                "blockId": get_random_str(),
                "location": location,
                "operation": "Wait",
                "operation_args": {
                    "recognize": recognize
                }
            }],
            "vehicle": ("" if vehicle is None else vehicle),
            "group": ("" if group is None else group),
            "label": ("" if label is None else label),
            "complete": complete,
            "prepointRedo": prepoint_redo
        }
        if speed is not None:
            data['blocks'][0]['robotMotionProfile'] = {
                'max_speed': speed
            }
    elif type(location) is list:
        blocks = []
        for loc in location:
            operation_args = {
                "recognize": recognize
            }
            blocks.append(get_block_data(loc, operation="JackLoad", operation_args=operation_args, speed=speed))
        data = {
            "id": order_id,
            "blocks": blocks,
            "vehicle": ("" if vehicle is None else vehicle),
            "group": ("" if group is None else group),
            "label": ("" if label is None else label),
            "complete": complete,
            "prepointRedo": prepoint_redo
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


def cancel_robot_blocked(robot: str, ip: str = None):
    """
    取消机器人的阻挡状态
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :return: None
    """
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "blocked": False
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


def set_robot_emergency(robot: str, emergency: bool = True, ip: str = None):
    """
    将机器人设置为阻挡状态
    :param emergency: 是否急停, 缺省为是
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :return: None
    """
    if ip is None:
        ip = config.ip
    data = {
        "vehicle_id": robot,
        "emergency": emergency
    }
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps(data))


def load_unload_order(location: [str, str], vehicle: str = None, order_id: str = None, group: str = None,
                      label: str = None, complete: bool = None, ip: str = None, out: str = ""):
    """
    发送取放货订单
    :param out: 打印日志格式, simple 为简易打印, 其他为完整订单打印
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param order_id: 订单 id，缺省则随机生成
    :param location: 目标点: 输入两个目标点，第一个执行 load; 第二个执行 unload
    :param vehicle: 机器人，缺省则随机分配
    :param group: 机器人组，缺省为空
    :param label: 标签，缺省为空
    :param complete: 是否封口，缺省则封口
    :return: 无
    """
    if ip is None:
        ip = config.ip
    if order_id is None:
        order_id = get_random_str()
    if complete is None:
        complete = True
    blocks = [get_block_data(location[0], operation="ForkLoad", operation_args={
        "start_height": 0.1,
        "end_height": 0.5
    }), get_block_data(location[1], operation="ForkUnload", operation_args={
        "start_height": 0.5,
        "end_height": 0.1
    })]
    data = {
        "id": order_id,
        "blocks": blocks,
        "vehicle": ("" if vehicle is None else vehicle),
        "group": ("" if group is None else group),
        "label": ("" if label is None else label),
        "complete": complete
    }
    if out:
        if label is not None:
            print(location[0] + " --> " + location[1] + '  ' + label + '  ' + str(datetime.datetime.now()))
        else:
            print(location[0] + " --> " + location[1] + '  ' + str(datetime.datetime.now()))
    else:
        print(data)
    requests.post('http://' + ip + ':8088/setOrder', json.dumps(data))


def set_robot_battery(robot: str, percentage: float, ip: str = None):
    """
    设置机器人电量
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :param robot: 机器人名称
    :param percentage: 设置电量
    :return:
    """
    if ip is None:
        ip = config.ip
    requests.post("http://" + ip + ":8088/updateSimRobotState", json.dumps({
        "vehicle_id": robot,
        "battery_percentage": 0.01 * percentage,
    }))


def fail_robot_task(robot: str, ip: str = None):
    """
    设置机器人任务失败
    :param robot: 机器人名称
    :param ip: 服务器 ip，缺省则采用 Lib.config.py 里的 ip
    :return:
    """
    if ip is None:
        ip = config
    requests.post('http://' + ip + ':8088/updateSimRobotState', json.dumps({
        "vehicle_id": robot,
        "fail_current_task": True
    }))


def set_special_bin(title1: str = None, start1: int = None, end1: int = None, fill1: bool = False,
                    title2: list[str] = None, start2: int = None, end2: int = None, fill2: bool = False,
                    title3: str = None, start3: int = None, end3: int = None, fill3: bool = False):
    """
    用于生成含有三段字符与连续数字的库位名称
    如 50-03-18A-01-1 其中 18A 01 1 是连续的数字
    :param title1: 第一段字符串, 上述示例为 50-03-
    :param start1: 第一段连续数字起始值, 上述示例为 1
    :param end1: 第一段连续数字终止值, 上述示例为 18
    :param fill1: 是否对第一段连续数字中小于 10 的值自动补零, 默认为否
    :param title2: 第二段连续字符串, 上述示例为 ['A-', 'B-']
    :param start2: 第二段连续数字起始值, 上述示例为 1
    :param end2: 第二段连续数字终止值, 上述示例为 4
    :param fill2: 是否对第二段连续数字中小于 10 的值自动补零, 默认为否
    :param title3: 第三段字符串, 上述示例为 -
    :param start3: 第三段连续数字起始值, 上述示例为 1
    :param end3: 第三段连续数字终止值, 上述示例为 4
    :param fill3: 是否对第三段连续数字中小于 10 的值自动补零, 默认为否
    :return: list[str]
    """
    result = []
    for i in range(start1, end1 + 1):
        for j in range(start2, end2 + 1):
            for k in range(start3, end3 + 1):
                for m in title2:
                    cur_i = str(0) + str(i) if fill1 and i < 10 else str(i)
                    cur_j = str(0) + str(j) if fill2 and j < 10 else str(j)
                    cur_k = str(0) + str(k) if fill3 and k < 10 else str(k)
                    result.append(title1 + cur_i + m + cur_j + title3 + cur_k)
    return result


def get_current_location(robot: str, ip: str = None):
    """
    获取机器人当前所在站点
    :param robot: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config 中的 ip
    :return: str
    """
    result = None
    has_result = False
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        if r['vehicle_id'] == robot:
            data = r['rbk_report']
            result = data['current_station']
            has_result = True
            break
    if has_result:
        return result


def get_remaining_time(robot: str, ip: str = None):
    """
    获取机器人当前订单剩余时间
    :param robot: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config 中的 ip
    :return: double
    """
    result = -1
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        if r['vehicle_id'] == robot:
            data = r['rbk_report']
            if 'remaining_time' in data:
                result = data['remaining_time']
                break
    print(result)
    return result


def get_robot_state(robot: str, ip: str = None):
    """
    获取机器人状态
    :param robot: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config 中的 ip
    :return: str
    """
    result = None
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        if r['vehicle_id'] == robot:
            data = r['current_order']
            if len(data):
                result = data['state']
                break
    return result


def get_clean_robot_property(robot: str, ip: str = None, p: bool = True):
    """
    获取清洁机器人属性
    :param p: 是否打印输出, 默认打印
    :param robot: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config.ip
    :return: dict
    """
    result = dict()
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        if r['vehicle_id'] == robot:
            data = r['rbk_report']
            if len(data):
                result = data['info']['cleanRobot']
                break
    if p:
        print(result)
    return result


def set_order_with_label(csv_name: str, timing: float, ip: str = None):
    """
    根据表格的流程发送订单
    表格为 csv 文件, 要求详见 Lib.config 中的说明
    :param timing: 发单持续时间, 单位秒
    :param ip: 服务器 ip，缺省则采用 Lib.config.ip
    :param csv_name: 表格名称（表格必须与此文件在同一文件夹下）
    :return: 无
    """
    if ip is None:
        ip = config.ip

    # path of csv
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    csv_path = os.path.join(path, csv_name)

    csv_file = pd.read_csv(csv_path)
    num_rows, num_columns = csv_file.shape

    pickups = list()
    unloads = list()
    rhythms = list()
    labels_ = list()
    pickups_check = set()
    unloads_check = set()
    rhythms_check = set()
    labels_check_ = set()

    # check csv format
    if num_columns % 4:
        raise ValueError(num_columns, "数据缺失, 表格的列数量不满足要求")
    for column_name in csv_file.columns:
        column_data = csv_file[column_name].dropna()
        temp_list = list()
        for data in column_data:
            temp_list.append(data)
        column_index = csv_file.columns.get_loc(column_name) + 1
        match column_index % 4:
            case 1:
                pickups_check.add(column_name[0:7])
                check_duplicated(column_data, column_name)
                pickups.append(temp_list)
            case 2:
                unloads_check.add(column_name[0:7])
                check_duplicated(column_data, column_name)
                unloads.append(temp_list)
            case 3:
                rhythms_check.add(column_name[0:7])
                if column_data.nunique() != 1:
                    raise ValueError(column_name, "同一个流程的节拍不一致")
                filter_rhythm = csv_file.dropna(subset=column_name)
                rhythms.append(get_column_element(filter_rhythm[column_data]))
            case 0:
                labels_check_.add(column_name[0:5])
                if column_data.nunique() != 1:
                    raise ValueError(column_name, "同一个流程的节拍不一致")
                filter_label = csv_file.dropna(subset=column_name)
                labels_.append(get_column_element(filter_label[column_name]))
            case _:
                raise ValueError("数学不存在了")
    check_column_name(pickups_check)
    check_column_name(unloads_check)
    check_column_name(rhythms_check)
    check_column_name(labels_check_)

    # set order
    print('Calculate:  ' + 'column:  ' + str(num_columns // 4) + ';  pickups:  ' + str(len(pickups)) + ';  unloads:  ' +
          str(len(unloads)) + ';  rhythms:  ' + str(len(rhythms)) + ';  labels:  ' + str(len(labels_)))
    order_num = 0
    time_control = list()
    for i in range(0, num_columns // 4):
        load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])],
                          label=labels_[i], out='simple', ip=ip)
        time_control.append(time.time())
        order_num += 1
    time_cost = time.time()
    while time.time() - time_cost < timing:
        for i in range(0, num_columns // 4):
            if time.time() - time_control[i] > rhythms[i]:
                load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])],
                                  label=labels_[i], out='simple', ip=ip)
                time_control[i] = time.time()
                order_num += 1
    print(order_num)


def check_duplicated(column_data: pandas.core.series.Series, column_name: str):
    a = column_data[column_data.duplicated(keep=False)]
    if not a.empty:
        print(a)
        raise ValueError(column_name, "点位名称重复")


def get_column_element(column_data: pandas.core.series.Series):
    for index, value in column_data.items():
        if pd.notna(value):
            return column_data.loc[index]
        return None


def check_column_name(columns: set):
    if len(columns) != 1:
        raise ValueError(columns, "列表名称不一致")


def calculate_order_from_database(ip: str = None):
    """
    从数据库统计订单信息
    :param ip: 服务器 ip，缺省则采用 Lib.config.ip
    :return: None
    """
    if ip is None:
        ip = config.ip
    condition = '{"relation":"AND","predicates":[["type","EQ","0"], ["state","EQ","FINISHED"]]}'
    encoded_condition = urllib.parse.quote(condition)
    data = 'http://' + ip + ':8088/orders?size=1000&where=' + encoded_condition
    print(data)
    orders = requests.get(data).json()
    orders_num = orders['total']
    orders = orders['list']
    print(orders_num, len(orders))
    print(orders)


def get_robot_speed(agv: str, ip: str = None):
    """
    获取机器人当前行驶速度
    :param agv: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config.ip
    :return: float
    """
    if ip is None:
        ip = config.ip
    data = requests.get('http://' + ip + ':8088/robotsStatus?vehicles=' + agv)
    if data.status_code != 200:
        return -1
    response = data.json()
    if 'report' not in response:
        return -1
    report = response['report']
    for i in report:
        if i["vehicle_id"] == agv:
            rbk_report = i["rbk_report"]
            if 'vx' not in rbk_report or 'vy' not in rbk_report:
                return -1
            vx = rbk_report['vx']
            vy = rbk_report['vy']
            v = math.hypot(vx, vy)
            print(v)
            return v
    return -1


def draw_graph(data: any, x_step: float, x_label: str, y_label: str, title: str, color: str = 'b'):
    """
    绘制 data 随时间变化图
    :param title: 标题
    :param y_label: 纵轴标题
    :param x_label: 横轴标题
    :param data: 纵轴数据
    :param x_step: 横轴间隔
    :param color: 曲线颜色, 默认蓝色
    :return: None
    """
    if type(data) is not list:
        print("typeerror")
        return
    x = [i * x_step for i in range(len(data))]
    smooth_time_intervals = np.linspace(0, len(data) * x_step, 1000)  # 生成1000个平滑的时间点
    smooth_speeds = np.interp(smooth_time_intervals, x, data)  # 进行数据插值，得到平滑的速度数据
    plt.figure(figsize=(10, 6))
    plt.plot(smooth_time_intervals, smooth_speeds, '-', color=color, label='Smoothed Curve')
    plt.scatter(x, data, color='r', marker='o', label='Original Data')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_agv2pp_from_rds_scene(scene_path: str = None, area_name: str = 'new'):
    """
    获取场景中机器人和绑定停靠点的对应表
    :param: scene_path: 需要解析的场景文件夹路径, 缺省采用 Lib.config.scene_path
    :param: area: 区域名称, 缺省为 new
    :return: None, 结果储存在文件同级 agv2pp.csv 中
    """
    if scene_path is None:
        scene_path = config.scene_path
    agv2pos = {}
    with open(scene_path, "r") as scene_file:
        scene = json.load(scene_file)
    scene_area = scene['areas']
    for area in scene_area:
        if area['name'] == area_name:
            points = area['logicalMap']['advancedPoints']
            for point in points:
                if point['className'] == 'ParkPoint':
                    pp = point['instanceName']
                    properties = point['property']
                    for _property in properties:
                        if _property['key'] == 'parkPoint' and len(_property['tag']):
                            agv2pos[_property['tag'][:-2]] = pp
    csv_path = os.path.abspath(__file__)
    csv_path = os.path.dirname(csv_path)
    csv_path = os.path.join(csv_path, 'agv2pp.csv')
    with open(csv_path, "w", newline='') as csv_file:
        csv_file.truncate(0)
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['agv', 'pp'])
        for key, value in agv2pos.items():
            csv_writer.writerow([key, value])


def set_agv_bound_pp_from_agv2pp_csv(scene_path: str = None):
    """
    根据同级文件 agv2pp.csv 将机器人绑定 PP 点写入场景中
    :param: scene_path: 需要写入的场景文件夹路径, 缺省采用 Lib.config.scene_path
    :return: None
    """
    if scene_path is None:
        scene_path = Lib.config.scene_path
    with open(scene_path, "r+", encoding='utf-8') as scene_file:
        scene = json.load(scene_file)
        csv_path = os.path.abspath(__file__)
        csv_path = os.path.dirname(csv_path)
        csv_path = os.path.join(csv_path, 'agv2pp.csv')
        agv2pp = {}
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                key, value = row
                agv2pp[key] = value
        scene_area = scene['areas']
        for area in scene_area:
            points = area['logicalMap']['advancedPoints']
            for point in points:
                if point['className'] == 'ParkPoint':
                    pp = point['instanceName']
                    properties = point['property']
                    for _property in properties:
                        if _property['key'] == 'parkPoint' and len(_property['tag']):
                            break
                    else:
                        if agv2pp.get(pp) is None:
                            print(f"{pp} 点未绑定")
                        else:
                            properties.append({
                                'key': 'parkPoint',
                                'type': 'bool',
                                'value': f"{agv2pp[pp]}:1",
                                'boolValue': True
                            })
        scene_file.truncate(0)
        scene_file.seek(0)


def set_agv_init_pos_from_agv2pp_csv(scene_path: str = None):
    """
    根据同级文件 agv2pp.csv 将机器人初始化位置写入场景中
    :param scene_path: 需要写入的场景文件夹路径, 缺省采用 Lib.config.scene_path
    :return: None
    """
    if scene_path is None:
        scene_path = Lib.config.scene_path
    with open(scene_path, "r+", encoding='utf-8') as scene_file:
        scene = json.load(scene_file)
        csv_path = os.path.abspath(__file__)
        csv_path = os.path.dirname(csv_path)
        csv_path = os.path.join(csv_path, 'agv2pp.csv')
        agv2pp = dict()
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                key, value = row
                agv2pp[key] = value
        scene_robot_group = scene['robotGroup']
        for group in scene_robot_group:
            for robot in group['robot']:
                if agv2pp.get(robot['id']) is not None:
                    for _property in robot['property']:
                        if _property['key'] == 'initialPosition':
                            _property['stringValue'] = agv2pp[robot['id']]
        scene_file.truncate(0)
        scene_file.seek(0)


def get_current_block_state(order_id: str, ip: str = None):
    """
    获取当前执行的动作块的状态
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'blocks' in order_details:
        blocks = order_details['blocks']
        block = blocks[-1]
        if 'state' in block:
            return block['state']
    return ""


def get_order_state(order_id: str, ip: str = None):
    """
    获取订单的状态
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'state' in order_details:
        return order_details['state']
    return ''


def get_order_vehicle(order_id: str, ip: str = None):
    """
    获取执行订单的机器人名称
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'vehicle' in order_details:
        return order_details['vehicle']
    return ''


def get_current_block_location(order_id: str, ip: str = None):
    """
    获取当前执行的动作块的目标点
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'blocks' in order_details:
        blocks = order_details['blocks']
        block = blocks[-1]
        if 'location' in block:
            return block['location']
    return ""


def get_last_second_block_location(order_id: str, ip: str = None):
    """
    获取倒数第二个动作块的目标点
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'blocks' in order_details:
        blocks = order_details['blocks']
        block = blocks[-2]
        if 'location' in block:
            return block['location']
    return ""


def add_block(location: any, order_id: str, complete: bool = None, ip: str = None):
    """
    追加动作块
    :param location: 目标点
    :param order_id: 订单号
    :param complete: 是否封口运单, 缺省为否
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: None
    """
    if complete is None:
        complete = False
    if ip is None:
        ip = config.ip
    data = dict()
    if type(location) is str:
        data = {
            "id": order_id,
            "blocks": [{
                "blockId": str(uuid.uuid1()),
                "location": location,
                "operation": "Wait",

            }],
            "complete": complete
        }
    elif type(location) is list:
        blocks = []
        for loc in location:
            blocks.append(get_block_data(loc, operation="Wait"))
        data = {
            "id": order_id,
            "blocks": blocks,
            "complete": complete
        }
    requests.post('http://' + ip + ':8088/addBlocks', json.dumps(data))
    print('addBlock: ', location, ' complete:', complete, order_id)


def get_robots_pos(ip: str = None):
    """
    获取场景中所有机器人位置
    :param ip: 服务器 ip, 缺省则采用 Lib.config::ip
    :return: dict
    """
    result = dict()
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        data = r['rbk_report']
        result[r['vehicle_id']] = data['current_station']
    return result


def get_robots_x_y_pos(name: str, ip: str = None):
    """
    获取机器人坐标
    :param name: 机器人名称
    :param ip: 服务器 ip, 缺省则采用 Lib.config::ip
    :return: dict
    """
    result = dict()
    if ip is None:
        ip = Lib.config.ip
    status = requests.get('http://' + ip + ':8088/robotsStatus').json()
    for r in status['report']:
        if r['vehicle_id'] == name:
            data = r['rbk_report']
            if len(data):
                result['x'] = data['x']
                result['y'] = data['y']
                break
    return result


def get_current_block_id(order_id: str, ip: str = None):
    """
    获取当前执行的动作块的 id
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = config.ip
    order_details = requests.get('http://' + ip + ':8088/orderDetails/' + order_id).json()
    if 'blocks' in order_details:
        blocks = order_details['blocks']
        block = blocks[-1]
        if 'blockId' in block:
            return block['blockId']
    return ""


def draw_speed_graph():
    goto_order(location='LM198', speed=0.99)
    time.sleep(0.5)
    speeds = list()
    while get_robot_state('rbk1') != 'FINISHED':
        speeds.append(get_robot_speed('rbk1'))
        time.sleep(0.5)
    draw_graph(speeds, 0.5, 'time', 'speed', 'agv speed graph')


def get_fork_height(name: str):
    """
    获取叉车货叉高度
    :param name: 机器人名称
    :return:
    """
    robots_status = requests.get('http://127.0.0.1:8088/robotsStatus').json()
    if 'report' in robots_status:
        report = robots_status['report']
        for r in report:
            if 'vehicle_id' in r and r['vehicle_id'] == name:
                robot_statue = r
                if 'rbk_report' in robot_statue:
                    rbk_report = robot_statue['rbk_report']
                    if 'fork' in rbk_report:
                        fork = rbk_report['fork']
                        if 'fork_height' in fork:
                            return fork['fork_height']
    return -1


def rds_log_time_analyze(log_path: str = None):
    """
    分析日志中的 t-cost \n
    只分析最新的.log文件中最多 100 条最近的 TCost 日志 \n
    控制台打印:
        1. 分析 TCost 日志数量
        2. TCost 日志原文
        3. 每周期耗时
        4. 平均每周期耗时
        5. 耗时最长的 5 个周期
        6. 耗时最短的 5 个周期
    :param log_path: 日志所在文件夹路径, 默认路径写在 config::log_path
    :return: csv 耗时降序排序, 在同级文件 timeCost.csv 中
    """
    if log_path is None:
        log_path = config.log_path
    csv_path = os.path.join(os.path.dirname(__file__), 'timeCost.csv')
    search_pattern = os.path.join(log_path, f"*.log")  # 在.log文件中查找
    log_files = glob.glob(search_pattern)
    if not log_files:
        print(f"No log files found in {log_path}")
        return None
    latest_log_file_path = max(log_files, key=os.path.getmtime)  # 只分析最新的一个日志
    # keyword_lines = (lambda file_path, keyword: [
    #     m_line.strip() for m_line in open(file_path, 'r').readlines() if keyword in m_line
    # ] if os.path.exists(file_path) else [])(latest_log_file_path, 'TCost')
    # 找到所有包含 TCost 的行
    keyword_lines = [m_line.strip() for m_line in open(latest_log_file_path, 'r').readlines() if 'TCost' in m_line]
    # 最多只取最近 50 条
    keyword_lines = keyword_lines[-100:] if len(keyword_lines) > 100 else keyword_lines
    if keyword_lines:
        print(f"Lines containing {len(keyword_lines)} 'TCost' in the file:")
        for line in keyword_lines:
            print(line)
        open(csv_path, 'w').close()  # 清空表格
        data_list = []
        for index, line in enumerate(keyword_lines):
            elements = (lambda m_line: re.findall(r'\[(.*?)]', m_line))(line)  # 提取[]内的元素
            time_cost = dict(zip(*[iter(elements[-1].split("|"))] * 2))  # 最后一个[]内的元素是记录各模块耗时的, 根据|拆分dict
            for key, value in time_cost.items():
                time_cost[key] = int(value)     # 耗时转为int
            sorted_time_cost = dict(sorted(time_cost.items(), key=lambda item: item[1], reverse=True))  # 耗时降序排序
            # dict 转为 DataFrame
            df_data = pd.DataFrame(list(sorted_time_cost.items()),
                                   columns=[f'Module-{index + 1}', f'TCost-{index + 1}'])
            data_list.append(df_data)
        df = pd.concat(data_list, axis=1)   # 按列追加
        time_cost_columns = df.iloc[0, 1::2]
        print(time_cost_columns)
        time_cost_columns = pd.to_numeric(time_cost_columns, errors='coerce')   # pandas.core.series.Series 转换为数值类型
        time_cost_columns = time_cost_columns.dropna()  # 删除有缺失值的行
        df.to_csv(csv_path, index=False)    # 写入csv文件
        print(f"平均每周期耗时: {time_cost_columns.mean()}")
        print(f"最大5个周期的耗时: {time_cost_columns.nlargest(5).values}")
        print(f"最小5个周期的耗时: {time_cost_columns.nsmallest(5).values}")
    else:
        print("No lines containing 'TCost' found in the file")


def mark_complete(order_id: str, ip: str = None):
    """
    订单封口
    :param order_id: 订单 id
    :param ip: 服务器 ip, 缺省采用 config.ip
    """
    if ip is None:
        ip = config.ip
    m_data = {
        "id": order_id
    }
    requests.post('http://' + ip + ':8088/markComplete', data=json.dumps(m_data))


def match():
    similarities = {
        "sim_01": [1, 2, 3, 4],
        "sim_02": [1, 2, 3],
        "sim_03": [1, 3, 4],
        "sim_04": [2, 4],
        "sim_05": [3, 4]
    }
    edges = []
    for key, nodes in similarities.items():
        for node in nodes:
            edges.append((key, node))
    print("生成的边：", edges)
    # 创建一个二分图
    graph = nx.Graph()
    # 添加左边节点集合
    graph.add_nodes_from(['sim_01', 'sim_02', 'sim_03', 'sim_04', 'sim_05'], bipartite=0)  # 设置bipartite=0表示这些节点属于左边集合
    # 添加右边节点集合
    graph.add_nodes_from([1, 2, 3, 4], bipartite=1)  # 设置bipartite=1表示这些节点属于右边集合
    # 添加边
    graph.add_edges_from(edges)
    # 使用匈牙利算法找到最大匹配
    matching = nx.bipartite.maximum_matching(graph)
    print("最大匹配结果：", matching)


def terminate_order(robot: list[str] = None, order_id: str = None, ip: str = None):
    """
    终止订单
    :param robot: 机器人名称, 缺省为空
    :param order_id: 订单号, 缺省为空
    :param ip: 服务器 ip, 缺省则采用 Lib.config::ip
    :return: None
    """
    if ip is None:
        ip = Lib.config.ip
    if order_id is None and robot is None:
        return
    elif not robot and not order_id:
        return
    elif order_id is not None:
        requests.post('http://' + ip + ':8088/terminate', data=json.dumps({'id': order_id}))
    else:
        requests.post('http://' + ip + ':8088/terminate', data=json.dumps({'vehicles': robot}))


def get_sweep_order_state(oid: str, ip: str = None):
    """
    获取清扫父订单状态
    :param oid: 订单 id
    :param ip: 服务器 ip, 缺省则采用 Lib.config::ip
    :return: str
    """
    if ip is None:
        ip = Lib.config.ip
    details = requests.get('http://' + ip + ':8088/sweepOrderDetails/' + oid).json()
    if 'state' in details:
        return details['state']
    return ''



if __name__ == '__main__':
    # rds_log_time_analyze(r'F:\SEER\Code\Python\SimulationTest-pure\RDSCoreLog')
    # rds_log_time_analyze()
    # match()
    while True:
        print(get_sweep_order_state('seer-01'))
        time.sleep(1)