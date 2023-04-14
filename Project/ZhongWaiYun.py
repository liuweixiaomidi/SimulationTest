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


if __name__ == '__main__':
    zwy()
