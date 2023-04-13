import random
import time

import Lib.function as core    # core的常用API封装在这个库里 里面的所有函数都有详细注释

"""
ip 设置：可以在Lib.config文件中设置服务器ip, Lib.function中的函数默认采用设置的ip
业务逻辑：左侧库位取货去最右侧库位放货
代码逻辑：
    1. 设置一个取货点集合和一个放货点集合
    2. 发送含有 取货 和 放货 两个动作块的订单
    3. 设计一个发单终止条件
    4. 如果不是测试很精细的逻辑终止条件不用太严格：比如发满 n 单就不发了，比如每个取货点只能取货一次 所有取货点都取过了就不发了
    5. 本程序选用后者终止条件
    6. 设置发单间隔（最简单的是每隔 n 秒发一单）
运行方式：需要有 python 环境, 运行 setup.py 文件, 终端命令行为 python setup.py
"""


def zhong_wai_yun():
    load_target = core.set_target_list(1, 2)
    # 将 AP1 AP2 放入取货点集合内  1 2这两个参数是连续库位的起点终点 如果传参是 1 4 那么就是把 AP1 AP2 AP3 AP4 放入取货集合 详见函数注释
    load_target += core.set_target_list(87, 88)
    load_target += core.set_target_list(92, 93)
    load_target += core.set_target_list(81, 82, ["AP17", "AP85"])   # 将 AP81 AP82 AP17 AP85 放入取货集合内
    unload_target = core.set_target_list(20, 24, "AP58")    # 设置六个放货点集合
    while len(load_target):   # 持续发单直到取货点集合为空
        cur_load = random.choice(load_target)   # 从取货集合中随机选取一个取货点
        core.goto_order([cur_load, random.choice(unload_target)])   # 发送含有两个动作块的订单，第一个动作块是上面选取的取货点
        # 第二个动作块为放货集合中随机选取的点 订单不指定接单机器人由调度进行分配 封口 详见函数注释
        load_target.remove(cur_load)   # 用过的取货点从集合中删除 实现每个站点只取货一次
        time.sleep(2)   # 2s 发一单
