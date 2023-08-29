import random

from Lib.function import *


# RCA 下料 --> ALD 上料
# ALD 上料 --> RCA 上料空花篮回传
# RCA 上下料转移
# # # # # # # # # # # # # # # #
# ALD 下料 --> 正 P 上料
# 正 P 下料 --> 背 P 上料
# 背 P 膜上料 --> 印刷上
# 印刷下 --> ALD 上空花篮回传
# 正 P 上下料转移
# 背 P 上下料转移

def init():
    move_robot('sim_01', 'PP2798')
    move_robot('sim_02', 'PP2797')
    for i in range(3, 19):
        if i < 10:
            r = 'sim_0' + str(i)
        else:
            r = 'sim_' + str(i)
        p = 'PP2' + str(i + 796)
        move_robot(r, p)
        time.sleep(0.1)
    for i in range(19, 22):
        r = 'sim_' + str(i)
        p = 'PP28' + str(i - 2)
        move_robot(r, p)
        time.sleep(0.1)
    for i in range(22, 34):
        r = 'sim_' + str(i)
        p = 'PP28' + str(i)
        move_robot(r, p)
        time.sleep(0.1)
    for i in range(34, 37):
        r = 'sim_' + str(i)
        p = 'PP28' + str(i + 2)
        move_robot(r, p)
        time.sleep(0.1)
    for i in range(37, 49):
        r = 'sim_' + str(i)
        p = 'PP28' + str(i + 3)
        move_robot(r, p)
        time.sleep(0.1)


# data = {
#     "AddWater": {
#         "is_open": true,
#         "status": 3
#     },
#     "args": {
#         "addingWater": "true"
#     },
#     "block_re_start_opt": [false, false, false, false, false, false],
#     "block_stop_opt": [false, false, false, false, false, false],
#     "cleanRobot": {
#         "cleanWaterLevel": 80,
#         "wasteWaterLevel": 0
#     },
#     "clean_water_level": 80.81742818584924,
#     "currentBlockId": "",
#     "getCanFrame_all": {
#         "braun_ball_valve": "4B80300764000000",
#         "brush_plate": "4B80300200000000",
#         "brush_plate_lift": "4B80300464000000",
#         "jet_water": "4B80300300000000",
#         "jet_water_valve": "4B80300600000000",
#         "suction_wing": "4B80300100000000",
#         "water_pa": "4B803005FF9C0000"
#     },
#     "status": 1,
#     "waste_water_level": 0.3084634663582032
# }


def run():
    # create bins by area
    rca_pickup_upon = set_target_list(284, 291)
    rca_pickup_down = set_target_list(292, 299)
    rca_unload_upon = set_target_list(332, 339)
    rca_unload_down = set_target_list(340, 347)
    ald_upon = set_target_list(348, 371)
    ald_pickup_upon = [ald_upon[i] for i in range(len(ald_upon)) if i % 2 == 0]
    ald_unload_upon = [ald_upon[i] for i in range(len(ald_upon)) if i % 2 != 0]
    ald_down = set_target_list(372, 395)
    ald_pickup_down = [ald_down[i] for i in range(len(ald_down)) if i % 2 == 0]
    ald_unload_down = [ald_down[i] for i in range(len(ald_down)) if i % 2 != 0]
    front_p_upon = set_target_list(396, 427)
    front_p_pickup_upon = [front_p_upon[i] for i in range(len(front_p_upon)) if i % 2 == 0]
    front_p_unload_upon = [front_p_upon[i] for i in range(len(front_p_upon)) if i % 2 != 0]
    front_p_down = set_target_list(428, 457)
    front_p_pickup_down = [front_p_down[i] for i in range(len(front_p_down)) if i % 2 == 0]
    front_p_unload_down = [front_p_down[i] for i in range(len(front_p_down)) if i % 2 != 0]
    back_p_upon = set_target_list(458, 485)
    back_p_pickup_upon = [back_p_upon[i] for i in range(len(back_p_upon)) if i % 2 == 0]
    back_p_unload_upon = [back_p_upon[i] for i in range(len(back_p_upon)) if i % 2 != 0]
    back_p_down = set_target_list(486, 509)
    back_p_pickup_down = [back_p_down[i] for i in range(len(back_p_down)) if i % 2 == 0]
    back_p_unload_down = [back_p_down[i] for i in range(len(back_p_down)) if i % 2 != 0]
    print_upon = set_target_list(550, 569)
    print_pickup_upon = [print_upon[i] for i in range(len(print_upon)) if i % 2 == 0]
    print_unload_upon = [print_upon[i] for i in range(len(print_upon)) if i % 2 != 0]
    print_down = set_target_list(570, 589)
    print_pickup_down = [print_down[i] for i in range(len(print_down)) if i % 2 == 0]
    print_unload_down = [print_down[i] for i in range(len(print_down)) if i % 2 != 0]
    # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # #
    # 节拍: 1单/2.5s; 退出条件: 按节拍进行 5min
    done = False
    start_time = time.time()
    while not done:
        # # # # # # # # # # # # # # # # # # # # # # cycle 3 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # RCA 下料 --> ALD 上料
        load_unload_order([random.choice(rca_unload_upon), random.choice(ald_pickup_upon)], label='rca_upon')
        load_unload_order([random.choice(rca_unload_down), random.choice(ald_pickup_down)], label='rca_down')
        # ALD 上料 --> RCA 上料空花篮回传
        load_unload_order([random.choice(ald_pickup_upon), random.choice(rca_pickup_upon)], label='rca_upon')
        load_unload_order([random.choice(ald_pickup_down), random.choice(rca_pickup_down)], label='rca_down')
        # RCA 上下料转移
        load_unload_order([random.choice(rca_pickup_upon), random.choice(rca_unload_upon)], label='rca_upon')
        load_unload_order([random.choice(rca_pickup_down), random.choice(rca_unload_down)], label='rca_down')
        # # # # # # # # # # # # # # # # # # # # # # cycle 4 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # ALD 下料 --> 正 P 上料
        load_unload_order([random.choice(ald_unload_upon), random.choice(front_p_pickup_upon)], label='a_to_fp_upon')
        load_unload_order([random.choice(ald_unload_down), random.choice(front_p_pickup_down)], label='a_to_fp_down')
        # 正 P 下料 --> 背 P 上料
        load_unload_order([random.choice(front_p_unload_upon), random.choice(back_p_pickup_upon)],
                          label='fp_to_bp_upon')
        load_unload_order([random.choice(front_p_unload_down), random.choice(back_p_pickup_down)],
                          label='fp_to_bp_down')
        # 背 P 膜上料 --> 印刷上
        load_unload_order([random.choice(back_p_pickup_upon), random.choice(print_pickup_upon)], label='bp_to_pr_upon')
        load_unload_order([random.choice(back_p_pickup_down), random.choice(print_pickup_down)], label='bp_to_pr_down')
        # 印刷下 --> ALD 上空花篮回传
        load_unload_order([random.choice(print_unload_upon), random.choice(ald_pickup_upon)], label='bp_to_pr_upon')
        load_unload_order([random.choice(print_unload_down), random.choice(ald_pickup_down)], label='bp_to_pr_down')
        # 正 P 上下料转移
        load_unload_order([random.choice(front_p_pickup_upon), random.choice(back_p_pickup_upon)], label='a_to_fp_upon')
        load_unload_order([random.choice(front_p_pickup_down), random.choice(back_p_pickup_down)], label='a_to_fp_down')
        # 背 P 上下料转移
        load_unload_order([random.choice(back_p_pickup_upon), random.choice(back_p_unload_upon)], label='fp_to_bp_upon')
        load_unload_order([random.choice(back_p_pickup_down), random.choice(back_p_unload_down)], label='fp_to_bp_down')
        if time.time() - start_time > 300:
            done = True
        time.sleep(60)


if __name__ == '__main__':
    # init()
    run()
