import Lib.function as core
import time

"""
珠海飞利浦项目
"""


def test_1():
    """
    偏离线路
    :return: None
    """
    core.move_robot_by_xy("SW500-01", -66.689472, -17.928998)
    time.sleep(1)
    core.set_robot_angle("SW500-01", 0)
    time.sleep(1)
    core.goto_order("LM604", "SW500-01")
