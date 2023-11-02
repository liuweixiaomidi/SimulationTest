import random
import uuid

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
    for rk in rk_bins:
        m_id = str(uuid.uuid1())
        goto_order(rk, complete=False, order_id=m_id)
        m_ids.append(m_id)


def run():
    global m_ids
    pre_run()
    for m_id in m_ids:
        if get_current_block_state(m_id) == 'FINISHED':
            cur_loc = get_current_block_location(m_id)
            match cur_loc[:2]:
                case 'CK':
                    m_choice = random.random() < 1 / 6
                    add_block(dk_bins if m_choice else rg_bins, m_id)
                    cur_id = str(uuid.uuid1())
                    goto_order(location=cur_loc, complete=False, order_id=cur_id)
                    m_ids.append(cur_id)
                case 'RG':
                    pos = set(get_robots_pos().values())
                    if {'LM66', 'LM67', 'LM68', 'LM69', 'LM72', 'LM146'}.issubset(pos):
                        add_block(random.choice(rk_bins), complete=True, order_id=m_id)
                    else:
                        add_block([jxb_2, jxb_2], order_id=m_id)
                case 'DK':
                    pass
                case 'DJ':
                    pass
                case 'DS':
                    pass
                case 'RK':
                    pass
                case _:
                    continue


if __name__ == '__main__':
    run()
