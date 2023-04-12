import time

import Lib.function as core


def test_1():
    """
    复现左上角路口死锁
    :return: None
    """
    core.move_robot("R-3", "LM22806")
    core.move_robot("R-2", "LM3764")
    time.sleep(1)
    core.goto_order("AP3692", "R-3")
    core.goto_order(["AP3634", "AP3853"], "R-2")
