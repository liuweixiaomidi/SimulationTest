import os
import time

import pytz
import sqlite3
from datetime import datetime

def str_to_timestamp(date_str: str, date_format: str = "%Y-%m-%d %H:%M:%S", timezone: str = "Asia/Shanghai") -> int:
    """
    将日期字符串转换为 Unix 时间戳（指定时区）。
    :param date_str: 日期字符串，例如 '2024-11-20 00:00:00'
    :param date_format: 日期格式，默认为 '%Y-%m-%d %H:%M:%S'
    :param timezone: 时区名称，默认为 'Asia/Shanghai'
    :return: 时间戳（整数）
    """
    try:
        # 设置时区
        tz = pytz.timezone(timezone)
        # 解析日期字符串为本地时间
        local_time = datetime.strptime(date_str, date_format)
        # 转换为带时区的时间
        local_time = tz.localize(local_time)
        # 转换为 UTC 时间戳
        timestamp = int(local_time.timestamp())
        return timestamp
    except ValueError as e:
        print(f"Error parsing date string '{date_str}' with format '{date_format}': {e}")
        raise ValueError(f"Invalid date string '{date_str}' or format '{date_format}'. Please check inputs.") from e

def get_single_robot_wait_time_during_custom_time(robot_name: str, db_path: str, start_time: str=None, end_time: str=None, table_name: str='RobotEvent'):
    """
    计算单个机器人在自定义时间段内的总等待时间。
    :param robot_name: 机器人的名称
    :param db_path: 数据库路径
    :param start_time: 开始时间戳（可选）
    :param end_time: 结束时间戳（可选）
    :param table_name: 查询表格, 默认为 RobotEvent
    :return: 等待时间（秒）
    """
    if not os.path.exists(stat_db_path):
        print("Database file does not exist!")
    st = str_to_timestamp(start_time) if start_time is not None else 0
    et = str_to_timestamp(end_time) if end_time is not None else time.time()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    query = f'select * from {table_name} where event_type = ? and robot_id = ?'
    params = ["RobotStateChange", robot_name]
    if st:
        query += ' and timestamp >= ?'
        params.append(st)
    if et:
        query += ' and timestamp <= ?'
        params.append(et)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    record = []
    wait_time = 0

    for i in range(len(rows) - 1):
        current_row = rows[i]
        next_row = rows[i + 1]
        if current_row[2] == 'wait' and next_row[2] != 'wait':
            time_diff = next_row[3] - current_row[3]
            wait_time += time_diff
            record.append((current_row, next_row, time_diff))

    for current, _next, diff in record:
        print(f"Stat Change Record: {current}, {_next}, Time Difference: {diff}s")
    start_time = '数据库第一条记录' if start_time is None else start_time
    end_time = '此刻' if end_time is None else end_time
    print(f'{robot_name} 从 {start_time} 到 {end_time} 总计等待 {wait_time}s')
    return wait_time

if __name__ == "__main__":
    stat_db_path = r'C:\.SeerRobotics\rdscore\resources\db\stat.sqlite'
    robot_wait_time = get_single_robot_wait_time_during_custom_time('sim_01', stat_db_path,
                                                                    '2024-11-20 00:00:00',
                                                                    '2024-11-20 23:59:59')
