from tkinter import font
from turtle import color
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import copy
import numpy as np
import KL
import mcmc_fig

# grouped boxplot
# dict_demo_group = {'s1-m1': [1, 2, 3, 4, 5, 6, 7, 8, 9], 's2-m2': [9, 8, 7, 6, 5, 4, 3, 2, 1], 's1-m2': [1, 3, 1, 2, 6, 7, 0, 8, 1],
#         's2-m1': [2, 6, 2, 4, 1, 2, 7, 2, 2]}

# single boxplot


# dict_demo
# count: 'g' for group, 's' for single
# column_names: the list of column name
def creat_df(dict_demo, count, column_names):
    # if len(column_names) == 0:
    #     print('errors! please specify the columns !')
    #     return None

    all_line = list()
    for pair in dict_demo.items():
        keys = pair[0]
        values = pair[1]
        if count == 's':
            for value in values:
                line = [keys, value]
                all_line.append(line)
        if count == 'g':
            arrs = keys.split('-')
            for value in values:
                line = copy.deepcopy(arrs)
                line.append(value)
                all_line.append(line)
    df = pd.DataFrame(all_line, columns=column_names, dtype=float)
    return df


def draw_figure():

    sns.set(style="darkgrid", font_scale=1.3)

    column_single = ['SAT sampler', 'JS-Divergence']
    column_group = ['Unick++', 'Brute-Force', 'QuickSampler']

    # single box

    dict_demo_single = {'Unick++': KL.cmp_mcmc(), 'Brute-Force': KL.cmp_brute(), 'QuickSampler': KL.cmp_quick()}
    df = creat_df(dict_demo_single, 's', column_single)
    ax = sns.boxplot(x="SAT sampler", y="JS-Divergence",
                data=df, linewidth=3, width=0.5)

    medians = df.groupby(['SAT sampler'])['JS-Divergence'].median().values
    means = df.groupby(['SAT sampler'])['JS-Divergence'].mean().values 
    plt.savefig('./aaa.svg', format = 'svg')
    # print(medians)

    # 统计各个种类的样本数
    
    # Add it to the plot 
    # for tick,label in zip(means,ax.get_xticklabels()):
    #     ax.text(means[tick], means[tick], "%.3f" % means[tick], horizontalalignment='center', size='x-small', color='b', weight='semibold')
    
    
    # # group box
    # df = creat_df(dict_demo_group, 'g', column_group)
    # sns.boxplot(x="sampler", y="value", hue='metric',
    #             data=df, linewidth=3, width=0.5)

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



def draw_figure_uniform():

    sns.set(style="darkgrid")

    column_single = ['Benchmark Resources', 'JS-Divergence']
    column_group = ['Unick++', 'Brute-Force', 'QuickSampler']

    # single box
    tb, ts, tsk, ta, total = KL.cmp_mcmc_detail()
    print(ta)

    dict_demo_single = {'Blasted(%d)' % len(tb) : tb, 'S-i(%d)' % len(ts): ts, 'SK(%d)' % len(tsk): tsk, 'Alg(%d)' % len(ta): ta, 'Total(%d)' % len(total) : total}
    df = creat_df(dict_demo_single, 's', column_single)
    sns.boxplot(x="Benchmark Resources", y="JS-Divergence",
                data=df, linewidth=3, width=0.5)


def draw_figure_efficiency():

    sns.set(style="darkgrid")

    column_single = ['Benchmark Resources', r"$\hat{t_{avg}}$(Unick++) / $\hat{t_{avg}}$(QuickSampler)"]
    column_group = ['Unick++', 'Brute-Force', 'QuickSampler']

    # single box

    tb, ts, tsk, ta, total = mcmc_fig.draw_te_star_detail()

    dict_demo_single = {'Blasted(%d)' % len(tb) : tb, 'S-i(%d)' % len(ts): ts, 'SK(%d)' % len(tsk): tsk, 'Alg(%d)' % len(ta): ta, 'Total(%d)' % len(total) : total}
    df = creat_df(dict_demo_single, 's', column_single)
    sns.boxplot(x="Benchmark Resources", y=r"$\hat{t_{avg}}$(Unick++) / $\hat{t_{avg}}$(QuickSampler)",
                data=df, linewidth=3, width=0.5)



def save_fig_new():
    pdf = PdfPages('box_uniform' + '.pdf')
    draw_figure_uniform()

    # pdf = PdfPages('box_efficiency' + '.pdf')
    # draw_figure_efficiency()

    pdf.savefig()
    plt.show()
    plt.close()
    pdf.close()




if __name__ == '__main__':
    # save_figure('boxplot')
    save_fig_new()