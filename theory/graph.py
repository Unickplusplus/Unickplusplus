import os, sys
from math import comb
import matplotlib.pyplot as plt

'''
Pr[hitting] = \frac{K \cdot 2^{n - m}}{\sum \frac{C_n^i * C_{m - n} ^ {l - i}}{C_m^l * K * 2^{i - l}}}
'''

def genValue(M, N, K, L):
    res = 0
    for i in range(max(L + N - M, 0), min(N, L) + 1): 
        res = res + comb(N, i) * comb(M - N, L - i) / comb(M, L) * (2 ** (i - L + K)) 
    return 2 ** (N - M + K) / res 

def genList(M, N, K):
    x_L, y_Pr = [], []
    for L in range(K, K + 20):
        x_L.append(L)
        y_Pr.append(genValue(M, N, K, L))   
    # plt.plot(x_L, y_Pr)
    # plt.show()
    print(y_Pr[-1] / y_Pr[0])
    return x_L, y_Pr     


if __name__ == '__main__':
    print(genList(50, 10, 10))
    print(genList(50, 30, 10))
    print(genList(50, 10, 25))
    print(genList(50, 30, 25))
