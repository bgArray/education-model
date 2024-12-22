from utils import *
import pickle


# 初始化学习空间
# 说明：x轴：正方向：理科，   负方向：文科；
# -    y轴：正方向：实践性， 负方向：理论性
init_learning = [
    Subject("语文", VectorDescriber(-1, -1, 40)),
    Subject("数学", VectorDescriber(1, -1, 40)),
    Subject("物理", VectorDescriber(1, 1, 40)),
    Subject("经济", VectorDescriber(-1, 1, 40)),
]
init_blank_sub = [
    Subject("语文", VectorDescriber(-1, -1, 0)),
    Subject("数学", VectorDescriber(1, -1, 0)),
    Subject("物理", VectorDescriber(1, 1, 0)),
    Subject("经济", VectorDescriber(-1, 1, 0)),
]


# 初始化学习能力曲线函数
with open("data.pkl", "rb") as f:
    y_smooth: list = pickle.load(f)
# print(y_smooth.__len__())  # 300
# print(y_smooth)


def age_learn(age: int) -> float:
    if age <= 0:
        return 0
    if age < 6:
        return 2 * 0.0025
    elif age <= 18:
        if age == 18:
            return int(y_smooth[(age - 6) * 25 - 1]) * 0.0025
        return int(y_smooth[(age - 6) * 25]) * 0.0025
    elif age < 50:
        return 24.595 * np.exp(-0.006 * age)
    else:
        return -1


def c_subject_allow(increase: float, n: int = 3, k: int = 80):  # k分配多少时间在正业 n自然年增长
    rr = random.randint(1, 99)
    result = n + increase * (k / 100) / 12
    if rr >= 70:  # 默认许可创立者概率有30%
        result += increase * (k / 100) / (100 - rr) / 5
    return result


def normal_increase(now: float, increase: float, max_: float, n: int = 3, k: int = 80):  # k分配多少时间在正业 n自然年增长
    if now + 10 < max_:
        return n + increase * (k / 100) / 12
    elif max_ - 10 <= now <= max_:
        rr = random.randint(1, 99)
        result = (max_ - now) * 0.5
        if rr >= 90:  # 10%
            result += increase * (k / 100) / (100 - rr) / 5
        return result
    else:
        return c_subject_allow(increase, n, k)


# for i in range(19, 50):
#     print(age_learn(i))
# n = 0
# for i in range(19):
#     n += age_learn(i)
# print(n)
# print(age_learn(18))

# if __name__ == '__main__':
#     # 绘制学习能力曲线
#     data_ = [194, 242, 714, 1714, 2733, 2138, 4048, 3197, 3570, 5215, 4759, 838]  # https://arxiv.org/pdf/2302.07738
#     data = [194, 242, 714, 1114, 1638, 2133,
#             3697, 4170, 4848,
#             6759, 7715, 9838]
#     import numpy as np
#     import matplotlib.pyplot as plt
#     from scipy.interpolate import make_interp_spline
#     import pickle
#
#     # 假设你的数据如下
#     x = range(1, 4381, 365)
#     y = data
#
#     # 创建新的x值用于绘制光滑的曲线
#     x_new = np.linspace(min(x), max(x), 300)
#
#     # 使用make_interp_spline创建光滑曲线
#     spl = make_interp_spline(x, y, k=3)  # k=3表示使用三次样条插值
#     y_smooth = spl(x_new)
#     print(y_smooth)
#     # use pickle save data
#     with open('data.pkl', 'wb') as f:
#         pickle.dump(y_smooth, f)
#
#
#     # 绘制原始数据点和光滑曲线
#     plt.plot(x, y, 'o', label='原始数据点')
#     plt.plot(x_new, y_smooth, '-', label='光滑曲线')
#     plt.legend()
#     plt.xlabel('X轴')
#     plt.ylabel('Y轴')
#     plt.title('光滑曲线示例')
#     plt.show()
