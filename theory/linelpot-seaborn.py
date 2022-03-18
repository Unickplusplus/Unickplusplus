from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import copy
import numpy as np

# a list of demo
list_demo = [{1: 10, 100: 20, 1000: 30}, {1: 20, 100: 20, 1000: 20}, {1: 30, 100: 20, 1000: 10}]


# list_demo
# count: 'g' for group, 's' for single
# column_names: the list of column name
# dict_names: the list of names of each dict
def creat_df(list_demo, column_names, dict_names):
    # if len(column_names) == 0:
    #     print('errors! please specify the columns !')
    #     return None
    all_line = list()
    for i, demo in enumerate(list_demo):
        dict_name = dict_names[i]
        for pair in demo.items():
            key = pair[0]
            value = pair[1]
            all_line.append([dict_name, key, value])
    df = pd.DataFrame(all_line, columns=column_names, dtype=float)
    return df


def draw_figure():

    sns.set(style="darkgrid")

    column_names = ['sampler', 'distance', 'count']
    dict_names = ['sampler1', 'sampler2', 'sampler3']

    df = creat_df(list_demo, column_names, dict_names)
    g_result = sns.lineplot(x="distance", y="count", # style for different sytle of lines
                 hue="sampler",
                 data=df, marker='o')
    g_result.set(xscale='log')


    # # style related command
    # sns.despine(offset=10, trim=True) # 去除实心边框
    # plt.legend(loc='upper center')


def save_figure(name):
    pdf = PdfPages(name + '.pdf')
    draw_figure()
    pdf.savefig()
    plt.show()
    plt.close()
    pdf.close()


save_figure('example')
