# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt

boxprops = dict(linestyle='-', linewidth=3, color='k')
medianprops = dict(linestyle='-', linewidth=3, color='k')
def set_boxplot_linewidth(bp, linewidth=3):
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]
    [[item.set_linewidth(linewidth) for item in bp[key]] for key in bp.keys()]


# +
from matplotlib import rcParams
labelsize = 32
rcParams['xtick.labelsize'] = labelsize
rcParams['ytick.labelsize'] = labelsize

bsort1_2000 = pd.read_csv('hypothesis1/cyclesdata-BENCH1_2000-core1-configseries2-configbench1-offset0.csv', sep=' ')
bsort1444_2000 = pd.read_csv('hypothesis1/cyclesdata-BENCH1444_2000-core4-configseries2111-configbench1222-offset0.csv', sep=' ')
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(12,12))
xlab1 = ax[0].set_xlabel('run in isolation', fontsize=40, color='green')
xlab2 = ax[1].set_xlabel('with co-runners', fontsize=40, color='red')
maximum = [0, 0]
for i, df in enumerate([bsort1_2000, bsort1444_2000]):
    df = df.loc[df['core'] == 0]
    maximum[i] = df['cycles'].max()
    boxplot = df.boxplot(column=['cycles'], ax=ax[i], return_type='dict')
    set_boxplot_linewidth(boxplot, linewidth=4)

plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/bsort2000-boxplot.png', bbox_inches='tight')
print('The WCET of running 4 cores compared to 1 core is {} times slower'.format(maximum[1]/maximum[0]))
# -

# Calculate the Mann-Whitney U test
a = bsort1_2000['cycles']
b = bsort1444_2000.loc[bsort1444_2000['core'] == 0]['cycles']
t, p = ttest_ind(b, a, equal_var=False)
stat, p = mannwhitneyu(a, b)
alpha = 0.05
print('The calculated statistic is {}.'.format(stat))
print('The calculated p-value is {}.'.format(p))
if p < alpha:
    # enough evidence to reject H0
    print('Based on the Mann-Whitney U test with stat={} and p={}, we can reject the Null-hypothesis'.format(stat, p))
else:
    print('Based on the Mann-Whitney U test with stat={} and p={}, we cannot reject the Null-hypothesis'.format(stat, p))

# +
from matplotlib import rcParams
labelsize = 32
rcParams['xtick.labelsize'] = labelsize
rcParams['ytick.labelsize'] = labelsize

bsort1_8000 = pd.read_csv('hypothesis1/cyclesdata-BENCH1_8000-core1-configseries2-configbench1-offset0.csv', sep=' ')
bsort1444_8000 = pd.read_csv('hypothesis1/cyclesdata-BENCH1444_8000-core4-configseries2111-configbench1222-offset0.csv', sep=' ')
fig, ax = plt.subplots(1, 2, sharey=True, figsize=(10,8))
xlab1 = ax[0].set_xlabel('run in isolation  ', fontsize=40, color='green')
xlab2 = ax[1].set_xlabel('   with co-runners', fontsize=40, color='red')
max = [0, 0]
for i, df in enumerate([bsort1_8000, bsort1444_8000]):
    df = df.loc[df['core'] == 0]
    max[i] = df['cycles'].max()
    boxplot = df.boxplot(column=['cycles'], ax=ax[i], return_type='dict')
    set_boxplot_linewidth(boxplot, linewidth=4)
    
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/bsort8000-boxplot.png', bbox_inches='tight')
print('The WCET of running 4 cores compared to 1 core is {} times slower'.format(max[1]/max[0]))
# -

# Calculate the student t-test
a = bsort1_8000['cycles']
b = bsort1444_8000.loc[bsort1444_8000['core'] == 0]['cycles']
stat, p = mannwhitneyu(a, b)
alpha = 0.05
print('The calculated statistic is {}.'.format(stat))
print('The calculated p-value is {}.'.format(p))
if p < alpha:
    # enough evidence to reject H0
    print('Based on the Mann-Whitney U test with stat={} and p={}, we can reject the Null-hypothesis'.format(stat, p))
else:
    print('Based on the Mann-Whitney U test with stat={} and p={}, we cannot reject the Null-hypothesis'.format(stat, p))
