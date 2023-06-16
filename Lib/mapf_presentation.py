import random
import time

import function as core

# 整体流程:
# PP --> 长通道 --> 左下库区 --> 下方右侧库区
# 两车右上演示 recover
# 两车右下演示 EF-5
# 两车长通道对开避让


def pre_park():
    count = 0
    while count != 5:
        core.goto_order('AP1049', group='PrePark')
        core.goto_order('AP1050', group='PrePark')
        core.goto_order('AP1051', group='PrePark')
        count += 1
        time.sleep(20)


def right():
    # 车 1 去 Loc-01, 停住不动
    # 车 2 去 Loc-02, 触发 recover, 任务完成后去 Loc-16, 停住不动
    # 车 3 去 Loc-02, 与回来的去 Loc-05 的车 2 触发避让逻辑
    # 车 4 去 Loc-14, 停住不动
    # 车 3 去 Loc-13, 同时车 4 停在 LM1085, 触发曲线检测
    core.goto_order('Loc-01', vehicle='sim_05')
    core.goto_order('Loc-14', vehicle='sim_08')
    time.sleep(3)
    core.goto_order('Loc-02', vehicle='sim_06')
    core.goto_order('Loc-05', vehicle='sim_06')
    time.sleep(10)
    # core.goto_order('Loc-02', vehicle='sim_07')


def recover():
    core.goto_order('Loc-01', group='right')
    time.sleep(3)
    core.goto_order('Loc-02', group='right')


def transfer():
    core.goto_order('Loc-01', vehicle='sim_05')
    core.goto_order('Loc-05', vehicle='sim_06')


def curve():
    # core.goto_order('Loc-15', vehicle='sim_05')
    # core.goto_order('Loc-16', vehicle='sim_06')
    core.goto_order('LM1095')
    core.goto_order('Loc-14', vehicle='sim_06')


def transport_init_aka_rotate():
    init_bins_left = core.set_target_list(1, 15)
    init_bins_right = core.set_target_list(16, 23)
    for _bin in init_bins_left:
        core.goto_order(_bin, label='transport-left')
    for _bin in init_bins_right:
        core.goto_order(_bin, label='transport-right')


def transport():
    direct_locs = core.set_target_list(38, 45)
    from_locs = core.set_target_list(54, 68)
    to_locs = core.set_target_list(24, 37)
    to_locs.append('AP46')
    for _bin in direct_locs:
        core.goto_order(_bin, label='transport-right')
    while len(from_locs) and len(to_locs):
        _from_bin = random.choice(from_locs)
        _to_bin = random.choice(to_locs)
        core.load_unload_order([_from_bin, _to_bin], label='transport-left')
        from_locs.remove(_from_bin)
        to_locs.remove(_to_bin)


if __name__ == '__main__':
    # pre_park()
    # recover()
    # transfer()
    # curve()
    # transport_init_aka_rotate()
    transport()
