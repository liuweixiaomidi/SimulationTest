import math
import time
from operator import truediv
from xml.etree.ElementTree import indent

import requests
from fontTools.misc.psOperators import ps_integer
from pandas.core.groupby.categorical import recode_for_groupby

from Lib.config import linux_ip
from Lib.function import *

def chu_zhou_hui_ke():
    move_robot('L40-POL-134', 'LM8016')
    move_robot('L40-POL-132', 'AP8005')
    move_robot('L40-POL-133', 'AP8003')
    time.sleep(2)
    goto_order('CP8092', 'L40-POL-133')
    goto_order('CP8076', 'L40-POL-132')
    goto_order('AP8003', 'L40-POL-134')

def redo_change_water():
    dis_point_path(['CP1'])
    move_robot('SCL-AWG50-HMI', 'LM2')
    time.sleep(2)
    set_robot_speed('SCL-AWG50-HMI', 0.01)
    set_water_percentage('SCL-AWG50-HMI', 10)
    while True:
        if get_robot_state('SCL-AWG50-HMI') != 'RUNNING':
            time.sleep(.2)
            continue
        pos = get_robots_x_y_pos('SCL-AWG50-HMI')
        print(pos['x'])
        if pos['x'] < -1.6:
            fail_robot_task('SCL-AWG50-HMI')
            break
        time.sleep(.2)

def lift_conflict():
    move_robot('AMB-01', 'LM15')
    move_robot('AMB-03', 'LM3002')
    time.sleep(2)
    goto_order('K-11-T', 'AMB-03')
    goto_order('M-7-T', 'AMB-01')

def container_conflict():
    move_robot('warehouse-01', 'LM407')
    move_robot('warehouse-02', 'LM96')
    move_robot('warehouse-03', 'LM437')
    move_robot('warehouse-04', 'LM285')
    time.sleep(2)
    goto_order('AP383', 'warehouse-02')
    goto_order('AP72', 'warehouse-01')

def mapf_a_start():
    move_robot('2', 'LM725')
    move_robot('3', 'AP891', -math.pi/2)
    time.sleep(2)
    goto_order('AP888', '2')

def ting_yang():
    agvs = set_target_list(1, 9, title='warehouse-', fill=True)
    move_robot(agvs[0], 'LM5126', -math.pi/2)
    move_robot(agvs[1], 'LM955', 0)
    move_robot(agvs[2], 'LM316', 0)
    move_robot(agvs[3], 'LM378', 0)
    move_robot(agvs[4], 'LM563', 0)
    move_robot(agvs[5], 'AP4675', 0)
    time.sleep(2)
    goto_order('AP4675', agvs[0])
    goto_order('AP264', agvs[3])
    goto_order('AP540', agvs[2])
    goto_order('AP356', agvs[1])
    goto_order('AP80', agvs[4])
    goto_order('AP1002', agvs[5])

def ting_yang_out_of_mapf():
    move_robot('warehouse-01', 'AP756')
    move_robot('warehouse-02', 'AP750')
    time.sleep(2)
    goto_order('AP759', 'warehouse-02')
    goto_order('AP777', 'warehouse-01')

def spain_near_5_bins():
    goto_order('AP891')
    goto_order('AP895')
    goto_order('AP894')
    goto_order('AP893')
    goto_order('AP892')

def remove_first_point():
    set_robot_speed('AGV-W01', 0.005)
    move_robot('AGV-W01', 'LM569')
    time.sleep(2)
    goto_order('TL562', 'AGV-W01')
    time.sleep(.5)
    while True:
        pos = get_robots_x_y_pos('AGV-W01')
        if pos['y'] < 52.7:
            fail_robot_task('AGV-W01')
            break
        time.sleep(.2)

def rob_block_replan():
    move_robot('sim_01', 'PP35')
    move_robot('sim_02', 'PP36')
    time.sleep(2)
    set_robot_speed('sim_01', 0.4)
    set_robot_speed('sim_02', 0.4)
    time.sleep(2)
    goto_order('AP29', 'sim_01')
    goto_order('AP38', 'sim_02')
    time.sleep(2)
    while True:
        if get_robot_state('sim_01') != 'RUNNING':
            time.sleep(.2)
            continue
        pos = get_robots_x_y_pos('sim_01')
        print(pos['x'])
        if pos['x'] > -5.0:
            set_robot_emergency('sim_01')
            break
        time.sleep(.2)

def long_time_cost():
    # warehouse-05 LM5003 --> 262805
    # warehouse-06 LM4 --> 210105
    # warehouse-07 LM563 --> ws8
    # warehouse-08 LM747 --> ws2
    move_robot('warehouse-05', 'LM5003')
    move_robot('warehouse-06', 'LM4')
    move_robot('warehouse-07', 'LM563')
    move_robot('warehouse-08', 'LM747')
    time.sleep(2)
    goto_order('262805', 'warehouse-05')
    goto_order('210105', 'warehouse-06')
    goto_order('ws8', 'warehouse-07')
    goto_order('ws2', 'warehouse-08')

def rob_stop_replan():
    move_robot('sim_01', 'LM43')
    move_robot('sim_02', 'LM44')
    time.sleep(2)
    set_robot_speed('sim_01', 0.4)
    set_robot_speed('sim_02', 0.4)
    time.sleep(2)
    goto_order('AP34', 'sim_01')
    goto_order('AP34', 'sim_02')
    time.sleep(2)
    while True:
        if get_robot_state('sim_01') != 'RUNNING':
            time.sleep(.2)
            continue
        pos = get_robots_pos()['sim_01']
        print(pos)
        if pos == 'LM17':
            terminate_order(['sim_01'])
            break
        time.sleep(.2)

def ykk():
    # move_robot('RIL-L-8235', 'LM7')
    # move_robot('RIL-L-8234', 'LM229')
    # move_robot('RIL-L-8233', 'LM230')
    # move_robot('RIL-L-8236', 'LM231')
    time.sleep(.5)
    goto_order('LM232', 'RIL-L-8234')
    goto_order('LM232', 'RIL-L-8235')
    goto_order('LM8245', 'RIL-L-8236')
    goto_order('LM232', 'RIL-L-8233')

def yun_lai():
    move_robot('DS-04', 'PP944')
    move_robot('DS-03', 'PP942')
    time.sleep(2)
    set_goods_shape('DS-04', -3.4, -0.3, 3.4, 0.3, autoLoad=True)
    set_goods_shape('DS-03', -3.4, -0.3, 3.4, 0.3, autoLoad=True)
    time.sleep(2)
    oid = get_random_str()
    load_unload_order(['LM972', 'AP157'], 'DS-03', reverse=True, complete=False, order_id=oid)
    load_unload_order(['LM972', 'AP156'], 'DS-04')
    time.sleep(10)
    add_block('LM91', oid, True)

def spain():
    bins = set_target_list(449, 453, single=['AP442', 'AP528', 'AP529', 'AP531', 'AP533', 'AP517', 'AP525'])
    for i in range(15):
        goto_order(random.choice(bins))

def multi_lift():
    bins = ['AP1054', 'AP1057', 'AP1062', 'AP1067', 'AP1072']
    agvs = ['CBD-16-41', 'CBD-16-24', 'CBD-16-36', 'sim_01', 'sim_02']
    for b, a in zip(bins, agvs):
        goto_order(b, a)
        time.sleep(1)

def multi_lift_philips():
    pps = ['PP1019', 'AP973', 'AP965', 'AP597', 'AP598', 'AP892']
    agvs = set_target_list(1, 6, title='SW500-', fill=True)
    bins = ['AP2100', 'AP2107', 'AP2353', 'AP2356', 'AP2354', 'AP2427']
    set_dispatchable_status([], DispatchStatus.ignore)
    set_dispatchable_status(agvs, DispatchStatus.dispatchable)
    for r, p in zip(agvs, pps):
        move_robot(r, p)
        time.sleep(0.2)
    time.sleep(5)
    for r, b in zip(agvs, bins):
        goto_order(b, r)
        time.sleep(0.5)

def bei_tuo_wait_point():
    agvs = set_target_list(1, 2, title='BT-', fill=True)
    pps = ['AP180', 'AP178']
    bins = [['AP544', 'AP185'], 'AP169']
    for r, p in zip(agvs, pps):
        move_robot(r, p)
        time.sleep(0.2)
    for r, b in zip(agvs, bins):
        goto_order(b, r)
        time.sleep(0.5)

def hui_che():
    move_robot('AMB-01', 'LM1921')
    move_robot('AMB-07', 'LM1299')
    time.sleep(2)
    goto_order('AP1943', 'AMB-01')
    goto_order('AP788', 'AMB-07')

def extra_radius():
    move_robot('23', 'LM1217', 3.14)
    move_robot('15', 'AP561', 3.14)
    time.sleep(2)
    goto_order('AP129', '15')

def another_extra_radius():
    move_robot('23', 'LM568', 1.57)
    move_robot('15', 'AP563', 3.14)
    time.sleep(2)
    goto_order('AP566', '15')

def extra_radius_1():
    """
    3
    |
    2-1-O
    |
    4-5-6
    |
    7
    1 5 额外半径, 0有车时, 其他车可以去 6
    """
    move_robot('23', 'AP566', 3.14)
    move_robot('15', 'LM562', 1.57)
    time.sleep(2)
    goto_order('AP563', '15')

def extra_radius_2():
    """
    3
    |
    2-1-O
    |
    4-5-6
    |
    7
    1 5 额外半径, 机器人 a b 分别在 0 6
    b 去 5, 可以去; 继续让 a 去 1, 不能去
    """
    move_robot('23', 'LM1217', 3.14)
    move_robot('15', 'LM562', 1.57)
    time.sleep(2)
    goto_order('AP563', '15')

def extra_radius_3():
    """
    3
    |
    2-1-O
    |
    4-5-6
    |
    7
    1 5 额外半径, 1有车时, 其他车不可以去 6, 停在 7
    """
    move_robot('23', 'LM1217', 3.14)
    move_robot('15', 'LM562', 1.57)
    time.sleep(2)
    goto_order('AP563', '15')

def fork_auto_fluent_1():
    """
    3
    |
    2-1-O
    |
    4-5-6
    |
    7
    叉车停在 0, 另一台叉车上去如果不能通过, 只能停在 7, 不能停在 4 2 3
    """

def fork_auto_fluent_2():
    """
    3
    |
    2-1-O
    |
    4-5-6
    |
    7
    叉车停在 0, 另一台叉车从下向上去 4, 可以去, 因为是目标点
    """

def fork_auto_fluent_3():
    """
    8
    |
    3-9-10
    |
    2-1-O
    |
    4-5-6
    |
    7
    叉车 a 停在 0, 叉车 b 停在 8, 另一台叉车从下向上去 10
    由于 b 阻挡, 无法到达, 只能停在 7, 不能停在 4
    此时让 a 车去 1, 需要能够执行 (现有机制下, 这似乎是个无解的死锁)
    """
    move_robot('23', 'AP566', 3.14)
    move_robot('15', 'LM562', 1.57)
    move_robot('12', 'LM434', -1.57)
    time.sleep(2)
    goto_order('AP567', '15')

def goto_pre_point_at_same_time():
    goto_order('LM1217', '23')
    goto_order('LM564', '15')

def get_clean_robot_status(r_name: str):
    while True:
        get_clean_robot_property(r_name)
        time.sleep(2)

def fork_recognize_theta():
    move_robot('OQC-137', 'LM22132', 1.57)
    time.sleep(2)
    clear_goods_shape(['OQC-137'])
    time.sleep(2)
    goto_order('AP22130', 'OQC-137', recognize=True)

def fork_height():
    data = {
        'id': get_random_str(),
        'complete': True,
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'Loc-162',
                'binTask': 'ForkLoad'
            },
            {
                'blockId': get_random_str(),
                'location': 'Loc-201',
                'binTask': 'ForkUnload'
            }
        ]
    }
    requests.post('http://127.0.0.1:8088/setOrder', json=data)

def dis_rotate_bug():
    set_position_by_edge('sim_01', 'LM18', 'LM17', 0.44)
    time.sleep(1)
    set_robot_angle('sim_01', -3.14)
    time.sleep(2)
    goto_order('LM16')

def send_loop_order(vehicle: str):
    data = {
        'id': get_random_str(),
        'vehicle': vehicle,
        'loopPoints': [
            'LM3',
            'LM4',
            'LM13',
            'LM6',
            'LM8',
            'LM9',
            'LM12',
            'LM11',
        ]

    }
    requests.post('http://127.0.0.1:8088/setOrder', json=data)

def send_loop_order_2(vehicle: str):
    data = {
        'id': get_random_str(),
        'vehicle': vehicle,
        'loopPoints': [
            'LM20',
            'LM21',
            'LM22',
            'LM23',
            'LM24',
            'LM25',
            'LM26',
            'LM27',
        ]

    }
    requests.post('http://127.0.0.1:8088/setOrder', json=data)

def stop_safe_dist():
    move_robot('sim_01', 'PP1')
    move_robot('sim_02', 'PP3')
    time.sleep(2)
    goto_order('AP25')
    goto_order('AP25')

def stop_safe_dist_pro():
    move_robot('sim_01', 'PP1')
    move_robot('sim_02', 'PP3')
    time.sleep(2)
    goto_order('PP7', 'sim_02')
    goto_order('PP9', 'sim_01')

def russia():
    move_robot('sim_001', 'LM137')
    move_robot('CPD15-1', 'LM136')
    time.sleep(2)
    goto_order('AP1', 'sim_001')
    goto_order('CP216', 'CPD15-1')

def adg_circle():
    move_robot('sim_01', 'LM30')
    move_robot('sim_02', 'LM32')
    time.sleep(2)
    goto_order('AP28', 'sim_02')
    goto_order('AP36', 'sim_01')

def adg_circle_origin():
    move_robot('RJ-66', 'LM3171')
    move_robot('RJ-12', 'LM3201')
    time.sleep(2)
    goto_order('AP6517', 'RJ-12')
    goto_order('AP6192', 'RJ-66')

def adg_transfer():
    move_robot('AGV-08', 'LM41')
    move_robot('AGV-06', 'LM322')
    time.sleep(2)
    goto_order('AP171', 'AGV-08')
    goto_order('LM20', 'AGV-06')

def hexing():
    order_template('CDD14-01', 'LM409', 'LM1', 'CBD15-01', 'LM401', 'AP442')

def chu_zhou():
    order_template('OQC-136', 'LM22106', 'LM22030', 'OQC-137', 'AP22071', 'AP22072')

def queue():
    init = ['LM'+str(i) for i in range(50, 58)]
    agvs = ['AMB-'+str(i) for i in range(1, 9)]
    target = 'AP23'
    next_target = ['LM89'] + ['LM'+str(i) for i in range(45, 39, -1)] + ['LM38']
    result = [[agvs[i], init[i], [target, next_target[i]]] for i in range(len(init))]
    print(result)
    order_template_complex(*[item for sublist in result for item in sublist])

def circle_mapf():
    order_template('AMB-01', 'LM71', 'AP33', 'AMB-02', 'AP20', 'AP104')

def single_point_no_rotate():
    # move_robot('CBD15-01', 'LM2025')
    # time.sleep(2)
    set_position_by_edge('CBD15-01', 'LM203', 'PP2038', 0.2725)
    time.sleep(2)
    set_robot_angle('CBD15-01', 3.14)

def fix_multi_path():
    single_order_template('AMB-01', 'AP30', 'AP5')
    time.sleep(30)
    move_robot_by_xy('AMB-01', -7.23, 1.37)
    time.sleep(2)
    goto_order('AP23', 'AMB-01')

def control_mapf():
    pass

def seer_pre():
    move_robot('CDD15-3M', 'LM40')
    move_robot('Box-01', 'LM12')
    move_robot('300L', 'LM26')
    move_robot('SWW45V1003', 'LM25')
    move_robot('SCL-AWG50-HMI', 'LM8')
    move_robot('CBD16-S', 'LM6')

def mapf_wait():
    move_robot('F1-AGV-122', 'AP4609')
    move_robot('F1-AGV-145', 'LM4608')
    move_robot('F1-AGV-119', 'AP4610')
    time.sleep(2)
    goto_order('LM4884', 'F1-AGV-122', complete=False)
    goto_order('AP4580', 'F1-AGV-145')
    goto_order('AP4583', 'F1-AGV-119')

def finished_path():
    move_robot('sim_01', 'PP81')
    time.sleep(2)
    # dis_point_path(['LM57'])
    # time.sleep(2)
    oid = get_random_str()
    goto_order('AP73', 'sim_01', order_id=oid)
    time.sleep(2)
    for _ in range(100):
        o_state = get_order_state(oid)
        if o_state == 'FINISHED':
            break
        print(o_state, get_robot_finished_path('sim_01'))
        time.sleep(0.2)
        print(o_state, get_robot_unfinished_path('sim_01'))
        time.sleep(1)

def fushikang():
    # order_template('AGV-WL3-42', 'LM13669', 'LM13667', 'AMR-HL12-32', 'LM1611', 'LM1609')
    move_robot('AGV-WL3-42', 'LM13672')
    move_robot('AMR-HL12-32', 'LM1609')
    time.sleep(2)
    goto_order('LM13667', 'AGV-WL3-42')
    goto_order('LM1611', 'AMR-HL12-32')
    time.sleep(2)
    while get_robot_state('AMR-HL12-32') != 'FINISHED':
        time.sleep(0.4)
    time.sleep(15)
    goto_order('LM1609', 'AMR-HL12-32')

def send_cancel_loop_order(vehicle: str):
    data = {
        'id': get_random_str(),
        'loopPoints': ['LM' + str(_i) for _i in range(1, 13)],
        'vehicle': vehicle
    }
    requests.post('http://127.0.0.1:8088/setOrder', json=data)

def witch():
    move_robot('AGV-HP-22', 'LM8074')
    move_robot('AGV-HP-24', 'LM182')
    time.sleep(2)
    goto_order('LM8065', 'AGV-HP-24')
    time.sleep(2)
    goto_order('LM200', 'AGV-HP-22')

def zhan_hui():
    agvs = ['sim_0' + str(_i) for _i in range(1, 7)]
    init = ['LM' + str(_i) for _i in range(1, 12) if _i % 2 != 0]
    for agv, pos in zip(agvs, init):
        move_robot(agv, pos)
        time.sleep(0.2)
    for agv in agvs:
        send_cancel_loop_order(agv)
        time.sleep(0.1)
    time.sleep(20)
    for agv in agvs:
        assert get_robot_state(agv) == 'RUNNING'
        time.sleep(0.2)
    random_two = random.sample(agvs, 2)
    data = {
        random_two[0]: 'AP20',
        random_two[1]: 'AP30'
    }
    go_away_loop(data)
    time.sleep(5)
    t_start = time.time()
    while True:
        if time.time() - t_start > 300:
            assert False, 'time out!!!'
        cond = True
        for agv in agvs:
            if get_robot_state(agv) != 'FINISHED':
                cond = False
                break
            time.sleep(0.2)
        if cond:
            break
        time.sleep(2)

def zhan_hui_run():
    failure_count = 0
    for i in range(50):
        try:
            zhan_hui()
        except AssertionError:
            failure_count += 1
        if i < 49:
            time.sleep(5)
    print(f"断言失败的次数: {failure_count}")

def movable_queue_park():
    move_robot('AMB-01', 'PP218', 1.57)
    move_robot('AMB-02', 'PP219', 1.57)
    move_robot('AMB-03', 'PP220', 1.57)
    move_robot('AMB-05', 'LM12')
    time.sleep(2)
    oid = get_random_str()
    goto_order('AP115', 'AMB-05', complete=False, order_id=oid)
    while get_robot_state('AMB-05') != 'WAITING':
        time.sleep(1)
    time.sleep(2)
    add_block('AP256', oid, True)

def fork_chanel_latest():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('F1-AGV-119', 'AP4588')
    move_robot('F1-AGV-146', 'AP44930')
    time.sleep(2)
    goto_order('LM4884', 'F1-AGV-146', complete=False)
    time.sleep(15)
    goto_order('PP4598', 'F1-AGV-119')

def fork_chanel():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('F1-AGV-119', 'LM4883')
    move_robot('F1-AGV-122', 'LM4882')
    move_robot('F1-AGV-146', 'AP44928')
    time.sleep(2)
    goto_order('LM4884', 'F1-AGV-119', complete=False)
    goto_order('AP44930', 'F1-AGV-122', complete=False)
    time.sleep(20)
    goto_order('AP4593', 'F1-AGV-146')
    time.sleep(30)
    if get_robots_pos()['F1-AGV-146'] == 'AP44929':
        assert False

def fork_chanel_run():
    failure_count = 0
    for i in range(50):
        print(f"第{i}次执行")
        try:
            fork_chanel()
        except AssertionError:
            failure_count += 1
        if i < 49:
            time.sleep(5)
    print(f"断言失败的次数: {failure_count}")

def scene_disconnect():
    for i in range(50):
        requests.get('http://127.0.0.1:8088/scene')
        print(f"getScene: {i}")
        time.sleep(10)

def zhong_dian_ke():
    terminate_all_order()
    time.sleep(2)
    move_robot('AMB-01', 'LM1021')
    time.sleep(2)
    oid = get_random_str()
    goto_order('XBJ03_1', 'AMB-01', complete=False, order_id=oid)
    start_time = time.time()
    while time.time() - start_time < 60:
        if get_robot_state('AMB-01') == 'WAITING':
            break
        time.sleep(1)
    add_block('XBJ03_1', oid, False)
    time.sleep(2)
    start_time = time.time()
    while time.time() - start_time < 60:
        if get_robot_state('AMB-01') == 'WAITING':
            break
        time.sleep(1)
    move_robot('AMB-02', 'LM1040')
    add_block('XBJ03_1', oid, False)
    goto_order('PP434', 'AMB-02')
    time.sleep(2)
    start_time = time.time()
    while time.time() - start_time < 60:
        if get_robot_state('AMB-01') == 'WAITING':
            break
        time.sleep(1)
    add_block('ZP01_DOWN_2', oid, False)

def phillips():
    init = ['PP847', 'PP848', 'PP885', 'PP887', 'PP888']
    agvs = ['SW500-03', 'SW500-01', 'SW500-12', 'SW500-04', 'SW500-11']
    target = ['AP2441', 'AP2434', 'AP2445', 'AP2442', 'AP2443']
    result = [[agvs[i], init[i], [target[i]]] for i in range(len(init))]
    print(result)
    order_template_complex(*[item for sublist in result for item in sublist])

def core_dump():
    set_goods_shape('TK-05', -1, -0.85, 0.9, 0.8)
    set_goods_shape('TK-08', -1, -0.85, 0.9, 0.8)
    time.sleep(2)
    order_template('TK-05', 'LM1056', 'AP1002', 'TK-08', 'AP1002', 'B')

def mutex_mapf():
    terminate_all_order()
    time.sleep(2)
    order_template('AMR-HL12-32', 'LM1611', 'LM1612', 'AGV-WL1-40', 'LM18819', 'LM13898')

def extreme_collision():
    move_robot('sim_03', 'LM183', -1.57)
    move_robot('sim_04', 'AP2', 0)
    move_robot('sim_05', 'AP1', 0)
    time.sleep(2)
    goto_order('AP7', 'sim_04')
    goto_order('AP1', 'sim_03')
    time.sleep(5)
    goto_order('AP8', 'sim_05')

def korea():
    move_robot('AMB-01', 'LM20', 3.14)
    move_robot('AMB-02', 'LM13', 0)
    time.sleep(2)
    goto_order('LM20', 'AMB-02')
    goto_order('LM13', 'AMB-01')

def fluent_coredump():
    move_robot('CBD-01', 'LM58', 0, ip='192.168.9.201')
    move_robot('CBD-02', 'AP228', 1.57, ip='192.168.9.201')
    time.sleep(2)
    goto_order('AP227', 'CBD-01', ip='192.168.9.201')

def mapf_agv_adjust():
    # terminate_all_order()
    # move_robot('sim_01', 'PP7')
    # move_robot('sim_02', 'PP9')
    # move_robot('sim_03', 'PP81')
    # time.sleep(2)
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps({
        'id': get_random_str(),
        'vehicle': 'sim_02',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP42',
            'operation': 'Wait',
            'adjustInfo': [{
                'points': 'AP42',
                'range': 3
                # 'region': [
                #     {'x': +1, 'y': +1.5},
                #     {'x': +1, 'y': -1.5},
                #     {'x': -2, 'y': -1.5},
                #     {'x': -2, 'y': +1.5},
                # ]
            }]
        }]
    }))
    # goto_order('AP42', 'sim_02', recognize=True)
    time.sleep(2)
    # goto_order('AP43', 'sim_01')
    # goto_order('AP162', 'sim_03')

def reduce_circle():
    terminate_all_order()
    move_robot('JRI-4', 'LM11', -1.57)
    move_robot('JFR-3', 'LM87', 0)
    time.sleep(2)
    goto_order('LM88', 'JFR-3', complete=False)
    goto_order('LM88', 'JRI-4')

def mapf_rst_a():
    move_robot('JRI-4', 'AP214', -1.57)
    move_robot('JFR-2', 'LM307', 3.14)
    time.sleep(2)
    goto_order('AP212', 'JRI-4')
    goto_order('AP220', 'JFR-2')

def mapf_adjust_self_position():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status(['sim_03', 'sim_04', 'sim_05'], DispatchStatus.ignore)
    time.sleep(2)
    set_dispatchable_status(['sim_01', 'sim_02'], DispatchStatus.dispatchable)
    move_robot('sim_02', 'PP9')
    move_robot('sim_01', 'AP43')
    time.sleep(2)
    oid = get_random_str()
    goto_order('AP42', 'sim_02', complete=False, order_id=oid)
    time.sleep(60)
    data = {
        'id': oid,
        'complete': False,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP42',
            'operation': 'Wait',
            'adjustInfo': [{
                'points': 'AP42',
                'range': 2.5
            }]
        }]
    }
    requests.post('http://' + '127.0.0.1' + ':8088/addBlocks', json.dumps(data))
    time.sleep(3)
    goto_order('AP49', 'sim_01')

def kate_adg():
    terminate_all_order()
    set_dispatchable_status([], DispatchStatus.ignore)
    set_dispatchable_status(['CPD15-dbf', 'Fork-16', 'Fork-11'], DispatchStatus.dispatchable)
    move_robot('CPD15-dbf', 'AP3490', 0)
    move_robot('Fork-16', 'LM1069', 1.57)
    move_robot('Fork-11', 'LM2488', 1.57)
    time.sleep(2)
    goto_order('LM2975', 'CPD15-dbf')
    goto_order('LM274', 'Fork-16')
    goto_order('LM2665', 'Fork-11')

def fork_path_plan_fail():
    goto_order('AP11', 'AMB-02')
    time.sleep(7)
    set_reach_deviation(['AMB-02'], 0.07)

def mapf_with_mutex():
    move_robot('sim_01', 'LM62', 3.14)
    move_robot('sim_02', 'PP82', 3.14)
    time.sleep(2)
    goto_order('AP74', 'sim_01')
    goto_order('AP78', 'sim_02')

def mapf_adjust_requirement_2():
    """
    基础需求 1 只考虑了我在调整时, 你不能过来
    需求 2 需要考虑你在过来路上, 那我就不能调整
    :return:
    """
    terminate_all_order()
    time.sleep(2)
    delete_all_orders()
    time.sleep(2)
    modify_param({'RDSDispatcher': {
        'AutoPark': False,
        'ClearDBOnStart': True,
        'CloseChargeParkError': True,
        'DelayFinishTime': 20
    }})
    move_robot('sim_01', 'LM21')
    move_robot('sim_02', 'LM22')
    time.sleep(2)
    oid = get_random_str()
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps({
        'id': oid,
        'vehicle': 'sim_02',
        'complete': False,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP44',
            'operation': 'Wait',
            'adjustInfo': [{
                'points': 'AP44',
                'range': 3
            }]
        }]
    }))
    goto_order('AP50', 'sim_01')
    start_time = time.time()
    while get_current_location('sim_02') != 'AP44' and time.time() - start_time < 60:
        time.sleep(2)
    time.sleep(5)
    loc_1 = get_current_location('sim_01')
    assert loc_1 == 'LM38', loc_1
    time.sleep(2)
    loc_2 = get_current_location('sim_01')
    sta_1 = get_order_state(oid)
    assert loc_2 == 'LM38' and sta_1 == 'RUNNING', {loc_2, sta_1}
    modify_param({'RDSDispatcher': {
        'DelayFinishTime': 0,
    }})
    time.sleep(2)
    start_time = time.time()
    while get_order_state(oid) != 'WAITING' and time.time() - start_time < 20:
        time.sleep(2)
    time.sleep(0.5)
    ex_item = {
        'adjustInfo': [{
            'points': 'AP44',
            'range': 3
        }]
    }
    add_block('Loc-3', oid, True, pair=ex_item)
    time.sleep(2)
    sta_2 = get_order_state(oid)
    assert sta_2 == 'RUNNING', sta_2
    start_time = time.time()
    while get_current_location('sim_01') != 'LM48' and time.time() - start_time < 60:
        time.sleep(2)
    sta_3 = get_order_state(oid)
    assert sta_3 == 'FINISHED', sta_3

def auto_order_record():
    start_time = time.time()
    while time.time() - start_time < 90:
        print(get_robot_auto_order_status([], AutoOrderType.park))
        time.sleep(1)

def query_frequency():
    start_time = time.time()
    while time.time() - start_time < 600:
        res = requests.get('http://' + config.ip + ':8088/orders').json()
        print(res)
        time.sleep(9)

def get_topo_pos():
    data = requests.get('http://' + config.ip + ':8088/robotsStatus').json()
    for r in data['report']:
        if r['vehicle_id'] == 'CBD16-S':
            return r['area_resources_occupied'][0]['path_occupied']
    return []

def no_rotate_in_mid_path():
    move_robot('CBD16-S', 'CP81', 1.57)
    time.sleep(2)
    data = get_topo_pos()
    if len(data) <= 2:
        assert False, f'unexpected path occupy: {len(data), data}'
    goto_order('PP108', 'CBD16-S')
    time.sleep(20)
    f_path = get_robot_finished_path('CBD16-S')
    assert 'LM80' in f_path, f'wrong path: {f_path}'

def no_rotate_in_mid_path_simple():
    move_robot_by_xy('CBD16-S', -1, -4.041)
    set_robot_angle('CBD16-S', 1.57)
    time.sleep(2)
    goto_order('LM110', 'CBD16-S')

def stop_safe_dist_with_2_point():
    move_robot('sim_01', 'LM22')
    move_robot('sim_02', 'LM23')
    time.sleep(2)
    goto_order('LM23', 'sim_01')

def jin_bo_lift():
    move_robot('R-WL-AGV-001', 'AP15127')
    time.sleep(2)
    goto_order('AP20004', 'R-WL-AGV-001')

def recognize_resource():
    move_robot('AGV-F3-52', 'LM2398', 1.57)
    move_robot('AGV-F3-55', 'LM3023', 1.57)
    time.sleep(2)
    set_robot_speed('AGV-F3-55', 0.1)
    time.sleep(2)
    goto_order('AP2364', 'AGV-F3-55', operation='JackLoad', recognize=True)
    time.sleep(1)
    goto_order('AP2411', 'AGV-F3-52')

def replan_path():
    move_robot('AMR-HL03-33', 'LM1022', 1.57)
    move_robot('AMR-HL04-34', 'LM1027', -1.57)
    time.sleep(2)
    goto_order('LM1023', 'AMR-HL03-33')
    goto_order('LM1069', 'AMR-HL04-34')

def min_dist():
    move_robot('LIFT-02', 'LM238')
    move_robot('LIFT-04', 'LM147')
    time.sleep(2)
    # goto_order('AP200', 'LIFT-04')
    # goto_order('AP207', 'LIFT-02')

def mapf_pp_crash():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.ignore)
    time.sleep(2)
    set_dispatchable_status(['F3-AGV-102', 'F3-AGV-105', 'F3-AGV-113'], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('F3-AGV-105', 'AP3110', -1.57)
    move_robot('F3-AGV-102', 'PP2749', +1.57)
    move_robot('F3-AGV-113', 'AP3107', +1.57)
    time.sleep(2)
    goto_order('CP2804', 'F3-AGV-105')
    goto_order('AP2808', 'F3-AGV-113')

def order_issue_pool_10666():
    """
    多车型下的禁止旋转属性会导致死锁
    :return:
    """
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.ignore)
    time.sleep(2)
    set_dispatchable_status(['CBD-10', 'CDD-20'], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('CBD-10', 'CP71', 3.14)
    move_robot('CDD-20', 'LM20374', 1.57)
    time.sleep(2)
    goto_order('AP20371', 'CDD-20')

def order_issue_pool_10650():
    """
    路线选择不合理, 选择了转弯更多的路线
    :return: None
    """
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.ignore)
    time.sleep(2)
    set_dispatchable_status(['AGV-F2-63', 'AGV-F2-70'], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('AGV-F2-63', 'AP1346')
    move_robot('AGV-F2-70', 'LM1297')
    time.sleep(2)
    goto_order('LM1353', 'AGV-F2-70', complete=False)
    goto_order(['LM1347', 'AP1256'], 'AGV-F2-63')

def order_issue_pool_10627():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.ignore)
    time.sleep(2)
    set_dispatchable_status(['YJ-2F-Fork04', 'YJ-2F-Fork02'], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('YJ-2F-Fork04', 'LM4137')
    move_robot('YJ-2F-Fork02', 'LM4138')
    time.sleep(2)
    goto_order(['AP3481', 'AP3425'], 'YJ-2F-Fork04')
    goto_order('AP3486', 'YJ-2F-Fork02')

def order_issue_pool_10614():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('AMB-01', 'PP2')
    time.sleep(2)
    load_unload_order(['AP170', 'AP172'])
    time.sleep(2)
    load_unload_order(['AP172', 'AP170'])

def no_cargo_pass():
    set_position_by_edge('SWW4673006', 'AP2096', 'AP2091', 0.962)
    # time.sleep(2)
    # set_goods_shape('SWW4673006', -0.2, -0.2, 0.2, 0.2)

def order_notice():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.dispatchable)
    time.sleep(2)
    goto_order(['AP77', 'ironMan'])

def amb_mapf_recognize():
    terminate_all_order()
    time.sleep(2)
    set_dispatchable_status([], DispatchStatus.dispatchable)
    time.sleep(2)
    move_robot('sim_01', 'LM1')
    move_robot('sim_02', 'LM5')
    set_reach_deviation(['sim_02'], 0.7)
    time.sleep(2)
    goto_order('LM8', 'sim_02', recognize=True, complete=False)
    time.sleep(2)
    goto_order('LM6', 'sim_01')

def mapf_collision():
    terminate_all_order()
    time.sleep(2)
    move_robot('SCA-A09', 'LM340', 3.14)
    move_robot('SCA-A03', 'LM293', 3.14)
    time.sleep(2)
    goto_order('AP381', 'SCA-A03')
    time.sleep(2)
    goto_order('PP308', 'SCA-A09')

def mapf_deadlock_3():
    terminate_all_order()
    time.sleep(2)
    move_robot('AMB-5', 'LM151', math.radians(-177.04395869542438))
    move_robot('AMB-2', 'LM149', math.radians(-90.871106307748580))
    move_robot('AMB-3', 'LM145', math.radians(+179.56497299400000))
    time.sleep(2)
    goto_order('AP146', 'AMB-2')
    goto_order('AP138', 'AMB-5')
    goto_order('AP150', 'AMB-3')

def mapf_deadlock_4():
    terminate_all_order()
    time.sleep(2)
    move_robot('AMB-02', 'AP169', 3.14)
    move_robot('AMB-01', 'LM403', 1.57)
    time.sleep(2)
    goto_order('LM58', 'AMB-02')
    goto_order('AP171', 'AMB-01')

def mapf_deadlock_5():
    terminate_all_order()
    time.sleep(2)
    move_robot('F2-AGV-109', 'LM7927', 3.14)
    move_robot('F2-AGV-142', 'LM7926', 0)
    time.sleep(2)
    goto_order('LM8374', 'F2-AGV-109')
    goto_order('LM7796', 'F2-AGV-142')

def order_issue_pool_11229():
    ## 避让稳定不能舍近求远
    order_template('AMB-01', 'LM405', 'AP187', 'AMB-02', 'AP184', 'LM64')

def order_issue_pool_11247():
    ## 库位前置点资源加速释放
    order_template('AMB-01', 'LM508', 'AP526', 'AMB-02', 'LM670', 'AP534')

def order_issue_pool_11247_3_agvs():
    ## 3 车避让路线反复更换
    terminate_all_order()
    time.sleep(2)
    move_robot('AMB-06', 'LM662')
    move_robot('AMB-05', 'LM682')
    move_robot('AMB-04', 'LM35')
    time.sleep(2)
    goto_order('DC026', 'AMB-06')
    goto_order('BQ022', 'AMB-05')
    goto_order('BQ062', 'AMB-04')

def order_issue_pool_11147():
    ## oneStep 任务有碰撞时不能下发
    terminate_all_order()
    time.sleep(2)
    move_robot('AMB-06', 'LM25')
    move_robot('AMB-05', 'AP62')
    time.sleep(2)
    goto_order('AP63', 'AMB-06')
    time.sleep(5)
    goto_order('AP7', 'AMB-05')

def mapf_adjust_info_region_basic():
    # 最基本的凸多边形调整范围测试: 2 车不能通过 1 车调整范围的区域
    terminate_all_order()
    set_dispatchable_status(['sim_04', 'sim_05'], DispatchStatus.ignore)
    modify_param({'RDSDispatcher': {
        'DelayFinishTime': 20,
    }})
    time.sleep(2)
    move_robot('sim_01', 'LM3')
    move_robot('sim_02', 'LM2')
    move_robot('sim_03', 'LM8')
    time.sleep(2)
    data = {
        'id': get_random_str(),
        'vehicle': 'sim_01',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP17',
            'adjustInfo': [{
                'points': 'AP17',
                'region': [
                    { 'x': -3, 'y': +1 },
                    { 'x': +1, 'y': +1 },
                    { 'x': +1, 'y': -1 },
                    { 'x': -3, 'y': -1 }
                ]
            }]
        }]
    }
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps(data))
    time.sleep(2)
    goto_order('AP19', 'sim_02')
    goto_order('AP21', 'sim_03')

def mapf_adjust_info_region_self_position():
    # 最基本的凸多边形调整范围原地任务: 调整范围内存在机器人, 我不能执行原地调整任务
    # 分为两种: 1. 范围内的机器人是运动的(cur_func); 2. 范围内的机器人是静止的
    terminate_all_order()
    set_dispatchable_status(['sim_04', 'sim_05'], DispatchStatus.ignore)
    modify_param({'RDSDispatcher': {
        'DelayFinishTime': 0,
    }})
    move_robot('sim_01', 'AP17')
    move_robot('sim_02', 'LM2')
    move_robot('sim_03', 'LM8')
    time.sleep(2)
    goto_order('AP17', 'sim_01')
    time.sleep(5)
    goto_order('AP19', 'sim_02')
    time.sleep(5)
    data = {
        'id': get_random_str(),
        'vehicle': 'sim_01',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP17',
            'adjustInfo': [{
                'points': 'AP17',
                'region': [
                    { 'x': -3, 'y': +1 },
                    { 'x': +1, 'y': +1 },
                    { 'x': +1, 'y': -1 },
                    { 'x': -3, 'y': -1 }
                ]
            }]
        }]
    }
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps(data))

def mapf_adjust_info_region_self_position_2():
    # 最基本的凸多边形调整范围原地任务: 调整范围内存在机器人, 我不能执行原地调整任务
    # 分为两种: 1. 范围内的机器人是运动的; 2. 范围内的机器人是静止的(cur_func)
    terminate_all_order()
    set_dispatchable_status(['sim_04', 'sim_05'], DispatchStatus.ignore)
    modify_param({'RDSDispatcher': {
        'DelayFinishTime': 0,
    }})
    move_robot('sim_01', 'AP17')
    move_robot('sim_02', 'AP18')
    move_robot('sim_03', 'LM8')
    time.sleep(2)
    goto_order('AP17', 'sim_01')
    goto_order('AP18', 'sim_02')
    time.sleep(10)
    data = {
        'id': get_random_str(),
        'vehicle': 'sim_01',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP17',
            'adjustInfo': [{
                'points': 'AP17',
                'region': [
                    { 'x': -3, 'y': +1 },
                    { 'x': +1, 'y': +1 },
                    { 'x': +1, 'y': -3 },
                    { 'x': -3, 'y': -3 }
                ]
            }]
        }]
    }
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps(data))

def mapf_adjust_info_region_real():
    # 奥士康实际生产测试有问题
    terminate_all_order()
    modify_param({'RDSDispatcher': {
        'DelayFinishTime': 0,
    }})
    move_robot('F3-AGV-105', 'LM2107')
    move_robot('F3-AGV-129', 'LM2965')
    time.sleep(2)
    time.sleep(10)
    data = {
        'id': get_random_str(),
        'vehicle': 'F3-AGV-105',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'SMIAPL80B0018',
            'adjustInfo': [{
                'points': 'SMIAPL80B0018',
                'region': [
                    { 'x': -1, 'y': 1.5 },
                    { 'x': 0.5, 'y': 0.5 },
                    { 'x': 0.5, 'y': -0.5 },
                    { 'x': -1, 'y': -1.5 }
                ]
            }]
        }]
    }
    requests.post('http://' + config.ip + ':8088/setOrder', json.dumps(data))
    goto_order('AP3009', 'F3-AGV-129')

def order_issue_pool_11247_near_bin_deadlock():
    # forkChanel 引发死锁
    order_template('AMB-02', 'LM1007', 'LM995', 'AMB-01', 'LM993', 'LM1006')

def order_issue_pool_11438():
    move_robot('CDD14-2', 'LM61')
    time.sleep(2)
    goto_order('AP98', recognize=True)

def order_issue_pool_11147_pro():
    # 多车死锁
    terminate_all_order()
    move_robot('AMB-02', 'LM23', -1.57)
    move_robot('AMB-04', 'LM115', 0)
    move_robot('AMB-05', 'LM31', 0)
    move_robot('AMB-06', 'LM127', -1.57)
    move_robot('AMB-07', 'LM25', 1.57)
    time.sleep(2)
    goto_order('AP63', 'AMB-02')
    goto_order('AP16', 'AMB-04')
    goto_order('AP63', 'AMB-05')
    goto_order('AP12', 'AMB-06')
    goto_order('PP106', 'AMB-07')

def order_issue_pool_11540():
    # 释放前置点资源慢
    terminate_all_order()
    move_robot('SCA-A09', 'LM34', 1.57)
    move_robot('SCA-A06', 'LM438', 1.57)
    time.sleep(2)
    set_operation_time('SCA-A09', 'JackLoad', 10)
    time.sleep(2)
    goto_order('AP12', 'SCA-A09', operation='JackLoad', recognize=True)
    goto_order('AP11', 'SCA-A06')

def order_issue_pool_11455():
    # 检测不出和 waiting 状态的机器人路线冲突
    terminate_all_order()
    time.sleep(2)
    move_robot('SD-F3-02', 'LM12419', -1.57)
    move_robot('SD-F3-03', 'AP12115')
    move_robot('SD-F3-04', 'AP12009')
    time.sleep(2)
    goto_order('AP12030', 'SD-F3-03', complete=False)
    goto_order('AP12032', 'SD-F3-04', complete=False)
    time.sleep(20)
    goto_order('AP12028', 'SD-F3-02')

def order_issue_pool_6089():
    terminate_all_order()
    move_robot('OPK-121', 'LM5218')
    move_robot('OPK-124', 'LM5216')
    time.sleep(2)
    goto_order('LM6814', 'OPK-121')
    goto_order('LM6800', 'OPK-124')

def order_issue_pool_11363():
    terminate_all_order()
    time.sleep(2)
    move_robot('SCA-B02', 'LM386', 0)
    move_robot('SCA-B08', 'LM441', 3.14)
    time.sleep(2)
    goto_order('AP370', 'SCA-B08')
    goto_order('AP258', 'SCA-B02')

def ao_shi_kang_0305():
    terminate_all_order()
    time.sleep(2)
    move_robot('SD-F3-02', 'AP12031')
    move_robot('SD-F3-03', 'AP12117')
    time.sleep(2)
    goto_order('AP12032', 'SD-F3-03', complete=False)
    time.sleep(10)
    goto_order('AP12015', 'SD-F3-02')

def order_issue_pool_10355():
    # 大连佳林 多车小区域规划效果差
    terminate_all_order()
    time.sleep(2)
    move_robot('JLAMR-01', 'PP1003')
    move_robot('JLAMR-02', 'PP1002')
    move_robot('JLAMR-03', 'PP18002')
    move_robot('JLAMR-04', 'PP1018')
    move_robot('JLAMR-12', 'PP1022')
    move_robot('JLAMR-15', 'LM11201')
    time.sleep(2)
    unlock_vehicles = ['JLAMR-01', 'JLAMR-02', 'JLAMR-03', 'JLAMR-04', 'JLAMR-12', 'JLAMR-15']
    set_nickname(unlock_vehicles, "dingyubo")
    time.sleep(2)
    move_robot('JLAMR-05','AP117')
    move_robot('JLAMR-08','LM10626')
    move_robot('JLAMR-09','LM10661')
    move_robot('JLAMR-10','AP97')
    move_robot('JLAMR-11','LM10234')
    time.sleep(2)
    set_goods_shape('JLAMR-05', -0.54, -0.73, 0.54, 0.73)
    set_goods_shape('JLAMR-08', -0.61, -0.83, 0.61, 0.83)
    set_goods_shape('JLAMR-11', -0.60, -0.83, 0.60, 0.83)
    time.sleep(2)
    goto_order('AP122', 'JLAMR-05',)
    goto_order('AP116', 'JLAMR-08',)
    goto_order('AP60', 'JLAMR-09',)
    goto_order('AP157', 'JLAMR-10',)
    goto_order('AP140', 'JLAMR-11',)

def order_issue_pool_11678():
    # 两车从不同楼层去同一楼层不同目标点
    terminate_all_order()
    time.sleep(2)
    move_robot('SWW3B31027', 'LM4540')
    move_robot('SWW39J1021', 'LM1041')
    time.sleep(2)
    goto_order('AP1580', 'SWW3B31027')
    goto_order('AP271', 'SWW39J1021')

def order_issue_pool_11630():
    # api 调用导致调度崩溃, 无法复现
    block_names = [f'MutexRegion{i:03d}' for i in range(1, 20)]
    while True:
        for block in block_names:
            print(block, get_robots_in_block(block))
            time.sleep(0.2)
        time.sleep(0.2)

def order_issue_pool_11619():
    terminate_all_order()
    time.sleep(2)
    vehicles = ['CTU-2F-2', 'CTU-2F-3', 'CTU-2F-4']
    init_pos = ['AP21233',  'AP21237',  'LM115']
    init_ang = [0, 0, -1.57]
    targets  = ['Z-03-02-02', 'Z-03-02-01', 'Z-02-02-01']
    complete = [True, False, True]
    for v, p, a in zip(vehicles, init_pos, init_ang):
        move_robot(v, p, a)
    time.sleep(2)
    for v, t, c in zip(vehicles, targets, complete):
        goto_order(t, v, complete=c)

def set_bin_goods_shape():
    data = {
        'Loc-01': [-0.5, -0.2, 0.5, 0.2],
        'Loc-02': [-0.5, -0.25, 0.5, 0.2],
        'Loc-03': [-0.5, -0.2, 0.55, 0.2],
        'Loc-04': [-0.5, -0.2, 0.5, 0.25]
    }
    requests.post("http://" + config.ip + ":8088/updateSimRobotState", json.dumps(data))

def order_issue_pool_11951():
    terminate_all_order()
    time.sleep(2)
    move_robot('AGV-F2-78', 'AP22125')
    move_robot('AGV-F2-85', 'AP20870')
    time.sleep(2)
    goto_order('AP22013', 'AGV-F2-78')
    goto_order('AP21971', 'AGV-F2-85')

def simulation_fork_height():
    while True:
        print(get_fork_height('sim_01'))
        time.sleep(0.1)

def bin_occupy():
    db_path = r'C:\.SeerRobotics\rdscore\resources\db\bin-monitor.sqlite'
    add = ("INSERT INTO binmonitor (binname, binstatus, holder, update_time, connection_status, binarea, "
                "goodsid, content) VALUES ('Loc-03', 1, 1, '', 1, '', '', '')")
    execute_sqlite3_db(db_path, add)
    delete = "DELETE FROM binmonitor WHERE binname = 'Loc-01'"
    execute_sqlite3_db(db_path, delete)

def order_issue_pool_12121():
    terminate_all_order()
    time.sleep(2)
    order_template('QY-01', 'LM530', 'LM8', 'QY-02', 'LM179', 'PP523')

def well_wit_583():
    terminate_all_order()
    time.sleep(2)
    move_robot('AMR-HL-06', 'LM6007')
    time.sleep(2)
    goto_order('LM6018')
    time.sleep(7)
    terminate_order(['AMR-HL-06'])
    goto_order('LM6018')

def order_issue_pool_12157():
    terminate_all_order()
    time.sleep(2)
    move_robot('sim_01', 'LM131')
    time.sleep(2)
    set_goods_shape('sim_01', -0.2, -0.2, 0.2, 0.2)
    time.sleep(2)
    goto_order('LM119', operation='JackUnload')
    time.sleep(2)
    goto_order('AP130')

def order_issue_pool_12370():
    terminate_all_order()
    time.sleep(2)
    move_robot('316001', 'LM1890', 1.57)
    move_robot('316002', 'LM1133', 0)
    time.sleep(2)
    set_goods_shape('316001', -0.2, -0.2, 0.2, 0.2)
    time.sleep(2)
    goto_order('PP1924', '316001')
    time.sleep(2)
    goto_order('AP543', '316002')

def order_issue_pool_12393():
    terminate_all_order()
    time.sleep(2)
    move_robot('AGF-B', 'LM1011', 0)
    oid = get_random_str()
    goto_order('20101', 'AGF-B', order_id=oid, complete=False)
    time.sleep(20)
    add_block('20102', oid, True)

def order_issue_pool_12441():
    terminate_all_order()
    time.sleep(2)
    order_template('Number1', 'LM452', 'LM422', 'Number3', 'LM7', 'LM449')

def tianjin():
    terminate_all_order()
    time.sleep(2)
    move_robot('316001', 'LM257')
    move_robot('316002', 'LM1447')
    time.sleep(2)
    set_goods_shape('316001', -0.335, -0.7, 0.335, 0.7, 1.57)
    set_goods_shape('316002', -0.335, -0.7, 0.335, 0.7, 1.57)
    set_goods_shape('316001', -0.335, -0.7, 0.335, 0.7, 1.57, autoLoad=True)
    set_goods_shape('316002', -0.335, -0.7, 0.335, 0.7, 1.57, autoLoad=True)
    time.sleep(2)
    goto_order('AP542', '316001', operation='JackUnload')
    goto_order('AP543', '316002', operation='JackUnload')
    time.sleep(2)
    goto_order('AP548', '316001', operation='JackLoad')
    goto_order('AP549', '316002', operation='JackLoad')

def custom_mapf_test():
    agvs = set_target_list(1, 10, title='SCA-A', fill=True)
    move_robot(agvs[0], 'LM158')
    move_robot(agvs[1], 'LM159')
    move_robot(agvs[2], 'LM160')
    move_robot(agvs[3], 'LM161')
    move_robot(agvs[4], 'LM570')
    move_robot(agvs[5], 'AP254')
    move_robot(agvs[6], 'LM529')
    move_robot(agvs[7], 'LM205')
    move_robot(agvs[8], 'AP258')
    move_robot(agvs[9], 'LM527')
    time.sleep(2)
    data = [
        { 'r_name': agvs[0], 'target': 255, 'type': 0 },  # 158->255
        { 'r_name': agvs[4], 'target': 238, 'type': 1 },  # 570->238
        { 'r_name': agvs[5], 'target': 238, 'type': 1 },  # 254->238
        { 'r_name': agvs[6], 'target': 238, 'type': 1 },  # 529->238
        { 'r_name': agvs[7], 'target': 238, 'type': 1 },  # 205->238
        { 'r_name': agvs[8], 'target': 238, 'type': 1 },  # 258->238
        # { 'r_name': agvs[9], 'target': 238, 'type': 1 },  # 527->238
    ]
    print(json.dumps(get_custom_mapf_result(data), indent=2))

def order_issue_pool_12378():
    terminate_all_order()
    time.sleep(2)
    move_robot('AGV02', 'LM607')
    move_robot('AGV14', 'LM719')
    time.sleep(2)
    goto_order('AP600', 'AGV02')
    goto_order('LM229', 'AGV14')

def join_order():
    data1 = {
        'id': 'seer-test-001',
        'complete': True,
        'group': 'RobotGroup-1.2T',
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'WH003',
                'binTask': 'Load'
            },
            {
                'blockId': get_random_str(),
                'location': 'PL_FG_DMF19_001',
                'binTask': 'Unload'
            }
        ]
    }
    data2 = {
        'id': 'seer-test-002',
        'complete': False,
        'group': 'RobotGroup-1.2T',
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'PL_FG_DMF19_002',
                'binTask': 'Load'
            },
            {
                'blockId': get_random_str(),
                'location': 'LM336',
                'operation': 'wait'
            }
        ]
    }
    data3 = {
        'id': 'seer-test-003',
        'complete': False,
        'group': 'RobotGroup-1.2T',
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'PL_PKG_DMF19_001',
                'binTask': 'Load'
            },
            {
                'blockId': get_random_str(),
                'location': 'LM336',
                'operation': 'wait'
            }
        ]
    }
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data1))
    time.sleep(5)
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data2))
    time.sleep(5)
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data3))

def join_order_2():
    data1 = {
        'id': 'seer-test-03',
        'complete': True,
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'PL_FG_DMF19_001',
                'binTask': 'Load'
            },
            {
                'blockId': get_random_str(),
                'location': 'WH001',
                'binTask': 'Unload'
            }
        ]
    }
    data2 = {
        'id': 'seer-test-04',
        'complete': True,
        'group': 'RobotGroup-1.2T',
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'WH002',
                'binTask': 'Load'
            },
            {
                'blockId': get_random_str(),
                'location': 'PL_FG_DMF19_002',
                'binTask': 'Unload'
            }
        ]
    }
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data1))
    time.sleep(5)
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data2))

def mapf_search_conflict():
    terminate_all_order()
    time.sleep(2)
    move_robot('316001', 'LM943')
    move_robot('316002', 'LM1749')
    time.sleep(2)
    set_goods_shape('316001', -0.5, -0.5, 0.5, 0.5)
    time.sleep(2)
    goto_order('AP488', '316001')
    goto_order('AP304', '316002')

def order_issue_pool_12820():
    terminate_all_order()
    time.sleep(2)
    move_robot('YJ-2F-Fork01', 'LM1600')
    move_robot('YJ-2F-Fork02', 'LM2031')
    move_robot('YJ-2F-Fork03', 'LM4130')
    move_robot('YJ-2F-Fork04', 'LM3743')
    time.sleep(2)
    goto_order('AP606', 'YJ-2F-Fork02')
    goto_order('LM1600', 'YJ-2F-Fork03')
    goto_order('LM1600', 'YJ-2F-Fork04')
    time.sleep(2)
    goto_order('AP605', 'YJ-2F-Fork01')

def cate():
    terminate_all_order()
    time.sleep(2)
    order_template('Fork-10', 'LM2674', 'AP2189', 'Fork-03', 'LM2501', 'AP2188')

def tianjin_schedule():
    move_robot('sim_01', 'LM131')
    time.sleep(2)
    set_goods_shape('sim_01', -0.2, -0.2, 0.2, 0.2)
    time.sleep(2)
    data1 = {
        'id': 'seer-dyb-01',
        'complete': True,
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'Loc-8-1',
                'binTask': 'QuickUnload'
            }
        ]
    }
    data2 = {
        'id': 'seer-dyb-02',
        'complete': True,
        'blocks': [
            {
                'blockId': get_random_str(),
                'location': 'Loc-7-1',
                'binTask': 'QuickLoad'
            }
        ]
    }
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data1))
    time.sleep(5)
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data2))

def ioi():
    data1 = {
        'id': '11111',
        'complete': False,
        'keyRoute': 'AP130'
    }
    requests.post("http://" + config.ip + ":8088/setOrder", json.dumps(data1))
    data2 = {
        'id': '11111',
        'complete': True,
        'blocks': [{
            'blockId': get_random_str(),
            'location': 'AP130',
            'operation': 'JackLoad'
        }]
    }
    time.sleep(10)
    requests.post("http://" + config.ip + ":8088/addBlocks", json.dumps(data2))

def adam_detour():
    move_robot('RIL-H-9015', 'AP10050', 1.57)
    move_robot('RIL-H-9019', 'AP10051', 1.57)
    time.sleep(2)


if __name__ == '__main__':
    """
    README
    1. 严格限制测试函数编写规范, 方便后续的整理迁移
    2. 函数名用对应 coding 命名, 如 robokit_100, order_issue_pool_100, 这样方便以后回溯问题下载日志等
    3. 如果没有对应 coding, 需要在函数中注释测试使用的场景
    4. 函数注释要写明测试点, 为追求简洁, 大部分测试函数不写断言, 只依赖人观察合理性, 所以需写明观察点, 必要时需要画出简易拓扑图
    5. 尽可能采用封装好的函数模板, 避免写过长的逻辑; 如最简单的两台车初始化位置并发单就采用函数 order_template
    """
    adam_detour()