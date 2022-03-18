import numpy as np
import scipy
import pandas as pd
import os, sys
import json
import copy
import KL

def bench_val(benchmark, key, js):
    # print(benchmark, key)
    for i in js:
        if i['name'] == benchmark:
            return i[key]

def illustration():
    selected = ['blasted_case47', 'blasted_case110', 'blasted_squaring7', 'blasted_squaring16', 's820a_7_4', 's820a_15_7', 's1238a_3_2', 's1196a_3_2', 's832a_15_7',
    'blasted_case_1_b12_2', 'blasted_squaring7', '70.sk_3_40', '56.sk_6_38', '35.sk_3_52', '80.sk_2_48',
    '7.sk_4_50', '19.sk_3_48', '29.sk_3_45', '17.sk_3_45', '81.sk_5_51', '77.sk_3_44', '20.sk_1_51', 
    'ProcessBean.sk_8_64', 'LoginService2.sk_23_36', 'sort.sk_8_52', 'enqueueSeqSK.sk_10_42', 
    'tutorial3.sk_4_31']
    
    parameters = [['blasted_case47', 28, 118, 328, 262144, 426, 0.564],
        ['blasted_case110', 17, 287, 1263, 16384, 34, 0.822],
        ['blasted_squaring7', 72, 1628, 5837, 274408144896, 22186, 0.112], 
        # ['blasted_squaring16', 72, 1627, 5835, 1865275930882, 215680, 0.209],
        ['blasted_case_1_b12_2', 45, 827, 2725, 274877906944, 71769, 0.739], 
        ['s820a_7_4', 23, 616, 1703, 591872, 802, 0.770], 
        ['s820a_15_7', 23, 685, 1987, 722944, 674, 0.674], 
        ['s1238a_3_2', 32, 686, 1850, 2466250752, 60515, 0.936], 
        ['s1196a_3_2', 32, 690, 1805, 1038090240, 60320, 0.803],
        ['s832a_15_7', 23, 693, 2017, 3713024, 3803, 0.818], 
        ['70.sk_3_40', 40, 4670, 15864, 8589934592, 109854, 1.000],
        ['56.sk_6_38', 38, 4842, 17828, 3690987520, 71623, 0.930], 
        ['35.sk_3_52', 52, 4915, 10547, 4398046511104, 435883, 1.000],
        ['80.sk_2_48', 48, 4969, 17060, 1099511627776, 103909, 1.000], 
        ['7.sk_4_50', 50, 6683, 24816, 2199023255552, 296687, 1.000], 
        ['19.sk_3_48', 48, 6993, 23867, 2959802892288, 814253, 0.937],
        ['29.sk_3_45', 45, 8866, 31557, 347892350976, 1995316, 0.855],
        ['17.sk_3_45', 45, 10090, 27056, 274877906944, 3207452, 1.000],
        ['81.sk_5_51', 51, 10775, 38006, 18141941858304, 1035125, 0.867],
        ['77.sk_3_44', 44, 14535, 27573, 18253611008, 2552683, 0.966],
        ['20.sk_1_51', 51, 15475, 60994, 37108517437440, 2360454, 0.910], 
        ['ProcessBean.sk_8_64', 64, 4768, 14458, 7009386627072, 179418, 0.906],
        ['LoginService2.sk_23_36', 36, 11511,41411, 163840, 34, 0.724],
        ['sort.sk_8_52', 52, 12125, 49611, 88046829568, 155253, 0.625],
        ['enqueueSeqSK.sk_10_42', 42, 16466, 58515, 3355443200, 30830, 0.762],
        # ['tutorial3.sk_4_31', 31, 486193, 2598178, 49283072, 18783, 0.798]
        ]

    tempKeys = ['Benchmark', '|S|', 'Vars', 'Clauses', 'Solutions', 'Acc', r't_{avg}', r'\hat(t_{avg})', 'Acc', r't_{avg}', r'\hat(t_{avg})', r't_{avg}']
    temp = {}
    for key in tempKeys:
        temp[key] = ''

    df = pd.DataFrame(columns = ['Benchmark', '|S|', 'Vars', 'Clauses', 'Solutions', 'Acc', r't_{avg}', r'\hat(t_{avg})', 'DIS-JS', 'QAcc', r'Qt_{avg}', r'Q\hat(t_{avg})', 'DIS-JS1', r'Ut_{avg}'])

    inputFile1 = open('./time/mcmc.json')
    inputFile2 = open('./time/quick-check.json')
    inputFile3 = open('./time/quick-gen.json')
    inputFile4 = open('./time/mcmc-implement.json')
    mcRes = json.load(inputFile1)
    quickCheck = json.load(inputFile2)
    quickGen = json.load(inputFile3)
    mcImp = json.load(inputFile4)



    for line in parameters:
        newTemp = copy.deepcopy(temp)
        benchmark = line[0] + '.cnf'
        print(benchmark)
        newTemp['Benchmark'], newTemp['|S|'], newTemp['Vars'] = line[0], line[1], line[2]
        newTemp['Clauses'], newTemp['Solutions'] = line[3], line[4]
        newTemp['QAcc'] = line[6]

        newTemp['Acc'] = (bench_val(benchmark, 'legal', mcRes) + bench_val(benchmark, 'legal', mcImp)) / (bench_val(benchmark, 'legal', mcRes) + bench_val(benchmark, 'legal', mcImp) + bench_val(benchmark, 'illegal', mcRes))
        newTemp[r't_{avg}'] = 1000 * (bench_val(benchmark, 'sumTime', mcRes) - bench_val(benchmark, 'tempTime', mcRes)) / (bench_val(benchmark, 'num', mcRes) + bench_val(benchmark, 'legal', mcImp))
        newTemp[r'\hat(t_{avg})'] = 1000 * bench_val(benchmark, 'sumTime', mcRes) / (bench_val(benchmark, 'num', mcRes) + bench_val(benchmark, 'legal', mcImp)) / 0.69
        newTemp['DIS-JS'] = KL.J_S('./mcmc_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')


        newTemp[r'Qt_{avg}'] = 1000 * bench_val(benchmark, 'time', quickGen) / (bench_val(benchmark, 'legal', quickCheck) + bench_val(benchmark, 'illegal', quickCheck))
        newTemp[r'Q\hat(t_{avg})'] = 1000 * bench_val(benchmark, 'sumTime', quickCheck) / (bench_val(benchmark, 'illegal', quickCheck) + bench_val(benchmark, 'legal', quickCheck)) / 0.75
        newTemp['DIS-JS1'] = KL.J_S('./quick_dis/' + benchmark + '.samples.json', './oracle_dis/' + benchmark + '.oracle.json')


        newTemp[r'Ut_{avg}'] = line[5] * newTemp[r'Qt_{avg}']

        df = df.append(newTemp, ignore_index = True)
    df.to_excel('./table.xlsx', index=False)
    print(df)





if __name__ == '__main__':
    illustration()