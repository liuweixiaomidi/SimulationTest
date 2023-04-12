import time

import Lib.function as core

"""
青岛海信
"""


def test_1():
    """
    充电点进出死锁
    :return: None
    """
    core.move_robot("HX_1", "LM197")
    core.move_robot("HX_14", "CP303")
    time.sleep(1)
    core.goto_order("CP303", "HX_1")
    core.goto_order("LM1", "HX_14")


def test_2():
    """
    充电点进出死锁
    :return: None
    """
    core.move_robot("HX_1", "LM197")
    core.move_robot("HX_2", "PP320")
    time.sleep(1)
    core.goto_order("LM2", "HX_1")
    core.goto_order("LM1", "HX_2")
