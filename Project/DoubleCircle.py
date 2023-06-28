import random
import time

import Lib.function as core


# Label: inside 8 agvs
# Label: outside 12 agvs


def assign_value(probability, value):
    # 根据概率获取目标点
    value = random.choices(value, probability)[0]
    return value


def get_finished_robots(robots) -> list:
    result = []
    for robot in robots:
        robot_status = core.get_robot_state(robot)
        if robot_status == 'FINISHED' or robot_status == 'STOPPED' or robot_status is None:
            result.append(robot)
    return result


def new_strategy():
    inside_points = core.set_target_list(42, 68, title='LM', remove=['LM51', 'LM55', 'LM61'])
    outside_points = core.set_target_list(1, 40, title='LM', remove=['LM11', 'LM18', 'LM31', 'LM38'])
    # 查询所有机器人状态 记录已经完成任务的机器人
    inside_robots = core.set_target_list(1, 8, title='sim_0')
    outside_robots = core.set_target_list(9, 20, fill=True, title='sim_')
    m_robot = core.set_target_list(1, 20, fill=True, title='sim_')
    count = 0
    while True:
        finished_robots = get_finished_robots(m_robot)
        for robot in finished_robots:
            _probability = [0.8, 0.2]
            _value = ['null', 'in<->out']
            choice = assign_value(_probability, _value)
            cur_sta = core.get_current_location(robot)
            options = {
                'null': (inside_points if robot in inside_robots else outside_points),
                'in<->out': (inside_points if robot in outside_points else outside_points)
            }
            available_points = options.get(choice)
            target = random.choice([p for p in available_points if p != cur_sta])
            core.goto_order(target, robot)
            count += 1
        if count == 100:
            break
        time.sleep(2)


if __name__ == '__main__':
    new_strategy()
