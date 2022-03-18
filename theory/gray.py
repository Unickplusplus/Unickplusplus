import math
import random

from sympy import re

def count(num):
    res = 0
    while num > 0:
        res = res + (num % 2)
        num = num // 2
    return res

def gray(num, n):
    res = 0
    for i in range(n):
        res = res + (num & (1 << i)) ^ ((num >> 1) & (1 << i))
    return res

def gray_list(n, k):
    res = []
    for i in range(1 << (n - k)):
        res.append(gray(i * (1 << k), n))
    return res

def rand_list(n, k):
    res = []
    for i in range(1 << (n - k)):
        res.append(random.randint(0, 1 << n))
    return res

def average_dis(inp):
    cnt = []
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            cnt.append(count(inp[i] ^ inp[j]))
    return [len(cnt), sum(cnt)]

def average_dis2(results):
    return 0

def test():
    l = gray_list(12, 5)
    r = rand_list(12, 5)
    print(average_dis(l))
    print(average_dis(r))

if __name__ == '__main__':
    test()