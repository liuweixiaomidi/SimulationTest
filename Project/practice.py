import pandas as pd

from Lib.function import *

# 设置库位
rk_bins = set_target_list(1, 6, title='RK-', fill=True)  # 入库
ck_bins = set_target_list(1, 6, title='CK-', fill=True)  # 出库
rg_bins = 'RG-02'  # 人工
dk_bins = 'DK'  # 打孔
jxb_1 = 'DJ'  # 第一个机械臂
jxb_2 = 'DS'  # 第二个机械臂

"""
1. CK: 1/2空, 1/2满(1/3打孔, 2/3人工), 发一个新订单
2. RG: 队列空(机械臂1), 队列满(入库, 封口)
3. DK: 1/2入库, 1/2人工
4. JXB1: 机械臂2
5. JXB2: 1/3打孔, 2/3入库(封口)
"""
m_ids = list()


def pre_run():
    global m_ids
    i = 0
    for ck in ck_bins:
        m_id = str(uuid.uuid1())
        goto_order([ck, jxb_1, jxb_2, rk_bins[i]], order_id=m_id)
        m_ids.append(m_id)
        i += 1
    time.sleep(25)
    for ck in ck_bins:
        m_id = str(uuid.uuid1())
        goto_order(ck, complete=False, order_id=m_id)
        m_ids.append(m_id)


def run():
    global m_ids
    block_ids = set()
    pre_run()
    time_start = time.time()
    while time.time() - time_start < 1800:
        for m_id in m_ids:
            if get_current_block_state(m_id) == 'FINISHED':
                cur_loc = get_current_block_location(m_id)
                cur_block_id = get_current_block_id(m_id)
                if cur_block_id in block_ids:
                    continue
                match cur_loc[:2]:
                    case 'CK':
                        options = [1, 2, 3]
                        probabilities = [60 / 100, 3 / 100, 37 / 100]
                        choice = random.choices(options, probabilities)[0]
                        if choice == 1:
                            add_block(rg_bins, m_id)
                        elif choice == 2:
                            add_block(dk_bins, m_id)
                        elif choice == 3:
                            add_block([jxb_1, jxb_2], m_id)
                        block_ids.add(cur_block_id)
                        cur_id = str(uuid.uuid1())
                        goto_order(location=cur_loc, complete=False, order_id=cur_id)
                        m_ids.append(cur_id)
                    case 'RG':
                        pos = set(get_robots_pos().values())
                        if {'LM66', 'LM67', 'LM68', 'LM69', 'LM75', 'LM146'}.issubset(pos):
                            add_block(random.choice(rk_bins), complete=True, order_id=m_id)
                        else:
                            add_block([jxb_1, jxb_2], order_id=m_id)
                        block_ids.add(cur_block_id)
                    case 'DK':
                        m_choice = random.random() < 1 / 2
                        if m_choice:
                            add_block(rg_bins, order_id=m_id)
                        else:
                            add_block(random.choice(rk_bins), complete=True, order_id=m_id)
                        block_ids.add(cur_block_id)
                    case 'DS':
                        m_choice = random.random() < 1 / 3
                        if m_choice:
                            add_block(dk_bins, order_id=m_id)
                        else:
                            add_block(random.choice(rk_bins), complete=True, order_id=m_id)
                        block_ids.add(cur_block_id)
                    case _:
                        continue
        time.sleep(2)


if __name__ == '__main__':
    run()
