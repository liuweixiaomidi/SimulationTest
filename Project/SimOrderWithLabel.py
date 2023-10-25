from Lib.function import *

# path of csv
path = os.path.abspath(__file__)
path = os.path.dirname(path)
csv_path = os.path.join(path, 'simOrder.csv')

csv_file = pd.read_csv(csv_path)
num_rows, num_columns = csv_file.shape


def run():
    if num_columns % 4:
        raise ValueError(num_columns, "数据缺失, 表格的列数量不满足要求")
    pickups = list()
    unloads = list()
    rhythms = list()
    labels_ = list()
    pickups_check = set()
    unloads_check = set()
    rhythms_check = set()
    labels_check_ = set()
    # 解析 csv 数据
    for column_name in csv_file.columns:
        column_data = csv_file[column_name].dropna()
        print(type(column_data))
        temp_list = list()
        for data in column_data:
            temp_list.append(data)
        column_index = csv_file.columns.get_loc(column_name) + 1
        match column_index % 4:
            case 1:
                pickups_check.add(column_name[0:7])
                check_duplicated(column_data, column_name)
                pickups.append(temp_list)
            case 2:
                unloads_check.add(column_name[0:7])
                check_duplicated(column_data, column_name)
                unloads.append(temp_list)
            case 3:
                rhythms_check.add(column_name[0:7])
                if column_data.nunique() != 1:
                    raise ValueError(column_name, "同一个流程的节拍不一致")
                filter_rhythm = csv_file.dropna(subset=column_name)
                rhythms.append(filter_rhythm[column_name].mean())
            case 0:
                labels_check_.add(column_name[0:5])
                if column_data.nunique() != 1:
                    raise ValueError(column_name, "同一个流程的节拍不一致")
                filter_label = csv_file.dropna(subset=column_name)
                labels_.append(get_column_element(filter_label[column_name]))
            case _:
                raise ValueError("数学不存在了")
    check_column_name(pickups_check)
    check_column_name(unloads_check)
    check_column_name(rhythms_check)
    check_column_name(labels_check_)
    # 发单
    rhythms = [x * 8 for x in rhythms]
    print("Calculate:  " + "column: " + str(num_columns // 4) + ";  pickups: " + str(len(pickups)) + ";  unloads: " +
          str(len(unloads)) + ";  rhythms: " + str(len(rhythms)) + ";  labels: " + str(len(labels_)))
    time_control = list()
    for i in range(0, num_columns // 4):
        load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])], label=labels_[i], out='simple')
        time_control.append(time.time())
    time_cost = time.time()
    while time.time() - time_cost < 3600 * 4:
        for i in range(0, num_columns // 4):
            if time.time() - time_control[i] > rhythms[i]:
                load_unload_order([random.choice(pickups[i]), random.choice(unloads[i])],
                                  label=labels_[i], out='simple')
                time_control[i] = time.time()


if __name__ == '__main__':
    run()
