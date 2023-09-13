import os
import random

import pandas as pd

from Lib.function import *

# path of csv
path = os.path.abspath(__file__)
path = os.path.dirname(path)
csv_path = os.path.join(path, 'project.csv')

csv_file = pd.read_csv(csv_path)
num_rows, num_columns = csv_file.shape


def check_duplicated(column_data, column_name):
    a = column_data[column_data.duplicated(keep=False)]
    if not a.empty:
        print(a)
        raise ValueError(column_name, "点位名称重复")


def run():
    if num_columns % 3:
        raise ValueError(num_columns, "数据缺失, 表格的列数量不满足要求")
    pickups = list()
    unloads = list()
    rhythms = list()
    # 解析 csv 数据 (含格式检查)
    for column_name in csv_file.columns:
        column_data = csv_file[column_name]
        temp_list = list()
        for data in column_data:
            temp_list.append(data)
        column_index = csv_file.columns.get_loc(column_name) + 1
        match column_index % 3:
            case 1:
                check_duplicated(column_data, column_name)
                pickups.append(temp_list)
            case 2:
                check_duplicated(column_data, column_name)
                unloads.append(temp_list)
            case 0:
                if column_data.nunique() != 1:
                    raise ValueError(column_name, "同一个流程的节拍不一致")
                rhythms.append(temp_list)
            case _:
                raise ValueError("数学不存在了")
    # 发单
    print("Calculate:  " + "column: " + str(num_columns // 3) + ";  pickups: " + str(len(pickups)) + ";  unloads: " +
          str(len(unloads)) + ";  rhythms: " + str(len(rhythms)) + ";")
    time_control = list()
    for i in range(0, num_columns // 3):
        load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])], cout='simple')
        time_control.append(time.time())
    time_cost = time.time()
    while time.time() - time_cost < 600:
        for i in range(0, num_columns // 3):
            if time.time() - time_control[i] > rhythms[i][0]:
                load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])], cout='simple')
                time_control[i] = time.time()


if __name__ == '__main__':
    run()
