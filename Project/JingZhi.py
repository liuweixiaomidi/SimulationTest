import random
import time

import Lib.function as core

"""
井智仿真
地图 scene_jingzhi0412
1. 共有上中下三个区域的库位
2. 中上之间有一个只有两个点位的独立库区 中间要去给它送货 下面不给它送货
3. 下面给中间送货
4. 中间给上方送货
5. 下面给上面送货
"""


def run():
    area_upon = []
    area_midd = []
    area_down = []
    area_miup = []
    area_miup += ["AP12", "AP21"]
    area_down += core.set_target_list(71, 76)
    area_down += core.set_target_list(51, 56)
    area_down += core.set_target_list(41, 45, "AP35")
    area_down += core.set_target_list(100, 105)
    area_down += core.set_target_list(112, 117)
    area_midd += ["AP22", "AP23", "AP132", "AP134"]
    area_upon += core.set_target_list(126, 129)
    area_upon += core.set_target_list(26, 29)
    print(len(area_down), len(area_miup), len(area_upon))
    while len(area_down) > 15:
        cur_down = random.choice(area_down)
        cur_upon = random.choice([random.choice(area_upon), random.choice(area_midd)])
        core.goto_order([cur_down, cur_upon])
        area_down.remove(cur_down)
        if len(area_down) > 20:
            core.goto_order([random.choice(area_midd), random.choice(area_upon)])
        if len(area_down) > 25:
            core.goto_order([random.choice(area_midd), random.choice(area_miup)])
        if len(area_down) > 28:
            time.sleep(2)
        else:
            time.sleep(30)


def recurrent_0515_1():
    core.move_robot('sim_04', 'LM17')
    core.move_robot('sim_03', 'LM152')
    time.sleep(2)
    core.goto_order('AP29', 'sim_03')
    core.goto_order('AP42', 'sim_04')


def recurrent_0515_2():
    core.move_robot('sim_01', 'LM5')
    core.move_robot('sim_02', 'AP100')
    time.sleep(2)
    core.goto_order('AP101', 'sim_01', ip='58.34.177.164')
    core.goto_order('AP127', 'sim_02', ip='58.34.177.164')


if __name__ == '__main__':
    recurrent_0515_2()
