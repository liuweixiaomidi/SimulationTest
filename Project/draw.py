import numpy as np
import matplotlib.pyplot as plt


# 定义曲线函数
def tanh(i, m: int):
    match m:
        case 0:
            w = (np.exp(-i) - np.exp(i)) / (np.exp(-i) + np.exp(i)) + 2   # 双曲正切函数
        case 1:
            w = (50 * np.exp(-0.3 * i) + 1) * 2.5     # 指数函数
        case _:
            return
    return w


# 设置 x 的范围
x = np.linspace(0, 15, 100)

# 计算 y 值
y = tanh(x, 1)

# 绘制曲线
plt.plot(x, y)

# 显示图像
plt.show()
