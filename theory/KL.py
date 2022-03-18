import numpy as np
import scipy
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd
import os, sys
import json

from sympy import re

def dis(vi, vj):
    res = 0
    for index in range(len(vi)):
        if vi[index] != vj[index]:
            res = res + 1
    return res

def read_oracle(inputPath, outputPath):
    file = open(inputPath)
    lines = file.readlines()
    vecs, res = [], []
    for line in lines:
        if line[0] == 'c':
            continue
        temp = line.split(' ')
        temp.remove(temp[-1])
        vecs.append(temp)
    print('num : ', len(vecs), inputPath)
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            res.append(dis(vecs[i], vecs[j]))
    if(len(res) < 10):
        raise Exception('unigen error')
    collected = pd.value_counts(res).to_dict()
    tempFile = open(outputPath, 'w')
    json.dump(collected, tempFile)
    tempFile.close()
    return collected

def read_input(inputPath, outputPath):
    file = open(inputPath)
    lines = file.readlines()
    vecs, res = [], []
    for line in lines:
        if line[0] == 'c':
            continue
        temp = []
        for i in range(3, len(line)):
            temp.append(line[i])
        vecs.append(temp)
    print('num : ', len(vecs), inputPath)
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            res.append(dis(vecs[i], vecs[j]))
    if(len(res) < 10):
        raise Exception('sampler error')
    collected = pd.value_counts(res).to_dict()
    tempFile = open(outputPath, 'w')
    json.dump(collected, tempFile)
    tempFile.close()
    return collected

def generate_oracle():
    distances = os.listdir('./oracle')
    distances.sort()
    num = 0
    for distance in distances:
        if not distance.endswith('oracle'):
            continue
        num = num + 1
        if num < 226:
            continue
        if num % 10 == 0:
            print('number : ', num)
        read_oracle('./oracle/' + distance, './oracle_dis/' + distance + '.json')

def generate_quick():
    distances = os.listdir('./quick_2000')
    distances.sort()
    num = 0
    for distance in distances:
        if not distance.endswith('samples'):
            continue
        num = num + 1
        # if num < 11:
        #     continue
        if num % 10 == 0:
            print('number : ', num)
        read_input('./quick_2000/' + distance, './quick_dis/' + distance + '.json')

def generate_brute():
    distances = os.listdir('./brute_2000')
    distances.sort()
    num = 0
    for distance in distances:
        if not distance.endswith('samples'):
            continue
        num = num + 1
        # if num < 263:
        #     continue
        if num % 10 == 0:
            print('number : ', num)
        read_input('./brute_2000/' + distance, './brute_dis/' + distance + '.json')


def generate_mcmc():
    distances = os.listdir('./mcmc')
    distances.sort()
    num = 0
    for distance in distances:
        if not distance.endswith('samples'):
            continue
        num = num + 1
        if num < 7:
            continue
        if num % 10 == 0:
            print('number : ', num)
        read_input('./mcmc/' + distance, './mcmc_dis/' + distance + '.json')


def generate():
    # generate_oracle()
    # generate_quick()
    generate_brute()
    # generate_mcmc()


def J_S(path1, path2):
    # print(path1, path2)
    inputFile1 = open(path1)
    inputFile2 = open(path2)
    dis_1 = json.load(inputFile1)
    dis_2 = json.load(inputFile2)

    # sum1, sum2 = 0, 0
    # for key in dis_1.keys():
    #     sum1 = sum1 + dis_1[key]
    # for key in dis_2.keys():
    #     sum2 = sum2 + dis_2[key]
    # print(sum1, sum2)

    x, y = [], []
    k1, k2, length = dis_1.keys(), dis_2.keys(), 0
    for k in k1:
        length = max(length, int(k))
    for k in k2:
        length = max(length, int(k))

    for i in range(length + 1):
        if str(i) in dis_1.keys():
            x.append(dis_1[str(i)])
        else:
            x.append(0)
        if str(i) in dis_2.keys():
            y.append(dis_2[str(i)])
        else:
            y.append(0)
    # print(np.sum(x), np.sum(y))
    # print(x, y)

    px = x / np.sum(x)
    py = y / np.sum(y)
    pm = []
    for i in range(length + 1):
        pm.append(0.5 * px[i] + 0.5 * py[i])

    # print(px, py)
    print(0.5 * scipy.stats.entropy(px, pm) , 0.5 * scipy.stats.entropy(py, pm))
    JS_div = 0.5 * scipy.stats.entropy(px, pm) + 0.5 * scipy.stats.entropy(py, pm)
    return JS_div

def cmpSingle(path1, path2):
    dis_1 = read_input(path1)
    dis_2 = read_oracle(path2)
    J_S(dis_1, dis_2)


def cmp_brute():
    benchmarks = os.listdir('./Benchmarks')
    # print(benchmarks)
    benchmarks.sort()
    num = 0
    js_divs = []
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./brute_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')
        js_divs.append(js_div)
    # print(js_divs, np.mean(js_divs))
    return js_divs


def cmp_quick():
    benchmarks = os.listdir('./Benchmarks')
    # print(benchmarks)
    benchmarks.sort()
    num = 0
    js_divs = []
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./quick_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')
        js_divs.append(js_div)
    # print(js_divs, np.mean(js_divs))
    return js_divs


def cmp_mcmc():
    benchmarks = os.listdir('./Benchmarks')
    # print(benchmarks)
    benchmarks.sort()
    num = 0
    js_divs = []
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./mcmc_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')
        js_divs.append(js_div)
    # print(js_divs, np.mean(js_divs))
    return js_divs



def cmp_mcmc_detail():
    benchmarks = os.listdir('./Benchmarks')
    # print(benchmarks)
    benchmarks.sort()
    num = 0
    tb, ts, tsk, ta, total = [], [], [], [], []
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./mcmc_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')
        total.append(js_div)
        if 'blasted' in benchmark:
            tb.append(js_div)
        elif 'sk' in benchmark[1:6]:
            tsk.append(js_div)
        elif benchmark[0] == 's' and benchmark[1] != 'o':
            ts.append(js_div)
        else:
            ta.append(js_div)

    # print(js_divs, np.mean(js_divs))
    return tb, ts, tsk, ta, total




def count_input(inputPath, outputPath):
    file = open(inputPath)
    lines = file.readlines()
    # results = {}
    # for line in lines:
    #     if line[0] == 'c':
    #         continue
    #     if line[3:] in results.keys():
    #         results[line[3:]] = results[line[3:]] + 1
    #     else:
    #         results[line[3:]] = 1
    #     temp = []

    results = []
    for line in lines:
        if line[0] == 'c':
            continue
        results.append(line[3:])

    collected = pd.value_counts(results).to_dict()
    values = []
    for key in collected.keys():
        values.append(collected[key])

    dis = pd.value_counts(values).to_dict()
    tempFile = open(outputPath, 'w')
    json.dump(dis, tempFile)
    tempFile.close()
    return dis


def count_saturated_quick():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']

    for benchmark in saturated:
        count_input('./quick_saturated/' + benchmark + '.samples', './quick_saturated/' + benchmark + '.samples.json')
    
def count_input_oracle(inputPath, outputPath):
    file = open(inputPath)
    lines = file.readlines()
    # results = {}
    # for line in lines:
    #     if line[0] == 'c':
    #         continue
    #     if line[3:] in results.keys():
    #         results[line[3:]] = results[line[3:]] + 1
    #     else:
    #         results[line[3:]] = 1
    #     temp = []

    results = []
    for line in lines:
        if line[0] == 'c':
            continue
        temp = ""
        for i in temp.split(' '):
            if "-" in i:
                temp = temp + '0'
            else:
                 temp = temp + '1'
        results.append(temp)

    collected = pd.value_counts(results).to_dict()
    values = []
    for key in collected.keys():
        values.append(collected[key])

    dis = pd.value_counts(values).to_dict()
    tempFile = open(outputPath, 'w')
    json.dump(dis, tempFile)
    tempFile.close()
    return dis


def count_saturated_oracle():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']

    for benchmark in saturated:
        count_input_oracle('./oracle/' + benchmark + '.oracle', './oracle_small/' + benchmark + '.oracle.json')
    
    


def count_saturated_brute():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']

    for benchmark in saturated:
        count_input('./brute_saturated/' + benchmark + '.samples', './brute_saturated/' + benchmark + '.samples.json')

def count_saturated_brute_small():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']

    for benchmark in saturated:
        count_input('./quick/' + benchmark + '.samples', './quick_small/' + benchmark + '.samples.json')

def cmp_sat_cnt():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    # print(benchmarks)
    num = 0
    js_divs = []
    for benchmark in saturated:
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./brute_saturated/' + benchmark + '.samples.json', './quick_saturated/' + benchmark + '.samples.json')
        js_divs.append(js_div)
    print(js_divs, np.mean(js_divs))
    return js_divs


def cmp_sat_cnt_small():
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    # print(benchmarks)
    num = 0
    js_divs = []
    for benchmark in saturated:
        num = num + 1
        if num % 10 == 0:
            print('number : ', num)
        js_div = J_S('./quick_small/' + benchmark + '.samples.json', './oracle_small/' + benchmark + '.oracle.json')
        js_divs.append(js_div)
    print(js_divs, np.mean(js_divs))
    return js_divs


if __name__ == '__main__':
    # cmpSingle(sys.argv[1], sys.argv[2])
    # generate()
    # cmp_brute()
    # cmp_quick()
    cmp_mcmc()
    # count_saturated_quick()
    # count_saturated_brute()    
    # cmp_sat_cnt()
    # count_saturated_brute_small()
    # cmp_sat_cnt_small()
    # count_saturated_oracle()