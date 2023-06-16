import random
import time

import Lib.function as core


def zhen_de_fan():
    area_a = core.set_target_list(151, 170)
    area_a += core.set_target_list(351, 370)
    area_a += core.set_target_list(514, 533)
    area_b = core.set_target_list(131, 138)
    area_b += core.set_target_list(331, 338)
    area_c = core.set_target_list(139, 146)
    area_c += core.set_target_list(339, 346)
    area_d = core.set_target_list(1, 56)
    area_d += core.set_target_list(201, 256)
    area_e = core.set_target_list(61, 116)
    area_e += core.set_target_list(261, 316)
    area_f = core.set_target_list(126, 130)
    area_f += core.set_target_list(326, 330)
    area_g = core.set_target_list(121, 125)
    area_g += core.set_target_list(321, 325)
    while len(area_g):
        loc_g = random.choice(area_g)
        loc_d = random.choice(area_d)
        core.load_unload_order([loc_g, loc_d])
        area_g.remove(loc_g)
        area_d.remove(loc_d)
        loc_d_1 = random.choice(area_d)
        area_d.remove(loc_d_1)
        loc_d_2 = random.choice(area_d)
        area_d.remove(loc_d_2)
        loc_a = random.choice(area_a)
        loc_b = random.choice(area_b)
        core.load_unload_order([loc_d_1, loc_a])
        core.load_unload_order([loc_d_2, loc_b])
        area_a.remove(loc_a)
        area_b.remove(loc_b)
        loc_a_1 = random.choice(area_a)
        loc_e = random.choice(area_e)
        core.load_unload_order([loc_a_1, loc_e])
        area_a.remove(loc_a_1)
        area_e.remove(loc_e)
        loc_c = random.choice(area_c)
        loc_e_1 = random.choice(area_e)
        core.load_unload_order([loc_c, loc_e_1])
        area_c.remove(loc_c)
        area_e.remove(loc_e_1)
        loc_e_2 = random.choice(area_e)
        loc_f = random.choice(area_f)
        core.load_unload_order([loc_e_2, loc_f])
        area_e.remove(loc_e_2)
        area_f.remove(loc_f)
        time.sleep(60)


if __name__ == '__main__':
    zhen_de_fan()
