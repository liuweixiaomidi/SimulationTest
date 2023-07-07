import random
import time

import Lib.function as core

# 司米橱柜项目仿真

a_in = ['AP1036', 'AP1042', 'AP1077']  # A进仓口
a_package_1 = core.set_target_list(894, 924, remove=['AP896', 'AP898', 'AP900', 'AP901', 'AP903', 'AP905', 'AP906', 
                                                     'AP908', 'AP910', 'AP911', 'AP913', 'AP915', 'AP916', 'AP918',
                                                     'AP920', 'AP921', 'AP923'])    # A包装1线
a_package_2 = core.set_target_list(932, 964, remove=['AP933', 'AP935', 'AP936', 'AP938', 'AP940', 'AP941', 'AP943',
                                                     'AP945', 'AP946', 'AP948', 'AP950', 'AP951', 'AP952', 'AP955',
                                                     'AP956', 'AP957', 'AP960', 'AP961', 'AP962'])  # A包装2线
a_select = core.set_target_list(509, 521)
a_select += core.set_target_list(531, 543)
a_select += core.set_target_list(553, 565)
a_select += core.set_target_list(575, 587)
a_select += core.set_target_list(801, 840, remove=['AP804', 'AP806', 'AP807', 'AP811', 'AP813', 'AP814', 'AP818',
                                                   'AP820', 'AP821', 'AP825', 'AP827', 'AP828', 'AP832', 'AP834',
                                                   'AP835', 'AP839'])   # A分拣区
a_select += core.set_target_list(683, 728, remove=['AP697', 'AP702', 'AP703', 'AP705', 'AP710', 'AP711', 'AP714',
                                                   'AP717', 'AP719', 'AP727'])   # A分拣区

a_select += core.set_target_list(731, 766, remove=['AP734', 'AP737', 'AP739', 'AP743', 'AP745', 'AP747', 'AP749',
                                                   'AP755', 'AP756', 'AP761', 'AP763', 'AP764'])
a_select += ['AP11', 'AP12', 'AP21', 'AP22', 'AP31', 'AP32', 'AP41', 'AP42', 'AP51', 'AP52', 'AP61', 'AP62', 'AP71',
             'AP72', 'AP121', 'AP122', 'AP131', 'AP132', 'AP141', 'AP142', 'AP151', 'AP152', 'AP161', 'AP162']  # A分拣区
b_door = core.set_target_list(461, 463)
b_door += core.set_target_list(469, 471)
b_door += core.set_target_list(477, 479)
b_door += core.set_target_list(485, 487)
b_door += core.set_target_list(1007, 1017, remove=['AP1009', 'AP1011', 'AP1012', 'AP1016'])
b_door += ['AP390', 'AP394', 'AP395', 'AP396', 'AP845', 'AP847', 'AP843', 'AP852', 'AP854', 'AP850', 'AP853']   # B2号门
a_back_board = ['AP257', 'AP262', 'AP265', 'AP273', 'AP274', 'AP275', 'AP276', 'AP282', 'AP284', 'AP292', 'AP295',
                'AP297', 'AP299', 'AP300', 'AP304', 'AP312', 'AP314', 'AP320', 'AP324', 'AP329', 'AP332', 'AP333',
                'AP334', 'AP340', 'AP345', 'AP349', 'AP354', 'AP355', 'AP358', 'AP360', 'AP371', 'AP389', 'AP799']
a_back_board += core.set_target_list(364, 366)
a_back_board += core.set_target_list(375, 381)  # A背板区
a_back_board += core.set_target_list(767, 772, remove=['AP773', 'AP775', 'AP776', 'AP784', 'AP786', 'AP787', 'AP795'])


def zmf():
    # A分拣区 --> A进仓口 2
    # A分拣区 --> A进仓口 2
    # A背板区 --> A进仓口 1
    # A包装1 --> A进仓口 1
    # A包装2 --> A进仓口 1
    # B2号门 --> A进仓口 1
    count = 0
    while True:
        for _ in range(4):
            core.load_unload_order([random.choice(a_select), random.choice(a_in)])
        core.load_unload_order([random.choice(a_back_board), random.choice(a_in)])
        core.load_unload_order([random.choice(a_package_1), random.choice(a_in)])
        core.load_unload_order([random.choice(a_package_2), random.choice(a_in)])
        core.load_unload_order([random.choice(b_door), random.choice(a_in)])
        time.sleep(60)


def wcnmd():
    # 1 2 3 from A包装1 to AP then goto A分拣 A背板
    # 4 5 6 from A分拣 A背板 to AP then goto A包装1
    core.dis_point_path(['LM206', 'LM1026', 'LM1021', 'LM'])
    core.move_robot('sim_01', 'LM1038')
    core.move_robot('sim_02', 'LM901')
    # core.move_robot('sim_03', 'LM1053')
    core.move_robot('sim_04', 'LM213')
    core.move_robot('sim_05', 'LM1024')
    core.move_robot('sim_06', 'LM208')
    # core.move_robot('sim_07', 'LM1019')
    time.sleep(2)
    core.load_unload_order(['AP953', 'AP1042'], 'sim_01')
    core.load_unload_order(['AP309', 'AP1042'], 'sim_02')
    # core.load_unload_order(['AP917', 'AP1042'], 'sim_03')
    core.load_unload_order(['AP830', 'AP1042'], 'sim_04')
    core.load_unload_order(['AP796', 'AP1042'], 'sim_05')
    core.load_unload_order(['AP22', 'AP1042'], 'sim_06')
    time.sleep(2)
    core.goto_order('AP511', 'sim_01')
    core.goto_order('AP689', 'sim_02')
    core.goto_order('AP333', 'sim_03')
    core.goto_order('AP954', 'sim_04')
    core.goto_order('AP912', 'sim_05')
    core.goto_order('AP963', 'sim_06')
    set_goods_shape_while_load_unload()


def set_goods_shape_while_load_unload():
    flag = 0
    load_condition = [['sim_04', 'AP830'], ['sim_05', 'AP796'], ['sim_06', 'AP22']]
    while flag < 4:
        for robot in ['sim_04', 'sim_05', 'sim_06']:
            cur_location = core.get_current_location(robot)
            if [robot, cur_location] in load_condition:
                time.sleep(1)
                core.set_goods_shape(robot, -1.25, -0.5, 1.25, 0.5, 1.57)
            if cur_location == 'AP1042':
                time.sleep(1)
                core.set_goods_shape(robot, 0, 0, 0, 0)
                flag += 1
                time.sleep(0.2)
        time.sleep(0.5)


if __name__ == '__main__':
    # zmf()
    wcnmd()
