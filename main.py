import random
import time

import requests

import Lib.function as core
import Lib.config as config
import Project.ChangShaHuiKe as cs
import Project.ZhuHaiFeiLiPu as zf
import Project.Debug as debug
import Project.JiNanFesto as jn
import Project.QingDaoHaiXin as qd


def general_demo():
    """
    1. 设置接单机器人集合、取货点集合、放货点结合
    2. 如果是分拨单等特殊需求，还需设置分拨点集合、归还点集合等
    3. 设置一个停止测试的条件: 如达到指定数量停止发单、取货点用光停止发单、放货点放满货停止发单等; 本示例设置条件: 每个机器人发送一个订单
    4. 不同的场景对库位是否可以同时被多辆车发单、单一库位最大容量等要求不尽相同
    5. 本次 demo 采用一个库位同时只能被一个车使用，且容量为 1
    6. 设置一个循环, 按一定时间间隔进行发单
    7. 循环内: 每次随机选取一个取货点和放货点(如有需要也可以随机选一个机器人接单)
    8. 循环内: 发送订单、将此次使用的取货点和防火点从库区集合中删除
    9. 循环内: 设置发单间隔时间
    :return: 无
    """
    vehicles = core.set_vehicle(start=1, end=10)  # 调用 set_vehicle 设置机器人集合
    load_pos = core.set_target_list(start=30, end=49, title="LM")  # 调用 set_target_list 设置取货点集合
    unload_p = core.set_target_list(start=15, end=24, title="AP")  # 调用 set_target_list 设置放货点集合
    while len(vehicles):    # 终止条件: 所有机器人都收到订单了
        m_vehicle = random.choice(vehicles)    # 从机器人列表中随机选择一个机器人
        m_load_po = random.choice(load_pos)    # 从取货点列表中随机选一个库位
        m_unloads = random.choice(unload_p)    # 从放货点列表中随机选一个库位
        core.goto_order(location=[m_load_po, m_unloads], vehicle=m_vehicle)    # 发送订单
        vehicles.remove(m_vehicle)    # 移除已发送订单的车
        load_pos.remove(m_load_po)    # 移除已使用的取货点
        unload_p.remove(m_unloads)    # 移除已使用的放货点
        time.sleep(1.5)    # 设置发单间隔


def run():
    """
    1. 初始化 取货区域 放货区域 等任务点
    2. 设置限制订单数量的条件: 计数、取货点空、放货点满、所有车均有单等
    3. 随机选择本次订单的取放货点位和机器人
    4. 生成动作块
    5. 发送订单
    6. 把已经使用过的取放货点、机器人从组内移出
    7. 发单间隔
    :return: 无
    """
    load_loc = core.set_target_list(30, 50, title="LM")
    unload_l = core.set_target_list(15, 25, title="LM")
    vehicles = core.set_vehicle(1, 11)
    m_number = 0
    while m_number < 3:
        m_load = random.choice(load_loc)
        m_unload = random.choice(unload_l)
        agv = random.choice(vehicles)
        block_1 = core.get_block_data(m_load)
        block_2 = core.get_block_data(m_unload)
        m_block = [block_1, block_2]
        m_order = core.get_order_data(m_block, vehicle=agv)
        core.set_order(m_order)
        load_loc.remove(m_load)
        unload_l.remove(m_unload)
        vehicles.remove(agv)
        m_number += 1
        time.sleep(2)


def demo():
    """
    分拨单自动发单
    :return: 无
    """
    distribute = core.set_target_list(15, 25, title="LM")
    _from_1 = "LM3"
    _to_1 = random.sample(distribute, 5)
    _return = "LM100"
    m_order = core.get_distribute_order_data(_from_1, _to_1, _return, False)
    core.set_order(m_order)
    time.sleep(3)
    order_id = m_order['id']
    detail = requests.get("http://" + config.ip + ":8088/distributeOrderDetails/" + order_id).json()
    order_vehicle = detail['vehicle']
    while detail['state'] != 'FINISHED':
        time.sleep(2)
        detail = requests.get("http://" + config.ip + ":8088/distributeOrderDetails/" + order_id).json()
        unload_status = {}
        for unload_order_list in detail['unloadOrderMap']:
            to_loc = unload_order_list['toLoc']
            unload_status[to_loc] = unload_order_list['unloadOrderList'][0]['blocks'][0]['state']
        for (loc, state) in unload_status.items():
            if state == 'WAITING':
                requests.post('http://' + config.ip + ':8088/distributeTaskDone/' + order_vehicle)


def festo():
    core.move_robot("R-1", "AP4192")
    core.move_robot("R-2", "AP4438")
    core.move_robot("R-3", "AP2891")
    core.move_robot("L-1", "AP4785")
    core.move_robot("L-3", "AP4657")
    core.move_robot("L-4", "AP4970")
    core.move_robot("L-5", "AP4317")
    core.move_robot("L-6", "AP4671")
    time.sleep(2)
    m_bin = ["AP2739", "AP2618"]
    for i in range(2723, 2730):
        m_bin.append("AP" + str(i))
    for i in range(2715, 2720):
        m_bin.append("AP" + str(i))
    for i in range(2732, 2738):
        m_bin.append("AP" + str(i))
    for i in range(2700, 2704):
        m_bin.append("AP" + str(i))
    for i in range(2694, 2697):
        m_bin.append("AP" + str(i))
    num = 0
    while num != 8:
        num += 1
        m_loc = random.choice(m_bin)
        core.goto_order(m_loc)
        m_bin.remove(m_loc)
        time.sleep(0.5)


if __name__ == '__main__':
    cs.test_5()
