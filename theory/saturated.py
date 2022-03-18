import sys, os
import numpy as np
import scipy
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd
import time
import json
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
import KL
import seaborn as sns



selected = ['blasted_case47', 'blasted_case110', 'blasted_squaring7', 'blasted_squaring16', 'blasted_case_1_b12_2.cnf', 's820a_7_4', 's820a_15_7', 's1238a_3_2', 's1196a_3_2', 's832a_15_7',
'blasted_case_1_b12_2', 'blasted_squaring7', '70.sk_3_40', '56.sk_6_38', '35.sk_3_52', '80.sk_2_48',
'7.sk_4_50', '19.sk_3_48', '29.sk_3_45', '17.sk_3_45', '81.sk_5_51', '77.sk_3_44', '20.sk_1_51', 
'ProcessBean.sk_8_64', 'LoginService2.sk_23_36', 'sort.sk_8_52', 'enqueueSeqSK.sk_10_42', 
'tutorial3.sk_4_31']

saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']


def generate_table():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    

    # inputFile1 = open('./time/mcmc.json')
    # inputFile2 = open('./time/quick-check.json')
    # inputFile3 = open('./time/quick-gen.json')
    # inputFile4 = open('./time/mcmc-implement.json')
    # res1 = json.load(inputFile1)
    # res2 = json.load(inputFile2)
    # res3 = json.load(inputFile3)
    # res4 = json.load(inputFile4)

    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    
    times, times2 = {}, {}
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        times[benchmark] = 0
        times2[benchmark] = 0

    dataPoints = []
    for key in times.keys():
        dataPoints.append(times[key])

    dataMean = np.mean(dataPoints)

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])


    s = Series(dataPoints)
    sns.set(style="darkgrid")

    sns.distplot(s,
                 hist=True,
                #  bins=15,
                 kde=False,
                 hist_kws={'histtype':'bar'})

                 
    # sns.kdeplot(s, shade = True, alpha = 0.7, label="te(brute) / te(quicksampler)") # 会将曲线下方的区域进行一个填充
    # sns.kdeplot(s2, shade = True, alpha = 0.7, label="src") # 会将曲线下方的区域进行一个填充
    line1 = plt.axvline(x=dataMean)
    plt.xlim((0,np.max(dataPoints)))
    plt.xlabel('$t_e$(Unick++) / $t_e$(QuickSampler)')
    plt.ylabel('Benchmark\'s Frequency')
    # plt.show() # 图2
    plt.legend(handles=[line1], labels=['Mean Value : %.2f' % dataMean], loc='best')
    plt.savefig('saturated.pdf')
    # print(dataPoints, np.mean(dataPoints))



if __name__ == '__main__':
    generate_table()