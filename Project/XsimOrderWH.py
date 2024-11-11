from Lib.function import *
from Lib.modifyScene import *

def set_single_bin(name: str, w_name: str, state: int=0):
    data = {
        'name': name,
        'state': state,
        'workstation_name': w_name
    }
    return data

def set_single_workstation(name: str, _type: int, _label: str, dock: float, machine: str, bins: list):
    data = {
        'name': name,
        'type': _type,
        'label': _label,
        'dock_time': dock,
        'machine_name': machine,
        'bins': bins
    }
    return data

def set_single_machine(name: str, capacity: int, process: float, upper: str = None, lower: str = None,
                       pickups: list[dict] = None, unloads: list[dict] = None):
    data = {
        'name': name,
        'max_capacity': capacity,
        'process_time': process
    }
    if upper is not None:
        data['upper_machine'] = upper
    if lower is not None:
        data['lower_machine'] = lower
    if pickups is not None:
        data['pickup_workstations'] = pickups
    if unloads is not None:
        data['unload_workstations'] = unloads
    return data

def generate_json_data():
    path = r"C:\Users\seer\AppData\Local\RoboshopPro\appInfo\robots\All\b8feeb7e-63d9cdfe-99852c77-56a5ceef\DispatchEditor\scene\rds.scene"
    scene = CoreScene(path)
    area_1 = scene.get_range_point((-79, -59), (-61, -58))
    # print(len(area_1), area_1)
    area_2 = scene.get_range_point((-79, -56), (-55, -35))
    # print(len(area_2), area_2)
    area_3 = scene.get_range_point((-54, -37), (-52, -38))
    # print(len(area_3), area_3)
    area_4 = scene.get_range_point((-33, -4), (-66, -32))
    # print(len(area_4), area_4)
    area_5 = scene.get_range_point((20, 30), (-64, -40))
    # print(len(area_5), area_5)
    # ----------------------------------------------------------------------- #
    # area_1  ----->  area_2  ----->  area_3  ----->  area_4  -----> area_5   #
    #   取             放/取            放/取            放/取           放
    # ----------------------------------------------------------------------- #
    data = [
        set_single_machine('m1', 13, 0.1 * 3 * 60, lower='m2',
                           pickups=[set_single_workstation('w1', 0, 'L1', 10, 'm1',
                                                           [set_single_bin(i, 'w1') for i in area_1])]), # m1 原料库 --> area_1
        set_single_machine('m2', 1000, 0.1 * 15 * 60, upper='m1', lower='m3',
                           pickups=[set_single_workstation('w2', 1, 'L1', 10, 'm2',
                                                           [set_single_bin(i, 'w2') for i in area_2])],
                           unloads=[set_single_workstation('w3', 0, 'L1', 10, 'm2',
                                                           [set_single_bin(i, 'w3') for i in area_2])]), # m2 取放货相同的机器 --> area_2
        set_single_machine('m3', 1000, 0.1 * 15 * 60, upper='m2', lower='m4',
                           pickups=[set_single_workstation('w4', 1, 'L1', 10, 'm3',
                                                           [set_single_bin(i, 'w4') for i in area_3])],
                           unloads=[set_single_workstation('w5', 0, 'L1', 10, 'm3',
                                                           [set_single_bin(i, 'w5') for i in area_3])]), # m3 取放货相同的机器 --> area_3
        set_single_machine('m4', 1000, 0.1 * 20 * 60, upper='m3', lower='m5',
                           pickups=[set_single_workstation('w6', 1, 'L1', 10, 'm4',
                                                           [set_single_bin(i, 'w2') for i in area_4])],
                           unloads=[set_single_workstation('w7', 0, 'L1', 10, 'm4',
                                                           [set_single_bin(i, 'w2') for i in area_4])]), # m4 取放货相同的机器 --> area_4
        set_single_machine('m5', 1000, 180, upper='m4',
                           unloads=[set_single_workstation('w8', 1, 'L1', 10, 'm5',
                                                           [set_single_bin(i, 'w8') for i in area_5])]), # m5 成品库 --> area_5
    ]
    print(data)
    requests.post('http://127.0.0.1:8088/updateXSimOrder', json=data)

def generate_test_json():
    # ---------------------------------------------- #
    # --| 1 |-----| 4 -- 7 |-----| 10 |-----| 13 |-- #
    # --| 2 |-----| 5 -- 8 |-----| 11 |-----| 14 |-- #
    # --| 3 |-----| 6 -- 9 |-----| 12 |-----| 15 |-- #
    # ---------------------------------------------- #
    bin_1 = set_target_list(1, 2)
    bin_2 = set_target_list(4, 6)
    bin_3 = set_target_list(7, 9)
    bin_4 = set_target_list(10, 12)
    bin_5 = set_target_list(13, 15)
    data = [
        set_single_machine('raw_material', 5, 30, lower='process',
                           pickups=[set_single_workstation('w1', 0, 'L1', 5, 'raw_material',
                                                           [set_single_bin(i, 'w1') for i in bin_1])]),
        set_single_machine('process', 4, 20, upper='raw_material', lower='temp',
                           unloads=[set_single_workstation('w2', 1, 'L1', 5, 'process',
                                                           [set_single_bin(i, 'w2') for i in bin_2])],
                           pickups=[set_single_workstation('w3', 0, 'L2', 5, 'process',
                                                           [set_single_bin(i, 'w3') for i in bin_3])]),
        set_single_machine('temp', 3, 10, upper='process', lower='finished_product',
                           pickups=[set_single_workstation('w4', 0, 'L2', 5, 'temp',
                                                           [set_single_bin(i, 'w4') for i in bin_4])],
                           unloads=[set_single_workstation('w5', 1, 'L3', 5, 'temp',
                                                           [set_single_bin(i, 'w5') for i in bin_4])]),
        set_single_machine('finished_product', 2, 5, upper='temp',
                           unloads=[set_single_workstation('w6', 1, 'L3', 5, 'finished_product',
                                                           [set_single_bin(i, 'w6') for i in bin_5])])
    ]
    print(data)
    requests.post('http://127.0.0.1:8088/updateXSimOrder', json=data)

if __name__ == '__main__':
    generate_test_json()