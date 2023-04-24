import random
import time

import Lib.function as core


def space():
    print()


def check_err(value: any, scope: list):
    """
    设置报错信息
    :param value: 输入值
    :param scope: 范围
    :return: None
    """
    if value not in scope:
        print('ERROR: 输入的数据不在提供的选择范围内！！！')
        return True
    return False


global terminate_condition


def conversation():
    """
    运行后的对话信息
    用于进行策略选择
    :return: None
    """
    global terminate_condition
    space()
    print('仿真测试发单设置: ')
    space()
    print('策略: 发单策略的设置, 根据提示进行选择')
    order_type = int(input('   - 订单类型(取放货订单: 1; 分拨单: 2; 混合类型: 3): '))
    if check_err(order_type, [1, 2, 3]):
        return
    match order_type:
        case 1:
            print('在取放货模式中, 每个订单由配置了 Load 动作的取货和 Unload 动作的放货两个动作块组成', '\n\n下面开始构建取货库区')
            load_single = None
            load_start = int(input('   - 请输入连续库位的起始值(如果取货点为 AP1 AP2 AP3, 则起始值应为 1): '))
            load_end = int(input('   - 请输入连续库位的终止值(如果取货点为 AP1 AP2 AP3, 则起始值应为 3): '))
            if load_end < load_start:
                print('ERROR: 终止值应大于起始值！！！')
                return
            load_fill = bool(int(input('   - 是否需要对上述连续库位中小于 10 的名称自动补零, 如 Loc-1 Loc-01(需要: 1; 不需要: 0): ')))
            load_title = str(input('   - 请输入库位的前缀名称(如果取货点为 AP1 AP2 AP3, 则前缀应为 AP): '))
            load_single_need = bool(int(input('   - 是否需要输入不在上述连续库位里的库位名称(需要: 1; 不需要: 0): ')))
            if load_single_need not in [0, 1]:
                print('ERROR: 输入的数据不在提供的选择范围内！！！')
            if load_single_need:
                load_single = \
                    list(map(str, input('   - 请输入独立的库位名称(如果取货点为 AP1 AP2 AP3 AP21 AP11, 则独立库位为 AP21 AP11): ').split()))
            space()
            print('下面开始构建放货库区')
            unload_single = None
            unload_start = int(input('   - 请输入连续库位的起始值(如果放货点为 AP1 AP2 AP3, 则起始值应为 1): '))
            unload_end = int(input('   - 请输入连续库位的终止值(如果放货点为 AP1 AP2 AP3, 则起始值应为 3): '))
            if unload_end < unload_start:
                print('ERROR: 终止值应大于起始值！！！')
                return
            unload_fill = bool(int(input('   - 是否需要对上述连续库位中小于 10 的名称自动补零, 如 Loc-1 Loc-01(需要: 1; 不需要: 0): ')))
            unload_title = str(input('   - 请输入库位的前缀名称(如果放货点为 AP1 AP2 AP3, 则前缀应为 AP): '))
            unload_single_need = bool(int(input('   - 是否需要输入不在上述连续库位里的库位名称(需要: 1; 不需要: 0): ')))
            if unload_single_need not in [0, 1]:
                print('ERROR: 输入的数据不在提供的选择范围内！！！')
            if unload_single_need:
                unload_single = \
                    list(map(str, input('   - 请输入独立的库位名称(如果放货点为 AP1 AP2 AP3 AP21 AP11, 则独立库位为 AP21 AP11): ').split()))
            space()
            load_bin = core.set_target_list(load_start, load_end, load_single, load_title, load_fill)
            unload_bin = core.set_target_list(unload_start, unload_end, unload_single, unload_title, unload_fill)
            robot_group = input('输入执行订单的机器组名称, 如果无须指定机器人组, 请输入0: ')
            if robot_group == '0':
                robot_group = None
            robot_label = input('输入执行订单的机器人标签名称, 如果无须指定标签, 请输入0: ')
            if robot_label == '0':
                robot_label = None
            sleep_time = int(input('输入相邻两订单间的发单间隔s: '))
            space()
            terminate_type = int(input('终止条件选择:\n   1: 取货点用光后终止发单\n   2: 放货点用光后终止发单\n   3: 发送订单一定数量后终止发单\n   请选择: '))
            index = 0
            match terminate_type:
                case 1:
                    terminate_condition = len(load_bin)
                case 2:
                    terminate_condition = len(unload_bin)
                case 3:
                    num = input('   发送多少订单后停止发单: ')
                    terminate_condition = index != num
                case _:
                    print('ERROR: 输入的数据不在提供的选择范围内！！！')
            while terminate_condition:
                index += 1
                cur_load = random.choice(load_bin)
                cur_unload = random.choice(unload_bin)
                core.load_unload_order([cur_load, cur_unload], group=robot_group, label=robot_label)
                load_bin.remove(cur_load)
                unload_bin.remove(cur_unload)
                time.sleep(sleep_time)
        case 2:
            print('暂不支持')
        case 3:
            print('暂不支持')
        case _:
            print('ERROR: 输入的数据不在提供的选择范围内！！！')


if __name__ == '__main__':
    conversation()
