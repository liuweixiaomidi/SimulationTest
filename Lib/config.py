"""
配置文件 及 相关设置说明
"""

"""
设置默认参数值
ip: 服务器 ip
rds_scene_path: 调度场景文件夹路径 
"""
ip = '127.0.0.1'
# ip = '58.34.177.164'
# ip = '192.168.8.122'
# ip = '192.168.141.1'
# ip = '192.168.8.212'
scene_path = (r'C:\Users\seer\AppData\Local\RoboshopPro\appInfo\robots\All\b8feeb7e-63d9cdfe-99852c77-56a5ceef'
              r'\DispatchEditor\scene\rds.scene')

"""
csv 表格文件的规范要求:
    1. 一个流程由 pickups unloads rhythms label 描述, 对应表格的四列
       pickups：取货点集合, 每行记录一个点位, 列内不允许出现重复元素
       unloads：放货点集合, 每行记录一个点位, 列内不允许出现重复元素
       rhythms：节拍, 每隔此值秒发送一次订单, 列内元素值必须保持一致, 支持部分缺省
       label  ：标签, 此标签的机器人执行订单, 列内元素值必须保持一致, 支持部分缺省
    2. 一个流程的四列表格必须按上述顺序书写且不可缺失, 不同流程间的四列表格不可交叉
    3. 表头必须为 pickups unloads rhythms label
"""
