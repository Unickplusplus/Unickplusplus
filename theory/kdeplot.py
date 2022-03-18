from turtle import color
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import KL

import seaborn as sns

np.random.seed(666)

s1 = Series(KL.cmp_brute())
s2 = Series(KL.cmp_quick())

# print(s1, s2)

sns.set(style="darkgrid")

sns.kdeplot(s1, shade = True, alpha = 0.7, label="src") # 会将曲线下方的区域进行一个填充
sns.kdeplot(s2, shade = True, alpha = 0.7, label="src") # 会将曲线下方的区域进行一个填充
plt.xlim((0,1))
plt.xlabel('JS-Divergence')
plt.ylabel('Density')
# plt.show() # 图2
plt.savefig('temp.svg', format = 'svg')