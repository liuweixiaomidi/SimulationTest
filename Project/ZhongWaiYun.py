import random
import time

import Lib.function as core


def zwy():
    load_target = core.set_target_list(1, 13, title="CPF1-04", fill=True)
    # AP4
    while len(load_target):
        cur_load = random.choice(load_target)
        core.load_unload_order([cur_load, "AP4"])
        load_target.remove(cur_load)
        time.sleep(5)


def neighbor():
    load_target = core.set_target_list(1, 13, title="CPF1-04", fill=True)
    # AP4
    n = 2
    done = True
    while done:
        cur_load = load_target[n:n+3]
        for load in cur_load:
            core.load_unload_order([load, "AP4"])
        n += 3
        if n > 10:
            done = False
        time.sleep(120)


def zwy_0505():
    load_target = core.set_special_bin(title1='F', start1=8, end1=10, fill1=True,
                                       title2=['_'], start2=1, end2=4, fill2=True,
                                       title3='_', start3=1, end3=3, fill3=True)
    need_to_delete = ['F08_01_03', 'F10_01_02', 'F10_01_03']
    for i in need_to_delete:
        if i in load_target:
            load_target.remove(i)
    load_target += core.set_target_list(start=1, end=3, title='F09_05_', fill=True)
    load_target += core.set_target_list(start=1, end=3, title='F10_05_', fill=True)
    load_target += core.set_target_list(start=1, end=3, title='F10_06_', fill=True)
    # AP4
    while len(load_target):
        cur_load = random.choice(load_target)
        core.load_unload_order([cur_load, "AP4"], group='out-in-1-L')
        load_target.remove(cur_load)
        time.sleep(5)


def real_rbk():
    core.load_unload_order(['AP40', 'AP4'])
    core.load_unload_order(['AP41', 'AP4'])
    core.load_unload_order(['AP44', 'AP4'])
    core.load_unload_order(['AP45', 'AP4'])
    core.load_unload_order(['AP48', 'AP4'])
    core.load_unload_order(['AP618', 'AP4'])


if __name__ == '__main__':
    # zwy()
    # neighbor()
    # real_rbk()
    zwy_0505()
