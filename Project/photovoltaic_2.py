import random
import time

from Lib.function import *


# 流水线上 --> 一道 EVA
# 流水线上 --> 电池片
# 流水线上 --> 汇流条

# 流水线中 --> 二道 EVA
# 流水线中 --> 背板

# 流水线下 --> 接线盒
# 流水线下 --> 大桶胶
# 流水线下 --> AB 胶

def run():
    flow_upon = set_target_list(2001, 2012)
    flow_midd = set_target_list(2295, 2296)
    flow_down = set_target_list(2401, 2402)
    eva_first = set_target_list(2013, 2026)
    batt_cell = set_target_list(2027, 2040)
    m_busbars = set_target_list(2041, 2054)
    target_mi = set_target_list(2055, 2082)
    target_do = set_target_list(2097, 2138)
    batt_cell += set_target_list(2083, 2096)

    total = 5
    done = True
    t23 = False
    t6 = False
    t2 = False
    t14 = False
    load_unload_order([random.choice(flow_upon), random.choice(eva_first)], label='small-upon')
    load_unload_order([random.choice(flow_midd), random.choice(target_mi)], label='small-middle')
    load_unload_order([random.choice(flow_upon), random.choice(batt_cell)], label='small-upon')
    load_unload_order([random.choice(flow_upon), random.choice(m_busbars)], label='small-upon')
    load_unload_order([random.choice(flow_down), random.choice(target_do)], label='small-down')
    time_start = time.time()
    tc23 = time.time()
    tc6 = time.time()
    tc2 = time.time()
    tc14 = time.time()
    while done:
        if time.time() - tc23 > 24 * 2:
            t23 = True
            tc23 = time.time()
        if time.time() - tc6 > 103 * 2:
            t6 = True
            tc6 = time.time()
        if time.time() - tc2 > 257 * 2:
            t2 = True
            tc2 = time.time()
        if time.time() - tc14 > 34 * 2:
            t14 = True
            tc14 = time.time()
        if t23:
            t23 = False
            load_unload_order([random.choice(flow_upon), random.choice(eva_first)], label='small-upon')
            total += 1
        if t14:
            t14 = False
            load_unload_order([random.choice(flow_midd), random.choice(target_mi)], label='small-middle')
            total += 1
        if t6:
            t6 = False
            load_unload_order([random.choice(flow_upon), random.choice(batt_cell)], label='small-upon')
            total += 1
        if t2:
            t2 = False
            load_unload_order([random.choice(flow_upon), random.choice(m_busbars)], label='small-upon')
            total += 1
            load_unload_order([random.choice(flow_down), random.choice(target_do)], label='small-down')
            total += 1
        if time.time() - time_start > 1200:
            done = False
        print(total)
        time.sleep(0.5)


if __name__ == '__main__':
    run()
