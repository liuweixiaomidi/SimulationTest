import Lib.function as core
import time

"""
长沙惠科项目测试代码库
"""
# dyb: 后续应加入测试用例用来检测 mapf 避让动作是否合理


def test_1():
    """
    现场复现: 三辆车初始停靠点，两车先后去同一工作区域内的两个点位, 另一个车去中间点位
    :return: None
    """
    core.move_robot("34001", "PP278")
    core.move_robot("34002", "PP80")
    core.move_robot("34003", "PP79")
    time.sleep(3)
    core.goto_order(["AP24", "LM77"], "34003")
    time.sleep(30)
    core.goto_order(["AP23", "LM77"], "34001")
    time.sleep(30)
    core.goto_order(["AP29", "LM77"], "34002")


def test_2():
    """
    场景 1: 最简单的双向路上两车对开
    :return: None
    """
    core.move_robot("34001", "LM117")
    core.move_robot("34002", "LM113")
    time.sleep(3)
    core.goto_order("AP32", "34001")
    core.goto_order("AP22", "34002")


def test_3():
    """
    场景 2: 比较近的两车在双向路上对开
    :return: None
    """
    core.move_robot("34001", "LM116")
    core.move_robot("34002", "LM114")
    time.sleep(3)
    core.goto_order("AP30", "34001")
    core.goto_order("AP27", "34002")


def test_4():
    """
    2号车来回转圈
    长沙地图
    :return: None
    """
    core.move_robot("34002", "LM220")
    core.move_robot("34003", "LM136")
    time.sleep(2)
    core.goto_order("AP19", "34002")
    core.goto_order("LM77", "34003")


def test_5():
    """
    只有一个机器人进算法时仍要原地等待
    :return: None
    """
    core.move_robot("34003", "LM287")
    core.move_robot("34002", "AP30")
    time.sleep(2)
    core.goto_order("AP31", "34003")
    core.goto_order("LM77", "34002")


def test_6():
    """
    一辆车停在工作站、另一辆车去同一目标点
    :return: None
    """
    # TODO(23-04-25): 添加一个区域, 当无法到达相同目标点时, 允许前往此区域
    core.move_robot('34003', 'LM77')
    core.move_robot('34002', 'AP34')
    time.sleep(2)
    core.goto_order('LM77', '34002')
    # core.goto_order('LM77', '34003', complete=False)


# dyb: 可加入 mapf 级别测试用例
def test_7():
    """
    已下发路线的旋转检测
    :return:
    """
    core.move_robot('34001', 'LM283')
    core.move_robot('34003', 'LM111')
    time.sleep(2)
    core.goto_order('AP36', '34001')
    core.goto_order('AP37', '34003')
