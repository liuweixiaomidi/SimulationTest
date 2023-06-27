import random
import time

import Lib.function as core


# Label: inside 8 agvs
# Label: outside 12 agvs


def assign_value(probability, value):
    # 根据概率获取目标点
    value = random.choices(value, probability)[0]
    return value


def old_strategy():
    inside_points = core.set_target_list(42, 68, title='LM', remove=['LM51', 'LM55', 'LM61'])
    outside_points = core.set_target_list(1, 40, title='LM', remove=['LM11', 'LM18', 'LM31', 'LM38'])
    _probability = [0.8, 0.1, 0.1]
    _value = ['null', 'in->out', 'out->in']
    count = 0
    while count < 100:
        choice = assign_value(_probability, _value)
        match choice:
            case 'null':
                core.goto_order(random.choice(inside_points), label='inside')
                core.goto_order(random.choice(outside_points), label='outside')
            case 'in->out':
                core.goto_order(random.choice(outside_points), label='inside')
            case 'out->in':
                core.goto_order(random.choice(inside_points), label='outside')
            case _:
                print('sth goes wrong!!!')
        if not count % 20:
            time.sleep(30)
        count += 1


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
            cur_sta = core.get_current_location(robot)
            target = random.choice([in_points for in_points in inside_points if in_points != cur_sta]) if robot in \
                inside_robots else random.choice([ou_points for ou_points in outside_points if ou_points != cur_sta])
            # target = random.choice(inside_points) if robot in inside_robots else random.choice(outside_points)
            core.goto_order(target, robot)
            count += 1
        if count == 100:
            break
        time.sleep(2)


if __name__ == '__main__':
    new_strategy()
