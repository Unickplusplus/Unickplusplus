from nis import cat
import sys, os
import numpy as np
import scipy
from scipy.stats import norm
from matplotlib import pyplot as plt
import pandas as pd
import time
import json
import math


def gen_quick_2000(requirement):
    number = 0
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            os.system('../quicksampler/quicksampler -n ' + str(requirement) + ' ../theory/Benchmarks/' + benchmark)
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return


def gen_quick(requirement):
    time_quick = []
    number = 0
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            st = time.time_ns()
            os.system('../quicksampler/quicksampler -n ' + str(requirement) + ' ../theory/Benchmarks/' + benchmark)
            os.system('mv ../theory/Benchmarks/' + benchmark + '.samples ../theory/quick/' + benchmark + '.samples')
            end = time.time_ns()
            time_quick.append({'name' : benchmark, 'time' : (end - st) / 1000000000})
            print('time', (end - st) / 1000000000)
            os.system('../ssampler/ssampler ' + benchmark + ' ../theory/Benchmarks/' + benchmark + ' ../theory/quick/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))

    tempFile = open('./time/quick-gen.json', 'w')
    json.dump(time_quick, tempFile)
    tempFile.close()
    return


def gen_quick_saturated(requirement):
    # time_quick = []
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    number = 0
    # benchmarks = os.listdir('./Benchmarks')
    # benchmarks.sort()
    for benchmark in saturated:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            st = time.time_ns()
            os.system('../quicksampler/quicksampler -n ' + str(requirement) + ' ../theory/Benchmarks/' + benchmark)
            os.system('mv ../theory/Benchmarks/' + benchmark + '.samples ../theory/quick_saturated/' + benchmark + '.samples')
            end = time.time_ns()
            # time_quick.append({'name' : benchmark, 'time' : (end - st) / 1000000000})
            print('time', (end - st) / 1000000000)
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))

    # tempFile = open('./time/quick-gen.json', 'w')
    # json.dump(time_quick, tempFile)
    # tempFile.close()
    return


def gen_oracle(requirement):
    number = 0
    time_quick = []
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        # if number < 194:
        #     continue
        try:
            st = time.time_ns()
            os.system('cat ./Benchmarks/' + benchmark + ' | docker run --rm  -i -a stdin -a stdout msoos/unigen --samples ' + str(requirement) + ' > ./oracle/' + benchmark + '.oracle')
            end = time.time_ns()

            inputFile = open('./oracle_dis/' + benchmark + '.oracle.json')
            inputJSON = json.load(inputFile)
            counter = 0
            for key in inputJSON.keys():
                counter = counter + inputJSON[key]
            num = math.ceil(math.sqrt(counter * 2))
            time_quick.append({'name' : benchmark, 'time' : (end - st) / 1000000000, 'num' : num})
            print('time', (end - st) / 1000000000)
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))

    tempFile = open('./time/oracle-gen.json', 'w')
    json.dump(time_quick, tempFile)
    tempFile.close()
    return

def gen_oracle_saturated(requirement):
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    number = 0
    # time_quick = []
    # benchmarks = os.listdir('./Benchmarks')
    # benchmarks.sort()
    for benchmark in saturated:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        # if number < 194:
        #     continue
        try:
            st = time.time_ns()
            os.system('cat ./Benchmarks/' + benchmark + ' | docker run --rm  -i -a stdin -a stdout msoos/unigen --samples ' + str(requirement) + ' > ./oracle_saturated/' + benchmark + '.oracle')
            end = time.time_ns()

            # time_quick.append({'name' : benchmark, 'time' : (end - st) / 1000000000, 'num' : num})
            print('time', (end - st) / 1000000000)
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))

    # tempFile = open('./time/oracle-gen.json', 'w')
    # json.dump(time_quick, tempFile)
    # tempFile.close()
    return


def gen_brute_2000(requirement):
    number = 0
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            os.system('../ssampler/ssampler -n ' + str(requirement) + ' ../theory/Benchmarks/' + benchmark + ' ../theory/brute_2000/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return



def gen_brute(requirement):
    number = 0
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            os.system('../ssampler/ssampler -n ' + str(requirement) + ' ' + benchmark + ' ../theory/Benchmarks/' + benchmark + ' ../theory/brute/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return



def gen_brute_saturated(requirement):
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    number = 0
    # benchmarks = os.listdir('./Benchmarks')
    # benchmarks.sort()
    for benchmark in saturated:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            os.system('../ssampler/ssampler -n ' + str(requirement) + ' ' + benchmark + ' ../theory/Benchmarks/' + benchmark + ' ../theory/brute_saturated/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return



def gen_mcmc(requirement):
    number = 0
    benchmarks = os.listdir('./Benchmarks')
    benchmarks.sort()
    for benchmark in benchmarks:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        # if number < 26:
        #     continue
        try:
            os.system('../mcmcsampler/mcmcsampler -n ' + str(requirement) + ' ' + benchmark + ' ../theory/Benchmarks/' + benchmark + ' ../theory/mcmc_temp/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return


def gen_brute_saturated_small(requirement):
    saturated = ['blasted_case47.cnf', 'blasted_case110.cnf', 's820a_7_4.cnf', 's820a_15_7.cnf', 'LoginService2.sk_23_36.cnf']
    number = 0
    # benchmarks = os.listdir('./Benchmarks')
    # benchmarks.sort()
    for benchmark in saturated:
        if not benchmark.endswith('.cnf'):
            continue
        number = number + 1
        print('current : ' + benchmark)
        try:
            os.system('../ssampler/ssampler -n ' + str(requirement) + ' ' + benchmark + ' ../theory/Benchmarks/' + benchmark + ' ../theory/brute_small/' + benchmark + '.samples')
        except:
            print('failed : ' + benchmark)
        print('finished : ' + benchmark)
        if number % 10 == 0:
            print('current number : ' + str(number))
    print('total numbers ' + str(number))
    return



if __name__ == '__main__':
    # gen_brute(2000)
    # gen_quick(2000)
    # gen_oracle(2000)
    # gen_quick(2000)
    # gen_mcmc(2000)
    # gen_oracle_saturated(100000)
    # gen_quick_saturated(1000000)
    # gen_brute_saturated(1000000)
    # gen_brute_2000(2000)
    gen_brute_saturated_small(2000)