import csv
import json
import os

# from Lib.function import *

# 使用相对路径测试
# scene_path = os.path.abspath(__file__)
# scene_path = os.path.dirname(scene_path)
# scene_path = os.path.join(scene_path, 'rds.scene')

# 绝对路径
scene_path = (r"C:\Users\seer\AppData\Local\RoboshopPro\appInfo\robots\All\a5dcf4de-a82c5013-27affde2-179bb03f"
              r"\DispatchEditor\scene\rds.scene")

agv2pos = {}

with open(scene_path, "r+", encoding="utf-8") as scene_file:
    scene = json.load(scene_file)
# print(json.dumps(scene,indent=4))

data = {
    "sim_01": "LM1",
    "sim_02": "LM2",
    "sim_03": "LM3",
    "sim_04": "LM4",
    "sim_05": "LM5",
}


def update_init_pos(scene, data):
    """写入初始化位置"""
    robotgroup = scene["robotGroup"]
    for group in robotgroup:
        for robot in group["robot"]:
            if data.get(robot["id"]) is not None:
                for ele in robot["property"]:
                    if ele["key"] == "initialPosition":
                        ele["stringValue"] = data[robot["id"]]
    # print(json.dumps(scene["robotGroup"],indent=4))


# 查找绑定的点
scene_area = scene['areas']
for area in scene_area:
    if area['name'] == 'new':
        points = area['logicalMap']['advancedPoints']
        num = 0
        for point in points:
            if point['className'] == 'ParkPoint':
                pp = point['instanceName']
                properties = point['property']
                for _property in properties:
                    if _property['key'] == 'parkPoint' and len(_property['tag']):
                        num += 1
                        agv2pos[_property['tag'][:-2]] = pp
                        # print(pp, _property['tag'][:-2])
        print(num)
print(agv2pos)

scene_path = os.path.abspath(__file__)
csv_path = os.path.dirname(scene_path)
csv_path = os.path.join(csv_path, 'agv2pp.csv')

# 写表格
with open(csv_path, "w", newline='') as csv_file:
    csv_file.truncate(0)
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['agv', 'pp'])
    for key, value in agv2pos.items():
        csv_writer.writerow([key, value])

# 修改地图数据绑定停靠点
# 绑定停靠点输入数据为字典格式   point:robot
"""原始数据可能是 robot:point 格式, 需要反转字典 
data = {v: k for k, v in data.items()}
"""


def init_pp_data(robot):
    """初始化填入停靠数据"""
    return {
        "key": "parkPoint",
        "type": "bool",
        "value": "",
        "tag": f"{robot}:1",
        "boolValue": True
    }


def undate_pp_point(scene: dict, data: dict):
    """更新场景停靠数据"""
    scene_area = scene['areas']
    data_t = {v: k for k, v in data.items()}  # 反转字典
    print(data_t)
    for area in scene_area:
        points = area['logicalMap']['advancedPoints']
        num = 0
        for point in points:
            if point['className'] == 'ParkPoint':
                pp = point['instanceName']
                properties = point['property']
                for _property in properties:
                    if _property['key'] == 'parkPoint' and len(_property['tag']):
                        break
                else:
                    if data_t.get(pp) is None:
                        print(f"{pp} 点未绑定")
                    else:
                        num += 1
                        properties.append(init_pp_data(data_t[pp]))
        print("绑定点数量:", num)


# print(json.dumps(scene["areas"], indent=4))
# undate_scene(scene)
# print(json.dumps(scene["areas"], indent=4))

# with open(scene_path, "r", encoding="utf-8") as scene_file:
#         scene = json.load(scene_file)
#         print(json.dumps(scene["areas"], indent=4))
#         undate_scene(scene)
#
#         json.dump(scene,scene_file)
#         # scene_file.seek(0)
#         scene2 = json.load(scene_file)
#         print(json.dumps(scene2["areas"], indent=4))


# for key, value in agv2pos.items():
#     move_robot(key, value, ip='192.168.10.30')

# 未分配 PP 点的机器人先随机初始化位置
# for i in range(1, 78):
#     agv = str('sim_' + str(i + 78))
#     pos = str('AP' + str(i))
#     move_robot(agv, pos, ip='192.168.10.30')


if __name__ == '__main__':
    with open(scene_path, "r+", encoding="utf-8") as scene_file:
        scene = json.load(scene_file)
        # 修改并返回数据
        undate_pp_point(scene, data)
        update_init_pos(scene, data)
        # print(json.dumps(scene,indent=4))
        # 写回数据
        scene_file.truncate(0)
        scene_file.seek(0)
        # print(json.dumps(scene["areas"], indent=4))
        json.dump(scene, scene_file)
