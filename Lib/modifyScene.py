# coding:utf8
# 本文件用于修改大型场景文件的绑定信息
# 场景文件路径为: 打开->打开场景文件夹->scene->rds.scene
# 推送场景, 重连, 场景修改即可生效
import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
sys.path.append(p)
import csv
import json
import os
import re
import networkx as nx      # networkx为第三方库,包含多种图论算法
import uuid
import math
import random
from enum import Enum


def getConfigValue(key: str) -> str:
    p = os.path.dirname(__file__)
    p = os.path.dirname(p)
    config_path = os.path.join(p, "config.json")
    with open(config_path, "r") as f:
        j = json.load(f)
        return j.get(key, "")



def max_match(func):
    """获得一个二分图的最大匹配, 并检验是否是完美匹配"""
    def hg_match(*args):
        """匈牙利匹配算法
            args 最后一个参数必须为字典, 键为点位, 其值是与该点位有关系的点位合集
        """
        edges=[]
        relationship=args[-1]
        if isinstance(relationship,str):
            print(relationship)
            return
        aconv={}
        rnode_list=[]
        rnode_ori=[]
        for l_node,r_nodes in relationship.items():
            for node in r_nodes:
                if isinstance(node,list):
                    if node not in rnode_ori:
                        rnode_ori.append(node)
                        uid = str(uuid.uuid4())
                        aconv.setdefault(uid, node)
                        edges.append((l_node, uid))
                    else:
                        for k, va in aconv.items():
                            if va == node:
                                edges.append((l_node, k))
                                break

                else:
                    edges.append((l_node,node))
                    rnode_list.append(node)
        print("releationship:",relationship,edges)
        g = nx.Graph()
        # 二分图左边点集合
        print(list(relationship.keys()))
        g.add_nodes_from(list(relationship.keys()),bipartite=0)
        # 二分图右边点集合
        print('r_nodes',rnode_list)
        g.add_nodes_from(rnode_list,bipartite=1)
        g.add_edges_from(edges)
        # 获取连通的分量
        connected_components = list(nx.connected_components(g))
        matching_all={}
        for component in connected_components:
            # 构建一个子图，只包含当前连通分量的节点和边
            subgraph = g.subgraph(component)
            # 使用匈牙利算法找到最大匹配
            matching = nx.bipartite.maximum_matching(subgraph)
            for i in list(matching.keys()):
                if i not in relationship.keys():
                    matching.pop(i)
            matching_all.update(matching)
        if aconv!={}:
            for i,j in matching_all.items():
                if aconv.get(j) is not None:
                    matching_all[i]=aconv[j]
        if len(matching_all)<len(relationship.keys()):
            print("不是完美匹配:",matching_all)
        new_args=list(args[:-1])
        new_args.append(matching_all)
        return func(*tuple(new_args))
    return hg_match


class AdvancedGroupType(Enum):
    TestOrder="TestOrder"
    Mutex="Mutex"
    UniqueStop="UniqueStop"
    def __str__(self):
        return self.name


def prep_update_pp(func):
    """数据处理"""
    def data_process(*args):
        data_origin=args[-1]
        for k,v in data_origin.items():
            if v=={}:
                del data_origin[k]
        count_points = 0
        for point in data_origin['points']:
            if isinstance(point, str):
                count_points += 1
            else:
                for i in point:
                    count_points += 1
        if data_origin.get('vehicles') is not None or data_origin.get('vehicles')!=[]:
            if len(data_origin['vehicles'])>count_points:
                # raise Exception("robots is mor than points")
                return func(args[0],args[1],"robots is mor than points")
        area=args[0].get_area()
        vehicles=[]
        robot_to_point={}
        for a in area.values():
            for v in a['robots']:
                robot_to_point.setdefault(v,[]).extend(a['points'])
        # print("robot_to_point",robot_to_point)
        if data_origin.get('vehicles') is None or data_origin.get('vehicles') == []:
            for a in area.values():
                for r in a['robots']:
                    vehicles.append(r)
                vehicles=list(set(vehicles))
        else:
            vehicles=data_origin['vehicles']
        data_new={}
        # 一个机器人一个点位
        if args[1]:
            for v in vehicles:
                for p in data_origin['points']:
                    if isinstance(p,list):
                        points=robot_to_point.get(v)

                        if points:
                            if set(p).issubset(set(points)):
                                print("set",set(p))
                                data_new.setdefault(v,[]).append(p)
                    elif isinstance(p,str):
                        if p in robot_to_point[v]:
                            data_new.setdefault(v,[]).append(p)
        new_args = list(args[:-1])
        new_args.append(data_new)
        print("data_new",data_new)
        return func(*new_args)
    return data_process


class CoreScene:
    """根据字典数据或csv文件批量修改地图数据"""

    def __init__(self,path=None):
        """"""
        self.path=(getConfigValue(key="scene_path") if path is None else path)
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"not found {self.path}")
        self.file=open(file=self.path, mode="r+", encoding="utf-8")
        self.scene=json.load(self.file)
        self.write_flag=False
        self.orrent=self.get_orrent()      # 场景中有朝向的点位
        self.numdict=self.get_point_num2dict()  # 场景中点位编号字典
        self.robotgroup=self._get_robotgroup()
        # self.csv_path=r"D:\workshop\doc\test.csv"

    def __del__(self):
        if self.write_flag==True:
            self.file.truncate(0)
            self.file.seek(0)
            json.dump(self.scene,self.file)
        print("test close file")
        self.file.close()

    @staticmethod
    def _random_hex_color():
        """#生成三个随机的十六进制数字，分别代表RGB颜色模型中的红绿蓝"""
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        return color

    def _get_robotgroup(self):
        """获取车组信息"""
        data={}
        scene_group = self.scene['robotGroup']
        for group in scene_group:
            for r in group['robot']:
                data.setdefault(group.get("name"),[]).append(r['id'])
        return data

    def print_scene(self)->None:
        print(json.dumps(self.scene, indent=4))

    def get_orrent(self)->dict:
        """获取朝向
            :return  返回所有点位朝向, 格式为字典 {'point_name':'dir',...}
        """
        points = {}
        scene_area = self.scene['areas']
        for area in scene_area:
            for p in area['logicalMap']['advancedPoints']:
                if p["ignoreDir"]==True:
                    continue
                else:
                    points.setdefault(p['instanceName'],p['dir'])
        return points

    def get_area(self)->dict:
        """获取区域信息

            :return  返回所有区域信息, 格式为字典 {{'area_name':{'robots':[...],'points':[...]}},...}}
        """
        areas_d = {}
        scene_area = self.scene['areas']
        for area in scene_area:
            areas_d.setdefault(area['name'], {})
            areas_m = areas_d[area['name']]
            for r in area['maps']:
                areas_m.setdefault('robots', []).append(r['robotId'])
            for p in area['logicalMap']['advancedPoints']:
                areas_m.setdefault('points', []).append(p['instanceName'])
        # print(json.dumps(areas_d, indent=4))
        return areas_d
    def get_point_xy(self,name:str=""):
        """
        获取点位的坐标
        :param name: 点位名称
        :return:
        """
        coordinate = None
        scene_area = self.scene['areas']
        for area in scene_area:
            # areas_d.setdefault(area['name'],{})
            # areas_m=areas_d[area['name']]
            for p in area['logicalMap']['advancedPoints']:
                if p['instanceName'] == name:
                    coordinate=p['pos']
                    break
            else:
                for p in area['logicalMap']['binLocationsList']:
                    if p['binLocationList'][0]['instanceName'] == name:
                        coordinate=['binLocationList'][0]['pos']
                        break
        return coordinate

    def get_insquare_points(self,rectangle:tuple=None,filter:str="AP"):
        """获取矩形坐标内的点位
        :param rectangle:
        :param filter:
        :return:
        """
        pointslist = []
        areas = self.scene['areas']
        for ar in areas:
            points = ar['logicalMap']['advancedPoints']
            if points != []:
                for p in points:
                    _match = re.match(filter, p['instanceName'])
                    if _match:
                        x = p['pos']['x']
                        y = p['pos']['y']
                        if x>rectangle[0] and x<rectangle[1] and y>rectangle[2] and y<rectangle[3]:
                            pointslist.append(p['instanceName'])
        return pointslist



    def get_bound_point(self,filter:str=None,search_only:bool=True)->dict:
        """查找绑定数据
           :param : filter 是否筛选, 默认返回所有充电点,停靠点, 可选的值有 'parkPoint'(只查找停靠点),'chargePoint'(只查找充电点)
           :param : search_only 是否只从PP,CP点查找 (速度更快)
        """
        def deal_bind_data(point:dict=None,f=filter,num:int=None):
            """"""
            for _property in point['property']:
                if f is None:
                    if (_property['key'] == 'parkPoint' or _property['key'] == 'chargePoint') and len(_property['tag']):
                            num += 1
                            robots = re.split(r':1,|:1', _property['tag'])
                            for r in robots:
                                if r:
                                    area_bound.setdefault(r, {}).setdefault(_property['key'],[]).append(point['instanceName'])
                                    area_bound_li.append(point['instanceName'])
                else:
                    if _property['key'] ==f and len(_property['tag']):
                        num += 1
                        robots = re.split(r':1,|:1', _property['tag'])
                        for r in robots:
                            if r:
                                area_bound.setdefault(r, {}).setdefault(_property['key'],[]).append(point['instanceName'])
                                area_bound_li.append(point['instanceName'])
            return num

        agv2pos={}
        scene_area = self.scene['areas']
        for area in scene_area:
            if area["maps"]!=[]:
                points = area['logicalMap']['advancedPoints']
                num = 0
                area_bound={}
                area_bound_li=[]
                for point in points:
                    if search_only:
                        if point['className'] == 'ParkPoint' or point['className'] == 'ChargePoint':
                            num=deal_bind_data(point=point,f=filter,num=num)
                        else:
                            continue
                    else:
                        num=deal_bind_data(point=point,f=filter,num=num)

                print(f"area {area['name']} has bound {num} points")
                if num!=0:
                    print(area_bound_li)
                agv2pos.update(area_bound)
        # 初始化点
        robots=self.scene['robotGroup']
        for group in robots:
            for r in group['robot']:
                for _property in r['property']:
                    if _property['key']=="initialPosition" and _property['stringValue']!='':
                        agv2pos.setdefault(r['id'],{}).setdefault('initialPosition',_property['stringValue'])
        print("binding_point",agv2pos)
        return agv2pos

    def get_advanced_points(self,name_list:list=None,prefix:str="",filter:str="AP")->dict:
        """获取高级组的点位, 返回点位数据的字典, 高级组名对应键, 值为点位数据
            :param: name_list 设置返回数据的键, 点位数据的字典的键根据name_list初始化, 若省略则使用高级组名字作为键
            :param: prefix 高级组名前缀, 只处理前缀为prefix的高级组, 支持模糊匹配, 详见re库的匹配规则
            :param: filter 筛选点位  eg: 'LM|SM|AP|CP'
            :return {'AdvancedGroup_name': [points_list], ...}
        """
        order_area={}
        name_list=([] if name_list is None else name_list)
        if not prefix.startswith('^'):
            prefix = '^' + prefix
        block_group=self.scene["blockGroup"]
        print("found AdvancedGroups as follows: ")
        index=0
        for advanced in block_group:
            _match=re.match(prefix,(advanced["name"]))
            if _match:
                if len(name_list)<=index:
                    print(advanced["name"])
                    # print("fuck")
                    name_list.append(advanced["name"])
                tem_dic = {name_list[index]:[]}
                for point in advanced["blockName"]:
                    if '-' not in point:
                        # _match=re.match(r'LM|SM|AP|CP',point)
                        _match=re.match(filter,point)
                        if _match:
                            tem_dic.setdefault(str(name_list[index]),[]).append(point)
                order_area.update(tem_dic)
                index += 1
        print(order_area)
        return order_area

    def get_advanced_path(self, name_list: list = None, prefix: str = "", filter: str = "AP")->dict:
        """获取高级组的线路, 返回点位数据的字典, 高级组名对应键, 值为点位数据
            :param: name_list 设置返回数据的键, 点位数据的字典的键根据name_list初始化, 若省略则使用高级组名字作为键
            :param: prefix 高级组名前缀, 只处理前缀为prefix的高级组
            :param: filter 筛选点位  eg: 'LM|SM|AP|CP'

            :return {'AdvancedGroup_name': [points_list], ...}
        """
        order_area = {}
        name_list = ([] if name_list is None else name_list)
        if not prefix.startswith('^'):
            prefix = '^' + prefix
        block_group = self.scene["blockGroup"]
        print("found AdvancedGroups as follows: ")
        index = 0
        for advanced in block_group:
            _match = re.match(prefix, (advanced["name"]))
            if _match:
                if len(name_list) <= index:
                    print(advanced["name"])
                    name_list.append(advanced["name"])
                tem_dic = {name_list[index]: []}
                # print(advanced["blockName"])
                for point in advanced["blockName"]:
                    if '-' in point:
                        # _match=re.match(r'LM|SM|AP|CP',point)
                        _match = re.match(filter, point)
                        if _match:
                            tem_dic.setdefault(str(name_list[index]), []).append(point)
                order_area.update(tem_dic)
                index += 1
        return order_area

    def get_advanced_leaves(self, name_list: list = None, prefix: str = "", filter: str = "AP")->dict:
        """获取高级组内的叶子节点
        :param: name_list 设置返回数据的键, 点位数据的字典的键根据name_list初始化, 若省略则使用高级组名字作为键
        :param: prefix 高级组名前缀, 只处理前缀为prefix的高级组
        :param: filter 筛选点位  eg: 'LM|SM|AP|CP'
        :return  {{'AdvancedGroup_name': [points_list], ...}  #
        """
        order_area = {}
        name_list = ([] if name_list is None else name_list)
        if not prefix.startswith('^'):
            prefix = '^' + prefix
        block_group = self.scene["blockGroup"]
        print("found AdvancedGroups as follows: ")
        index = 0
        for advanced in block_group:
            _match = re.match(prefix, (advanced["name"]))
            if _match:
                if len(name_list) <= index:
                    print(advanced["name"])
                    # print("fuck")
                    name_list.append(advanced["name"])
                tem_dic = {name_list[index]: []}
                # print(advanced["blockName"])
                adj_list = {}  # 邻接表
                for point in advanced["blockName"]:
                    if '-' in point:
                        # _match=re.match(r'LM|SM|AP|CP',point)
                        pos = point.split('-')
                        #
                        if adj_list.get(pos[0]) is None:
                            adj_list.setdefault(pos[0], [[],[]])[0].append(pos[1])
                        else:
                            adj_list[pos[0]][0].append(pos[1])
                        if adj_list.get(pos[1]) is None:
                            adj_list.setdefault(pos[1], [[], []])[1].append(pos[0])
                        else:
                            adj_list[pos[1]][1].append(pos[0])
                    else:
                        _match = re.match(filter, point)
                        if _match:
                            tem_dic.setdefault(str(name_list[index]), []).append(point)
                # print("points",tem_dic[str(name_list[index])])
                # print("adjust",adj_list)
                # 去除不在高级组的点位
                for p in tem_dic[str(name_list[index])][::-1]:
                    if len(adj_list.get(p)[0])+len(adj_list.get(p)[1])==2 and adj_list.get(p)[0]==adj_list.get(p)[1]:
                        continue
                    if len(adj_list.get(p)[0])+len(adj_list.get(p)[1])==1:
                        continue
                    else:
                        tem_dic[str(name_list[index])].remove(p)
                order_area.update(tem_dic)
                index += 1
        return order_area

    def get_advance_prepoint(self,name_list: list = None, prefix: str = "", filter: str = "LM")->dict:
        """找出高级组内的AP点和AP点相邻的前置点,AP点需是叶子节点,前置点默认是filter指定的点,默认LM点
        :param: name_list 设置返回数据的键, 点位数据的字典的键根据name_list初始化, 若省略则使用高级组名字作为键
        :param: prefix 高级组名前缀, 只处理前缀为prefix的高级组
        :param: filter 筛选点位  eg: 'LM|SM|AP|CP'
        :return  {'AdvancedGroup_name': {"prepoint":"APpoint",...}, ...}
        """
        data = {}
        name_list = ([] if name_list is None else name_list)
        if not prefix.startswith('^'):
            prefix='^'+prefix
        block_group = self.scene["blockGroup"]
        print("found AdvancedGroups as follows: ")
        index = 0
        for advanced in block_group:
            _match = re.match(prefix, (advanced["name"]))
            if _match:
                if len(name_list) <= index:
                    print(advanced["name"])
                    name_list.append(advanced["name"])
                tem_dic = {name_list[index]: []}
                # print(advanced["blockName"])
                adj_list = {}  # 邻接表
                for point in advanced["blockName"]:
                    if '-' in point:
                        # _match=re.match(r'LM|SM|AP|CP',point)
                        pos = point.split('-')
                        if pos[0].startswith("AP") and adj_list.get(pos[0]) is None and pos[1].startswith("LM"):
                            adj_list.setdefault(pos[0], pos[1])
                    else:
                        _match = re.match(filter, point)
                        if _match:
                            tem_dic.setdefault(str(name_list[index]), []).append(point)
                # print(adj_list)
                data.setdefault(advanced["name"],adj_list)
                index += 1
        return data


    def _only_the_point(self,data,point_type:str='parkPoint'):
        """剔除数据
        :param :  data 机器人绑定的停靠点数据, 格式为 {'robot_name': {'chargePoint': ['CP19',...], 'parkPoint': ['LM2',...],'initialPosition': []}}
        :param :  point_type 只保留类型为point_type 的数据
        :return  {'robot_name':['PP1',...]}
        """
        new_dic={}
        for i,j in data.items():
            if j.get(point_type) is not None:
                new_dic.setdefault(i,j[point_type])
        return new_dic

    @max_match
    def update_init_pos(self,data:dict)->bool:
        """一键配置写入(更新)初始化位置, 采用 Hungarian matching algorithm 求解
        :param :  data 机器人绑定的停靠点数据, 格式为{'robot_name':['PPpoint','PPpoint',...],...}
        : return bool
        """
        robotgroup = self.scene["robotGroup"]
        if len(data)!=0:
            self.write_flag=True
        else:
            return False
        for group in robotgroup:
            if group["robot"]!=[]:
                for robot in group["robot"]:
                    if isinstance(data.get(robot["id"]),str):
                        for ele in robot["property"]:
                            if ele["key"] == "initialPosition":
                                ele["stringValue"] = data[robot["id"]]
                            dir=self.orrent.get(data[robot["id"]])
                            if dir is not None:
                                if ele['key'] == 'dir':
                                    ele['doubleValue'] = dir*180/math.pi
                                    print(ele['doubleValue'])
                                    dir=None
                    if isinstance(data.get(robot["id"]),list):  # 后续优化 Hungarian matching algorithm 时兼容
                        for ele in robot["property"]:
                            if ele["key"] == "initialPosition":
                                ele["stringValue"] = data[robot["id"]][0]
                            dir = self.orrent.get(data[robot["id"]])
                            if dir is not None:
                                if ele['key'] == 'dir':
                                    ele['doubleValue'] = dir*360/math.pi
                                    print(ele['doubleValue'])
                                    dir=None
        print("initpos has been successfully written",data)
        return True

    def update_init_pos_dir(self):
        """
        更新机器人初始点的点位朝向
        :return:
        """
        flag=False
        robotgroup = self.scene["robotGroup"]
        for group in robotgroup:
            if group["robot"] != []:
                for robot in group["robot"]:
                    dir=None
                    dir_data=None
                    for ele in robot["property"]:
                        if ele["key"] == "initialPosition":
                            if ele["stringValue"]:
                                if self.orrent.get(ele["stringValue"]):
                                    dir=self.orrent.get(ele["stringValue"])
                        elif ele['key'] == 'dir':
                            dir_data=ele
                        if dir_data and dir:
                            dir_data['doubleValue']=dir * 180 / math.pi
                            flag=True
        if flag:
            self.write_flag=True
            print("dir has been successfully written")
        return True


    def update_init_pos_by_pp(self,onlypp=True):
        """使用绑定的停靠点设置初始化点
         : return bool
         """
        data=self.get_bound_point(filter="parkPoint",search_only=False)
        if onlypp:
            data=self._only_the_point(data)
        area=self.get_area()
        for ar in area.values():
            if ar.get('robots') is None:
                continue
            for v in ar["robots"]:
                if v not in data.keys():
                    print(f"{v} has no parkpoint")
        return  self.update_init_pos(data)

    def update_pp_point_specified(self,data:dict):
        """绑定停靠点, 每个机器人可以绑定一个点或多个点
           可以绑定PP点,LM点
           :param: data  修改的停靠数据, 格式为 robot_name: point_name

           :return None
        """
        def init_pp_data(robot:str):
            """初始化填入停靠数据"""
            return {
                "key": "parkPoint",
                "type": "bool",
                "value": "",
                "tag": robot,
                "boolValue": True
            }
        if len(data)==0:
            return
        self.write_flag=True
        scene_area = self.scene['areas']
        data_t={}
        # 反转字典
        for k,v in data.items():
            if isinstance(v,list):
                for point in v:
                    data_t.setdefault(point, []).append(k)
            if isinstance(v,str):
                data_t.setdefault(v,[]).append(k)
        for area in scene_area:
            points = area['logicalMap']['advancedPoints']
            num = 0
            for point in points:
                pp = point['instanceName']
                if data_t.get(pp) is None:
                    if point['className'] == 'ParkPoint':
                        print(f"parkpoint {pp} is not specified")
                    continue
                properties = point['property']
                flag=False
                for _property in properties:
                    if _property['key'] == 'parkPoint':
                        flag=True
                        for r in data_t[pp]:
                            if r in _property['tag']:
                                continue
                            else:
                                num += 1
                                _property['tag'] += f",{r}:1"
                    if flag==True:
                        break
                # 没有停靠属性
                else:
                    pp_str=""
                    for r in data_t[pp]:
                        num += 1
                        pp_str+=f"{r}:1"
                    # print(pp_str)
                    properties.append(init_pp_data(pp_str))
            print(f"{area['name']} has bound points:", num)

    @prep_update_pp
    @max_match
    def update_pp_point_random(self,ifonly:bool,data:dict):
        """根据给定点自动选择绑定停靠点,(不支持字典传参)
            :param: ifonly 一个机器人是否只绑定一个点位,目前只支持一个机器人绑定一个点位,必须为true
            :param: data  绑定数据,格式为{'points':[...], 'vehicles':[...]}, 若vehicles为空, 则绑定所有车
            :return None
        """
        print(data)
        self.update_pp_point_specified(data)

    def update_pp_by_init(self,search_only:bool=False):
        """根据初始化点位绑定停靠点
            :param: search_only 是否只从CP点,PP点中绑定, 例如 search_only=True, 如果initialPosition是LM点, 则不能将LM点绑定为停靠点
        """
        init_p=self.get_bound_point(search_only=search_only)
        self.update_pp_point_specified(self._only_the_point(init_p,point_type='initialPosition'))


    def clear_pp_point(self):
        """解绑停靠点"""
        scene_area = self.scene['areas']
        self.write_flag=True
        for area in scene_area:
            points = area['logicalMap']['advancedPoints']
            print(area['name']," clear:", end='\t')
            num = 0
            for point in points:
                pp = point['instanceName']
                properties = point['property']
                for _property in properties:
                    if _property['key'] == 'parkPoint':
                        _property['tag']=''
                        num+=1
                        print(pp,end=', ')
            print(num,"points total")

    def update_cp_point(self,data:dict):
        """绑定充电点,只能绑定CP点
            :param: data  绑定数据,格式为{'robot':['chargePoint',...],...}, 若vehicles为空, 则绑定所有车

            :return None

        """
        def init_cp_data(robot):
            """初始化填入停靠数据"""
            return {
                "key": "chargePoint",
                "type": "bool",
                "value": "",
                "tag": robot,
                "boolValue": True
            }
        if len(data)==0:
            return
        self.write_flag=True
        scene_area = self.scene['areas']
        data_t={}
        for k, v in data.items():
            for vp in v:
                data_t.setdefault(vp, []).append(k)
        for area in scene_area:
            points = area['logicalMap']['advancedPoints']
            num = 0
            for point in points:
                if point['className'] == 'ChargePoint':
                    cp = point['instanceName']
                    if data_t.get(cp) is None:
                        print(f"chargepoint {cp} is not specified")
                        continue
                    properties = point['property']
                    flag = False
                    for _property in properties:
                        if _property['key'] == 'chargePoint':
                            flag=True
                            for r in data_t[cp]:
                                if r in _property['tag']:
                                    continue
                                else:
                                    num += 1
                                    _property['tag'] += f",{r}:1"
                        if flag==True:
                            break
                    else:
                        cp_str = ""
                        for r in data_t[cp]:
                            num += 1
                            cp_str += f"{r}:1"
                        # print(pp_str)
                        properties.append(init_cp_data(cp_str))
            print(f"{area['name']} has bound points:", num)

    def clear_cp_point(self):
        """解绑充电点"""
        scene_area = self.scene['areas']
        self.write_flag=True
        for area in scene_area:
            points = area['logicalMap']['advancedPoints']
            print(area['name'],end='\t')
            num = 0
            for point in points:
                pp = point['instanceName']
                properties = point['property']
                flag = False
                for _property in properties:
                    if _property['key'] == 'chargePoint':
                        _property['tag'] = ''
                        num+=1
                        print(pp,end=' ')
            print(num)

    def clear_empty_adgroup(self):
        """删除空高级组
        """
        self.write_flag = True
        block_group = self.scene["blockGroup"]
        for bg in block_group[::-1]:
            if bg.get('blockName')==[]:
                print(f"del {bg.get('name')}")
                block_group.pop()
    def clear_adgroup(self,prfix:str=""):
        """
        删除前缀名为 prefix的高级组,如果prefix为空,则删除所有高级组
        :return:
        """
        self.write_flag=True
        block_group = self.scene["blockGroup"]
        regex=re.compile(f"^{prfix}")
        print("del",end='\t')
        for i in range(len(block_group)-1,-1,-1):
            # print(i,len(block_group))
            if regex.match(block_group[i]['name']):
                print(block_group[i]['name'], end=" ")
                block_group.pop(i)
        print(".")

    def add_advancedgroup(self,points_paths:list,name,type:AdvancedGroupType,adv_group_keys:dict):
        """添加高级组,只支持 Mutex, TestOrder, UniqueStop
        :param points_paths: 高级组需要包含的点位和线路
        :param name: 高级组名字
        :param type: 高级组类型
        """
        self.write_flag=True
        namelist=[]
        adv_json = {
            "name": "AdvancedGroup03",
            "blockName": [
            ],
            "property": [
                {
                    "key": "color",
                    "type": "string",
                    "value": "",
                    "tag": "",
                    "stringValue": self._random_hex_color()
                },
                {
                    "key": "type",
                    "type": "complexGroup",
                    "value": "",
                    "tag": "",
                    "stringValue": ""
                }
            ]
        }
        block_group = self.scene["blockGroup"]
        for bg in block_group:
            namelist.append(bg.get('name'))
        if name in namelist:
            raise ValueError(f"{name} already exists")
        adv_json["name"]=name
        adv_json["blockName"]=points_paths
        todict=None
        type=str(type)
        advanced_group=getConfigValue("advanced_group")
        if advanced_group[type]:
            todict=json.loads(advanced_group[type])
            for k,v in adv_group_keys.items():
                todict[type][k]['value']=v
        adv_json['property'][-1]['stringValue']=json.dumps(todict)
        block_group.append(adv_json)


    def advancedgroup_put_point(self,group_name:str,point_list:list=None,clear_first=False):
        """高级组添加点位
             :param: group_name  高级组名
             :param: point_list  点位列表,列表元素可以为 str,int
             :param: clear_first  在添加前是否清空点位
             :return None
        """
        self.write_flag = True
        block_group = self.scene["blockGroup"]
        # print(json.dumps(block_group, indent=4))
        for bg in block_group:
            if bg.get('name') == group_name:
                # 检查点位是否存在
                p_standard=None
                p_list=[]
                for p in point_list:
                    if isinstance(p,str):
                        p_standard=p[2:]
                        if self.numdict.get(p_standard)==p:
                            p_list.append(p)
                            continue
                    else:
                        if isinstance(p,int):
                            p2add=self.numdict.get(str(p))
                            if p2add is not None:
                                if p2add not in bg['blockName']:
                                    p_list.append(p2add)
                                continue
                    print(f"{p} not in scene")
                    return False
                if clear_first:
                    bg['blockName']=[]
                bg['blockName'].extend(p_list)
                print( bg['blockName'])
        # print(json.dumps(block_group, indent=4))

    def get_bin(self,prefix:str="",just_num:bool=False,area:str=None):
        """
        获取所有库位
            :param prefix: 库位前缀名, 支持模糊匹配 如 CS01HW[0-9]{3}  表示匹配CS01HW，后面跟随3个数字开头的字符串
            :param just_num:  是否去除前缀, 只保留编号
            :return: 库位列表
        """
        binlist=[]
        areas = self.scene['areas']
        if not prefix.startswith('^'):
            prefix='^'+prefix
        regex=re.compile(prefix)
        for ar in areas:
            if area is None or ar['name']==area:
                bins=ar['logicalMap']['binLocationsList']
                if bins!=[]:
                    for b in bins:
                        bname=b["binLocationList"][0]["instanceName"]
                        if regex.match(bname):
                            if just_num:
                                binlist.append(bname[len(prefix)-1:])
                            else:
                                binlist.append(bname)
        return binlist

    def get_near_point(self,coordinate:list=None,dist:float=10.0,area:str=None,filter:str="AP"):
        """
        找出距离坐标coordinate小于dist的所有点位(欧式距离)
        :param coordinate: 二维坐标 [0,0] 第一个为x坐标, 第二个为
        :param area: 区域
        :param dist: 距离
        :return: 点位列表
        """
        pointslist=[]
        areas = self.scene['areas']
        for ar in areas:
            if area is None or ar['name'] == area:
                points = ar['logicalMap']['advancedPoints']
                if points != []:
                    for p in points:
                        _match=re.match(filter,p['instanceName'])
                        if _match:
                            x = p['pos']['x']
                            y = p['pos']['y']
                            euclidean_dis = math.sqrt(sum((a - b) ** 2 for a, b in zip([x, y], coordinate)))
                            if euclidean_dis < dist and euclidean_dis>0:
                                pointslist.append(p['instanceName'])
        return pointslist

    def get_range_point(self,range_x:tuple=None,range_y:tuple=None,area:str=None,filter:str="AP"):
        """
        找出坐标在 range_x * range_y 区域内的所有点位
        :param range_x: 点位坐标x的范围
        :param range_y: 点位坐标x的范围
        :param area:
        :param filter:
        :return: 点位列表
        """
        pointslist = []
        areas = self.scene['areas']
        for ar in areas:
            if area is None or ar['name'] == area:
                points = ar['logicalMap']['advancedPoints']
                if points != []:
                    for p in points:
                        add_flag=False
                        _match = re.match(filter, p['instanceName'])
                        if _match:
                            if range_x:
                                x = p['pos']['x']
                                if range_x[0] <= x <= range_x[1]:
                                    add_flag=True
                                else:
                                    continue
                            if range_y:
                                y = p['pos']['y']
                                if range_y[0] <= y <= range_y[1]:
                                    add_flag=True
                                else:
                                    add_flag=False
                            if add_flag:
                                pointslist.append(p['instanceName'])
        return pointslist

    def get_near_bin(self,coordinate:list=None,dist:float=10.0,area:str=None):
        """
        找出距离坐标coordinate小于dist的所有库位(欧式距离)
        :param coordinate: 二维坐标 [0,0] 第一个为x坐标, 第二个为
        :param dist:
        :return: 库位列表
        """
        binlist = []
        areas = self.scene['areas']
        for ar in areas:
            if area is None or ar['name'] == area:
                bins = ar['logicalMap']['binLocationsList']
                if bins != []:
                    for b in bins:
                        x=b['binLocationList'][0]['pos']['x']
                        y=b['binLocationList'][0]['pos']['y']
                        euclidean_dis=math.sqrt(sum((a-b)**2 for a, b in zip([x,y],coordinate)))
                        # print(euclidean_dis)
                        if euclidean_dis<dist:
                            binlist.append(b["binLocationList"][0]["instanceName"])
        return binlist


    def add_point2adgroup(self,data):
        """添加高级组,只能将点位添加至高级组
        :param: data  {group_name:points}
        :return None
        """
        self.write_flag = True
        block_group = self.scene["blockGroup"]
        block_group.append(data)

    def add_delay_finishtime(self,vehicles:list=None,delay:float=5.0,points_l:list=None,area_name:str=None):
        """对点位添加delay finish time 属性
        :param vehicles: 在点位需要延迟动作的机器人
        :param delay: 延迟时间
        :param points: 点位
        :return:
        """
        nit={
            "key": "delayFinishTime",
            "type": "double",
            "value": "",
            "tag": "",
            "doubleValue": 0
        }
        self.write_flag=True
        scene_area = self.scene['areas']
        for area in scene_area:
            if area:
                if area['name']!=area_name:
                    # print(area['name'])
                    continue
            points = area['logicalMap']['advancedPoints']
            for point in points:
                pname = point['instanceName']
                # print(pname)
                if pname in points_l:
                    print("bin")
                    for proper in point['property']:
                        if proper['key']=='delayFinishTime':
                            proper['tag']=','.join([f"{v}:{delay}" for v in vehicles])
                            print(point['property'])
                            break
                    else:
                        nit['tag']=','.join([f"{v}:{delay}" for v in vehicles])
                        point['property'].append(nit)
                        print(point['property'])



    def get_point_num2dict(self):
        """获取所有点位编号

            :return list 由所有点位编号构成的列表
        """
        p_dict={}
        scene_area = self.scene['areas']
        for area in scene_area:
            for p in area['logicalMap']['advancedPoints']:
                if p_dict.setdefault(p['instanceName'][2:],p['instanceName'])==p['instanceName']:
                    continue
                else:
                    print(f"error scene,{p['instanceName'][2:]}")
                    return
        return p_dict


    def init_charge_param(self,chargeNeed=30,chargeOnly=10,chargedOk=50,chargedFull=70):
        """初始化充电参数
        """
        robotgroup = self.scene["robotGroup"]
        self.write_flag=True
        for group in robotgroup:
            if group["robot"] != []:
                for robot in group["robot"]:
                    if robot.get("id") is not None:
                        for ele in robot["property"]:
                            if ele["key"] == "chargeNeed":
                                ele["int32Value"] = chargeNeed
                            if ele["key"] == "chargeOnly":
                                ele["int32Value"] = chargeOnly
                            if ele["key"] == "chargedFull":
                                ele["int32Value"] = chargedFull
                            if ele["key"] == "chargedOk":
                                ele["int32Value"] = chargedOk
                    continue

    def init_sweep_param(self,maxDirtyWater=40,minCleanWater=20):
        """初始化扫地参数
        """
        robotgroup = self.scene["robotGroup"]
        self.write_flag = True
        for group in robotgroup:
            if group["robot"] != []:
                for robot in group["robot"]:
                    if robot.get("id") is not None:
                        for ele in robot["property"]:
                            if ele["key"] == "maxDirtyWater":
                                ele["int32Value"] = maxDirtyWater
                            if ele["key"] == "minCleanWater":
                                ele["int32Value"] = minCleanWater
                    continue

    def csv_read(self,csv_path:str=None)->csv.DictReader:
        """读取csv文件"""
        if not os.path.exists(csv_path):
            raise FileExistsError("csv_path not exist")
        with open(csv_path,newline='') as f:
            reader=csv.DictReader(f)
         #  for row in reader:
         #        print(row)
            return  reader

    def csv_write(self,csv_path:str=None,mode:str="area",datas_origin:dict=None):
        """
        :param csv_path:
        :param mode: orders表示生成运单数据, area表示生成逻辑库区数据

        :return: csv file
        """
        # if not os.path.exists(csv_path):
        #     raise FileExistsError("csv_path not exist")
        if datas_origin is None:
            raise ValueError("datas_origin supposed not to be Null")
        with open(csv_path,'w',newline='') as f:
            if mode=="area":
                writer=csv.DictWriter(f,['area','points'])
                writer.writeheader()
                datas=[]
                for a,p in datas_origin.items():
                    # area = a
                    # points,*_=i.values()
                    tem_dic = {'area':a,'points':','.join(p)}
                    datas.append(tem_dic)
                writer.writerows(datas)



# def test_dyb():
#     ip = '192.168.9.191'
#     rbk = rbklib(ip)
#     rbk.lock()
#     a = rbk.robot_status_all1_req(return_laser=False)
#     a = a[1].decode()
#     print(type(a))
#     print(a)


if __name__ == '__main__':
    scene_path = r"C:\Users\seer\AppData\Local\RoboshopPro\appInfo\robots\All\b8feeb7e-63d9cdfe-99852c77-56a5ceef\DispatchEditor\scene\rds.scene"
    test= CoreScene(path=scene_path)
    # test.print_scene()
    # print(json.dumps(test.get_area(),indent=4))
    # boundpoints=test.get_bound_point(search_only=False)
    # print("bound points",boundpoints)
    # print(test.get_ap_points())
    # print(test.get_advanced_points(filter="LM"))
    # adi=test.get_bound_point(search_only=False)
    # print(test.only_parkpoint(adi))
    # test.update_init_pos({"sim_01":["LM2","LM3"],"sim_02":["LM4"]})
    # test.clear_pp_point()
    # test.update_pp_point_random(True,{'points':[['LM4','LM5'],'LM301','LM2'],'vehicles':['sim_01','sim_02','sim_04']})
    # test.update_pp_point_random(True,{'points':['LM301','LM2'],'vehicles':['sim_01','sim_02','sim_04']})
    # update_pp_points={"sim_01":["LM2","LM3"]}
    # test.update_pp_by_init()
    # test.update_pp_point_specified(data=update_pp_points)
    # test.update_pp_point_random(points=["LM2","LM301"])
    # test.update_pp_point_random(points=[])
    # test.clear_cp_point()
    # test.update_pp_point_specified(data={})
    # test.clear_empty_adgroup()
    # test.adgroup_put_point(group_name="test",point_list=[18],clear_first=True)
    # print(test.numdict)
    # ps=test.get_advanced_points(prefix="Ad")
    # test.csv_write(csv_path='./test.csv',datas_origin=list(ps))
    # test.update_pp_by_init()
    # print(test.get_advanced_path(prefix="all_path", filter="LM"))
    a = test.get_range_point((-79, -56), (-55, -35))
    print(a)