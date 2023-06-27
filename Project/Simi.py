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
                                                   'AP717', 'AP719'])   # A分拣区

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


if __name__ == '__main__':
    zmf()
