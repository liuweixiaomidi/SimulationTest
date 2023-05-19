import time

import Lib.function as core


# 基于线路的绕行测试库


def code_scene():
    """
    用于开发的测试的最基本绕行
    触发条件: rbk_error: 52200
    订单: AP1-->AP4
    最优路线: AP1-->LM9-->LM10-->LM11-->AP4
    当机器人走到 LM10 时, set_rbk_error(52200)
    预期现象: 机器人沿线路绕行
    :return: 采用仿真车 失败了
    """
    core.move_robot('sim_01', 'AP1')
    time.sleep(2)
    core.goto_order('AP4')
    find = False
    while not find:
        current_station = core.get_current_location('sim_01')
        if current_station == 'LM10':
            find = True
            print('find')
            break
    if find:
        print('set')
        core.set_robot_error('sim_01', 52200)


def rbk_vehicle():
    """
    采用 sim_rbk
    :return:
    """
    core.goto_order('AP1')
    core.goto_order('AP4')


if __name__ == '__main__':
    # code_scene()
    rbk_vehicle()
