import os
import re
import glob
import pandas as pd

config_log_path = r'C:\Users\seer\Downloads\RDSCore-Debug-20240510-0717-0747-20240510153421\log'


def rds_log_time_analyze(log_path: str = None):
    """
    分析日志中的 t-cost \n
    只分析最新的.log文件中最多 100 条最近的 TCost 日志 \n
    控制台打印:
        1. 分析 TCost 日志数量
        2. TCost 日志原文
        3. 每周期耗时
        4. 平均每周期耗时
        5. 耗时最长的 5 个周期
        6. 耗时最短的 5 个周期
    :param log_path: 日志所在文件夹路径, 默认路径写在 config_log_path
    :return: csv 耗时降序排序, 在同级文件 timeCost.csv 中
    """
    if log_path is None:
        log_path = config_log_path
    csv_path = os.path.join(os.path.dirname(__file__), 'timeCost.csv')
    search_pattern = os.path.join(log_path, f"*.log")  # 在.log文件中查找
    log_files = glob.glob(search_pattern)
    if not log_files:
        print(f"No log files found in {log_path}")
        return None
    latest_log_file_path = max(log_files, key=os.path.getmtime)  # 只分析最新的一个日志
    # keyword_lines = (lambda file_path, keyword: [
    #     m_line.strip() for m_line in open(file_path, 'r').readlines() if keyword in m_line
    # ] if os.path.exists(file_path) else [])(latest_log_file_path, 'TCost')
    # 找到所有包含 TCost 的行
    keyword_lines = [m_line.strip() for m_line in open(latest_log_file_path, 'r').readlines() if 'TCost' in m_line]
    # 最多只取最近 1000 条
    keyword_lines = keyword_lines[-1000:] if len(keyword_lines) > 1000 else keyword_lines
    if keyword_lines:
        print(f"Lines containing {len(keyword_lines)} 'TCost' in the file:")
        for line in keyword_lines:
            print(line)
        open(csv_path, 'w').close()  # 清空表格
        data_list = []
        for index, line in enumerate(keyword_lines):
            elements = (lambda m_line: re.findall(r'\[(.*?)]', m_line))(line)  # 提取[]内的元素
            time_cost = dict(zip(*[iter(elements[-1].split("|"))] * 2))  # 最后一个[]内的元素是记录各模块耗时的, 根据|拆分dict
            for key, value in time_cost.items():
                time_cost[key] = int(value)     # 耗时转为int
            sorted_time_cost = dict(sorted(time_cost.items(), key=lambda item: item[1], reverse=True))  # 耗时降序排序
            # dict 转为 DataFrame
            df_data = pd.DataFrame(list(sorted_time_cost.items()),
                                   columns=[f'Module-{index + 1}', f'TCost-{index + 1}'])
            data_list.append(df_data)
        df = pd.concat(data_list, axis=1)   # 按列追加
        time_cost_columns = df.iloc[0, 1::2]
        print(time_cost_columns)
        time_cost_columns = pd.to_numeric(time_cost_columns, errors='coerce')   # pandas.core.series.Series 转换为数值类型
        time_cost_columns = time_cost_columns.dropna()  # 删除有缺失值的行
        df.to_csv(csv_path, index=False)    # 写入csv文件
        print(f"平均每周期耗时: {time_cost_columns.mean()}")
        print(f"最大5个周期的耗时: {time_cost_columns.nlargest(5).values}")
        print(f"最小5个周期的耗时: {time_cost_columns.nsmallest(5).values}")
    else:
        print("No lines containing 'TCost' found in the file")


if __name__ == '__main__':
    rds_log_time_analyze()
