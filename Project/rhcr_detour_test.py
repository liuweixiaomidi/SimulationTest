import os
import re
import glob

from Lib.function import goto_order

log_path = r'D:\download\rhcr_disable_detour_test'
key_word = 'runOrder.runRHCR'

def mapf_time_cost():
    result = list()
    search_pattern = os.path.join(log_path, f"*.log")  # 在.log文件中查找
    log_files = glob.glob(search_pattern)
    if not log_files:
        print(f"No log files found in {log_path}")
        return result
    for single_log in log_files:
        if not os.path.exists(single_log):
            print(f"No such file: {single_log}")
            continue
        # 找到所有包含 key_word 的行
        keyword_lines = [m_line.strip() for m_line in open(single_log, 'r').readlines() if key_word in m_line]
        if not keyword_lines:
            print(f"No {key_word} keywords found in {single_log}")
            continue
        print(f"Lines containing {len(keyword_lines)} in {single_log}")
        for line in keyword_lines:
            mapf_time = re.search(rf"{re.escape(key_word)}\|(\d+)\|", line).group(1)
            result.append(int(mapf_time))
    print(result)
    print(f"In {log_path} RHCR run {len(result)} cost {sum(result)}ms")
    return result

def run_order():
    # 两条通道, 只发一个订单, 每次追击一个去随机库位的订单, 永远不封口
    # 机器人处于 waiting 状态 60s 后追加新动作块
    # 详细步骤:
    # 1. 左右两个区域各 5 台车执行任务
    # 2. 每个机器人下发一个订单, 不封口, 初始目标点分别为库位 1、3、5、7、9、11
    # 3. 监控订单状态, 在订单处于 waiting 状态 60s 后, 追加下一个动作块; 或者直接使用 delayFinishTime
    # 4. 按列表顺序追加动作块, 这样做可以保证任意时刻至少有一台车是存在绕的选择的
    # 5. 执行完 6 个动作块后, 订单封口
    left_aps = ['AP10065', 'AP10060', 'AP10055', 'AP10050', 'AP10044', 'AP10049']
    right_ap = ['AP10097', 'AP10110', 'AP10090', 'AP10100', 'AP10111', 'AP10113']
    left_agvs = ['RIL-H-9015', 'RIL-H-9019', 'RIL-H-9021', 'RIL-H-9023', 'RIL-H-9024']
    right_agv = ['RIL-L-8282', 'RIL-L-8283', 'RIL-L-8284', 'RIL-L-8285', 'RIL-L-8286']
    assert len(left_aps) == len(left_agvs)
    [goto_order(left_aps[i:]+left_aps[:i], left_agvs[i]) for i in range(len(left_aps))]
    assert len(right_ap) == len(right_agv)
    [goto_order(right_ap[i:]+right_ap[:i], right_agv[i]) for i in range(len(right_ap))]

if __name__ == '__main__':
    run_order()
    # mapf_time_cost()