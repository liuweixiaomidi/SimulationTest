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
    mid_unload_target = set_special_bin('50-03-', 1, 18, True, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    delis = set_special_bin('50-03-', 12, 12, False, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    unload_target = [x for x in mid_unload_target if x not in delis]
    r_unload_target = set_special_bin('R50-03-', 1, 18, True, ['A-', 'B-'], 5, 6, True, '-', 1, 3, False)
    mid_unload_target = set_special_bin('50-04-', 1, 18, True, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    delis = set_special_bin('50-04-', 12, 12, False, ['A-', 'B-'], 1, 4, True, '-', 1, 3, False)
    unload_target += [x for x in mid_unload_target if x not in delis]
    r_unload_target += set_special_bin('R50-04-', 1, 18, True, ['A-', 'B-'], 5, 6, True, '-', 1, 3, False)
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
