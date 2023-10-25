import csv
import os

from Lib.function import *

# scene_path = os.path.abspath(__file__)
# scene_path = os.path.dirname(scene_path)
# scene_path = os.path.join(scene_path, 'rds.scene')

scene_path = ('C:\\Users\\seer\\AppData\\Local\\RoboshopPro\\appInfo\\robots\\All\\b8feeb7e-63d9cdfe-99852c77-56a5ceef'
              '\\DispatchEditor\\scene')
scene_path = os.path.join(scene_path, 'rds.scene')

agv2pos = {}

with open(scene_path, "r") as scene_file:
    scene = json.load(scene_file)
# for item in scene:
#     print(item)
# print('\n')
# robot_group = scene['robotGroup']
# for group in robot_group:
#     # print(group)
#     if group['name'] == 'RobotGroup-01':
#         robot = group['robot']
#         print(robot)
#         for r in robot:
#             agv = r['id']
#             for r_property in r['property']:
#                 # print(r_property)
#                 pass
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

with open(csv_path, "w", newline='') as csv_file:
    csv_file.truncate(0)
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['agv', 'pp'])
    for key, value in agv2pos.items():
        csv_writer.writerow([key, value])
for key, value in agv2pos.items():
    move_robot(key, value, ip='127.0.0.1')
