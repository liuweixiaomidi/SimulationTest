import math
import time

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


if __name__ == '__main__':
    spain_near_5_bins()
