import Lib.function as core
import time
import math

"""
用于悲惨的日常找bug
"""


def normal():
    core.move_robot("sim_01", "LM4")
    core.move_robot("sim_02", "LM24")
    time.sleep(1)
    core.goto_order("AP22", "sim_01")
    core.goto_order("PP61", "sim_02")


def test_1():
    """
    recover 拼接路线错误
    吴江卡特地图
    :return: None
    """
    # core.move_robot_by_xy("Fork-03", 10.7, -3.5)
    core.move_robot("Fork-03", "LM107")
    core.move_robot("Fork-04", "LM190")
    time.sleep(1)
    core.goto_order("PP256", "Fork-04")
    # core.goto_order("AP38", "Fork-04")


def test_2():
    """
    rotate 应该多看一步 防止点位过近
    吴江卡特地图
    :return: None
    """
    core.move_robot("Fork-03", "LM166")
    core.move_robot("Fork-04", "AP1068")
    core.goto_order("AP163", "Fork-03")
    time.sleep(5)
    core.goto_order("AP243", "Fork-04")


def test_3():
    """
    走到路线一半被阻挡 触发 reset 后再次下发路线 float path 错误
    青岛海信地图
    :return: None
    """
    core.move_robot("HX_1", "LM15")
    core.move_robot("HX_2", "CP303")
    time.sleep(2)
    core.goto_order("LM146", "HX_1")
    time.sleep(20)
    core.move_robot_by_xy("HX_2", 7.7, 27.8)


def test_4():
    """
    特殊自动任务需求
    地图 test_specialAutoTask
    :return: None
    """
    core.move_robot("AMB-01", "LM719")
    core.move_robot("AMB-02", "LM924")
    time.sleep(2)
    core.goto_order("AP944", "AMB-01")
    core.goto_order("LM719", "AMB-02")


def test_5():
    """
    mutexExpand 测试用例
    地图 zwy_0414
    :return: None
    """
    core.move_robot("Fork-21", "AP43")
    core.move_robot("Fork-19", "PP455")
    time.sleep(2)
    core.goto_order("AP44", "Fork-19")
    time.sleep(30)
    core.goto_order("AP4", "Fork-21")


def replan():
    core.move_robot('sim_01', 'AP2')
    time.sleep(1)
    core.goto_order('AP4', 'sim_01')
    time.sleep(5)
    core.set_robot_error('sim_01', ['40', '41'])


def charge_safe():
    """
    当机器人电量低于 chargeSafe 时, 必须从正在充电的车中找出一辆已经充电最多的车交换
    :return:
    """
    core.move_robot("sim_01", "PP46")
    core.move_robot("sim_02", "PP47")
    core.move_robot("sim_03", "PP31")
    time.sleep(1)
    core.set_robot_battery("sim_01", 40)
    core.set_robot_battery("sim_02", 30)
    time.sleep(30)
    core.set_robot_battery("sim_03", 10)


def count():
    total = 2700
    for i in range(total):
        if total < 0:
            break
        print(total)
        total -= 3
        time.sleep(1)


def test_festo():
    core.move_robot("AMB-01", "LM283")
    core.move_robot("AMB-02", "LM204")
    time.sleep(2)
    core.goto_order("AP677", "AMB-01")
    core.goto_order("AP619", "AMB-02")


def test_fushikang():
    # dyb: 加入测试用例 mapf避让测试
    core.move_robot('AMB-02', 'LM53')
    core.move_robot('AMB-03', 'LM61')
    time.sleep(2)
    core.goto_order(location='LM65', vehicle='AMB-02')
    core.goto_order(location='PP76', vehicle='AMB-03')


def test_fushikang2():
    # dyb: 加入测试用例 mapf避让测试
    core.move_robot('AMB-05', 'LM439')
    core.move_robot('AMB-06', 'LM441')
    time.sleep(2)
    core.goto_order(location='LM419', vehicle='AMB-06')
    time.sleep(3)
    core.goto_order(location='LM414', vehicle='AMB-05')


def calculate_two_points_length(x1: float, x2:float, y1: float, y2: float):
    x = x1 - x2
    y = y1 - y2
    return math.hypot(x, y)


if __name__ == '__main__':
    count()




















