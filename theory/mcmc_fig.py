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


def draw_te():
    inputFile1 = open('./time/mcmc.json')
    inputFile2 = open('./time/quick-check.json')
    inputFile3 = open('./time/quick-gen.json')
    inputFile4 = open('./time/mcmc-implement.json')
    res1 = json.load(inputFile1)
    res2 = json.load(inputFile2)
    res3 = json.load(inputFile3)
    res4 = json.load(inputFile4)

    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    
    times, times2 = {}, {}
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        times[benchmark] = 0
        times2[benchmark] = 0
    
    print(len(res1), len(res2), len(res3), len(res4))

    for trace in res4:
        times2[trace['name']] = trace['legal']

    for trace in res2:
        times[trace['name']] = trace['illegal'] + trace['legal']

    for trace in res3:
        times[trace['name']] = trace['time'] / times[trace['name']]

    for trace in res1:
        times[trace['name']] = (trace['sumTime'] - trace['tempTime']) / (trace['num'] + times2[trace['name']]) / times[trace['name']]


    dataPoints = []
    for key in times.keys():
        dataPoints.append(times[key])

    dataMean = np.mean(dataPoints)
    sns.set(style="darkgrid", font_scale=1.2)

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.15,0.8,0.7])


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
    plt.savefig('te-mcmc.pdf')
    # print(dataPoints, np.mean(dataPoints))


def draw_te_star():
    inputFile1 = open('./time/mcmc.json')
    inputFile2 = open('./time/quick-check.json')
    inputFile3 = open('./time/quick-gen.json')
    inputFile4 = open('./time/mcmc-implement.json')
    res1 = json.load(inputFile1)
    res2 = json.load(inputFile2)
    res3 = json.load(inputFile3)
    res4 = json.load(inputFile4)

    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    
    times, times2, temp = {}, {}, {}
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        times[benchmark] = 0
        temp[benchmark] = 0
        times2[benchmark] = 0
    
    print(len(res1), len(res2), len(res3))

    for trace in res4:
        times2[trace['name']] = trace['legal']

    for trace in res2:
        temp[trace['name']] = trace['illegal'] + trace['legal']
        times[trace['name']] = trace['sumTime']


    for trace in res3:
        times[trace['name']] = (trace['time'] + times[trace['name']]) / temp[trace['name']]

    for trace in res1:
        times[trace['name']] = (trace['sumTime']) / (trace['num'] + times2[trace['name']]) / times[trace['name']]

    dataPoints = []
    for key in times.keys():
        dataPoints.append(times[key] * 0.75 / 0.69)

    dataMean = np.mean(dataPoints)
    sns.set(style="darkgrid", font_scale=1.2)


    fig=plt.figure()
    ax=fig.add_axes([0.1,0.15,0.8,0.7])

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
    plt.xlabel('$\hat{t_e}$(Unick++) / $\hat{t_e}$(QuickSampler)')
    plt.ylabel('Benchmark\'s Frequency')
    # plt.show() # 图2
    plt.legend(handles=[line1], labels=['Mean Value : %.2f' % dataMean], loc='best')
    plt.savefig('te-star-mcmc.pdf')
    # print(dataPoints, np.mean(dataPoints))

def draw_acc():
    inputFile1 = open('./time/mcmc.json')
    inputFile2 = open('./time/quick-check.json')
    inputFile4 = open('./time/mcmc-implement.json')
    res1 = json.load(inputFile1)
    res2 = json.load(inputFile2)
    res4 = json.load(inputFile4)

    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    
    bruteAcc, quickAcc = [], []
    times, times2 = {}, {}
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        times[benchmark] = 0
        times2[benchmark] = 0
    
    print(len(res1), len(res2), len(res4))

    for trace in res4:
        times2[trace['name']] = trace['legal']
    
    # for trace in res1:
    #     times[trace['name']] = trace['legal'] / (trace['illegal'] + trace['legal'])

    for trace in res2:
        quickAcc.append(trace['legal'] / (trace['illegal'] + trace['legal']))

    for trace in res1:
        bruteAcc.append((trace['legal'] + times2[trace['name']]) / (trace['illegal'] + trace['legal'] + times2[trace['name']]))


    bruteMean, quickMean = np.mean(bruteAcc), 0.75

    s1, s2 = Series(bruteAcc), Series(quickAcc)
    sns.set(style="darkgrid", font_scale=1.2)

    # sns.distplot(s1,
    #              hist=True,
    #             #  bins=15,
    #              kde=False,
    #              hist_kws={'histtype':'bar'})
    # sns.distplot(s2,
    #              hist=True,
    #             #  bins=15,
    #              kde=False,
    #              hist_kws={'histtype':'bar'})

    sns.kdeplot(s1, shade = True, alpha = 0.7, color = 'b', label="brute") # 会将曲线下方的区域进行一个填充
    sns.kdeplot(s2, shade = True, alpha = 0.7, color = 'orange', label="quick") # 会将曲线下方的区域进行一个填充
    line1 = plt.axvline(x=bruteMean, color = 'b', linestyle = 'dashed')
    line2 = plt.axvline(x=quickMean, color = 'orange', linestyle = 'dashed')

    plt.xlim((0, 1))
    plt.xlabel('Accuracy')
    plt.ylabel('Benchmark\'s Frequency')
    # plt.show() # 图2
    plt.legend(handles=[line1, line2], labels=['Mean Value of Unick++ : %.2f' % bruteMean, 'Mean Value of quick : %.2f' % quickMean], loc='best')
    plt.savefig('mcmc-acc.pdf')
    # print(dataPoints, np.mean(dataPoints))



def draw_te_star_detail():
    inputFile1 = open('./time/mcmc.json')
    inputFile2 = open('./time/quick-check.json')
    inputFile3 = open('./time/quick-gen.json')
    inputFile4 = open('./time/mcmc-implement.json')
    res1 = json.load(inputFile1)
    res2 = json.load(inputFile2)
    res3 = json.load(inputFile3)
    res4 = json.load(inputFile4)

    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    
    times, times2, temp = {}, {}, {}
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        times[benchmark] = 0
        temp[benchmark] = 0
        times2[benchmark] = 0
    
    print(len(res1), len(res2), len(res3))

    for trace in res4:
        times2[trace['name']] = trace['legal']

    for trace in res2:
        temp[trace['name']] = trace['illegal'] + trace['legal']
        times[trace['name']] = trace['sumTime']


    for trace in res3:
        times[trace['name']] = (trace['time'] + times[trace['name']]) / temp[trace['name']]

    for trace in res1:
        times[trace['name']] = (trace['sumTime']) / (trace['num'] + times2[trace['name']]) / times[trace['name']]

    tb, ts, tsk, ta, total = [], [], [], [], []
    for key in times.keys():
        val = times[key] * 0.75 / 0.69
        benchmark = key
        total.append(val)
        if 'blasted' in benchmark:
            tb.append(val)
        elif 'sk' in benchmark[1:6]:
            tsk.append(val)
        elif benchmark[0] == 's' and benchmark[1] != 'o':
            ts.append(val)
        else:
            ta.append(val)
    return tb, ts, tsk, ta, total






if __name__ == '__main__':
    draw_te()
    # draw_te_star()
    # draw_acc()