import random
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


def lower_left_corner():
    """
    费斯托左下角业务逻辑发单
    :return: None
    """
    load_target = core.set_target_list(33, 40, title="HSD-01-")
    load_target += core.set_target_list(16, 28, title="HSD-01-")
    load_target += core.set_target_list(4, 11, title="HSD-01-", fill=True)
    r_load_target = core.set_target_list(4, 11, title="RHSD-01-", fill=True)
    r_load_target += core.set_target_list(16, 28, title="RHSD-01-", fill=True)
    r_load_target += core.set_target_list(33, 40, title="RHSD-01-", fill=True)
    mid_unload_target = core.set_special_bin('50-03-', 1, 18, True, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    delis = core.set_special_bin('50-03-', 12, 12, False, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    unload_target = [x for x in mid_unload_target if x not in delis]
    r_unload_target = core.set_special_bin('R50-03-', 1, 18, True, ['A-', 'B-'], 5, 6, True, '-', 1, 3, False)
    mid_unload_target = core.set_special_bin('50-04-', 1, 18, True, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    delis = core.set_special_bin('50-04-', 12, 12, False, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    unload_target += [x for x in mid_unload_target if x not in delis]
    r_unload_target += core.set_special_bin('R50-04-', 1, 18, True, ['A-', 'B-'], 5, 6, True, '-', 1, 3, False)
    while len(load_target) and len(r_load_target):
        loc1 = random.choice(load_target)
        loc2 = random.choice(unload_target)
        core.load_unload_order([loc1, loc2], group='SFL-L14')
        unload_target.remove(loc2)
        load_target.remove(loc1)
        loc3 = random.choice(r_load_target)
        loc4 = random.choice(r_unload_target)
        core.load_unload_order([loc3, loc4], group='SFL-R14S')
        r_load_target.remove(loc3)
        r_unload_target.remove(loc4)
        time.sleep(5)


if __name__ == '__main__':
    lower_left_corner()
