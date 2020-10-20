# -*- coding: utf-8 -*-
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
import matplotlib.pyplot as plt
import glob
import re


def create_bar_plot(df, title, ylim):
    fig, ax = plt.subplots(1,1, figsize=(15,6))
    ax.bar(df['offset'], df['slowdown'], color='red', edgecolor='black', label='Slowdown', alpha=0.5, width=0.75, yerr=(df['slowdown']-df['slowdown_lo']), capsize=5)
    ax.set_xlabel('offset', fontsize=24)
    ax.set_ylabel('slowdown factor', fontsize=24)
    ax.set_xticks(df['offset'])
    ax.set_xticklabels(df['offset'], fontsize=16)
    ax.set_ylim([1, ylim])
    ax.legend(loc='upper left', fontsize=20)


def autolabel(ax, bars):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{:.3}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 3, height),
                    xytext=(5, 5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=20)


g = 'report/data/*.csv'
filenames = glob.glob(g)
flist = list(set(filenames))
flist.sort()
regex = re.compile(r'^.*cyclesdata-CIRCLE_PI4_BENCH_MÄLARDALEN_MATMULT_([^-]*).*$')
for f in flist:
    m = regex.match(f)
    if m:
        label = m.group(1)
        df = pd.read_csv(f, sep=' ')
        df = df[df['core'] == 0]
        for offset in range(0, 1):
            df_offset = df[df['offset'] == offset]
            if len(df_offset.index) > 0:
                maximum = df_offset['cycles'].max()
                median = df_offset['cycles'].median()
                print('Experiment:{}\tWCET:{:10.0f}\t\tMedian:{:10.0f}\tFactor:{:8.3f}\toffset:{}'.format(label, maximum, median, maximum/median, offset))

# # Mälardalen matrix multiplication --- Raspberry Pi 4

# ## Mälardalen matrix multiplication --- 1 core

f='slowdown-factors-malardalen-matmult_pi4-20201018.csv'
df = pd.read_csv(f, sep=' ')
# Show overview of the experiments with one label
df = df[df['cores'] == 1]
# Drop one of the labels, for 1 core both labels are the same
df = df.drop(labels=['cores', 'label1core', 'mean1core', 'offset', 'slowdown', 'slowdown_wcet', 'wcet1core'], axis=1)
df

# ## Mälardalen matrix multiplication --- multiple cores

f='slowdown-factors-malardalen-matmult_pi4-20201018.csv'
df = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df = df[df['cores'] > 1]
# Drop the labels, not necessary here
#df = df.drop(labels=['label', 'label1core'], axis=1)
df['slowdown_hi'] = df['confidence_hi'] / df['mean1core']
df['slowdown_lo'] = df['confidence_lo'] / df['mean1core']
df

# ## Inputsize 20, 4 cores

df20 = df[df['inputsize'] == 20]
create_bar_plot(df20, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 20', 2)
df20

# ## Inputsize 50, 4 cores

df50 = df[df['inputsize'] == 50]
create_bar_plot(df50, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 50', 2)
df50

# ## Inputsize 80, 4 cores

df80 = df[df['inputsize'] == 80]
create_bar_plot(df80, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 80', 1.2)
df80

# ## Inputsize 90, 4 cores

df90 = df[df['inputsize'] == 90]
create_bar_plot(df90, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 90', 1.2)
df90

# ## Inputsize 100, 2 cores

df100 = df[df['inputsize'] == 100]
# Snip the experiments with memory profile
df100 = df100[df100['label'] != 'CIRCLE_PI4_BENCH_SDVBS_STITCH_CORES4_MEMORYPROFILE_INPUTSIZE100']
df100_2 = df100[df100['cores'] == 2]
create_bar_plot(df100_2, 'Mälardalen matmult on core 0 and linear array write on core 1 --- inputsize 100', 1.45)
df100_2

# ## Inputsize 100, 3 cores

df100 = df[df['inputsize'] == 100]
df100_3 = df100[df100['cores'] == 3]
create_bar_plot(df100_3, 'Mälardalen matmult on core 0 and linear array write on cores 1,2 --- inputsize 100', 1.6)
df100_3

# # Inputsize 100, 4 cores

df100 = df[df['inputsize'] == 100]
df100_4 = df100[df100['cores'] == 4]
create_bar_plot(df100_4, 'Mälardalen matmult on core 0 and linear array write on cores 1,2 and 3 --- inputsize 100', 1.8)
df100_4

# # Staircase with increasing offset and increasingly less contention

# +
index = np.arange(11)
fig, ax = plt.subplots(1, 1, sharey=True, figsize=(16,6))
barwidth = 0.3

bars1 = ax.bar(df100_2['offset']-barwidth, df100_2['slowdown'], label='Slowdown for 2 cores: 1 task, 1 co-runner',
               alpha=0.5, width=barwidth, color='green', edgecolor='black',
               yerr=(df100_2['slowdown']-df100_2['slowdown_lo']), capsize=5)

bars2 = ax.bar(df100_3['offset'], df100_3['slowdown'], label='Slowdown for 3 cores: 1 task, 2 co-runners',
               alpha=0.5, width=barwidth, color='blue', edgecolor='black',
               yerr=(df100_3['slowdown']-df100_3['slowdown_lo']), capsize=5)

bars3 = ax.bar(df100_4['offset']+barwidth, df100_4['slowdown'], label='Slowdown for 4 cores: 1 task, 3 co-runners',
               alpha=0.5, width=barwidth, color='red', edgecolor='black',
               yerr=(df100_4['slowdown']-df100_4['slowdown_lo']), capsize=5)

ax.legend(fontsize=18)
ax.set_xlabel('Offset', fontsize=24)
ax.set_ylabel('Slowdown factor', fontsize=24)
ax.set_xticks(index)
ax.set_ylim([1.0, 1.7])
ax.set_xticklabels(index, fontsize=24)
#ax.tick_params(labelrotation=45)
#autolabel(ax, bars1)
#autolabel(ax, bars2)
#autolabel(ax, bars3)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/report/img/matmult-staircase-bars-pi4.png')
# -

# # Inputsize 120, 4 cores

df120 = df[df['inputsize'] == 120]
df120_4 = df120[df120['cores'] == 4]
create_bar_plot(df120_4, 'Mälardalen matmult on core 0 and linear array write on cores 1,2 and 3 --- inputsize 120', 1.3)
df120_4

# # Mälardalen matmult --- 4 cores (Memory profile)

f='slowdown-factors-malardalen-matmult_pi4-20201019.csv'
dfs = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
dfs = dfs[dfs['cores'] > 1]
dfs = dfs[dfs['label'] == 'CIRCLE_PI4_BENCH_MÄLARDALEN_MATMULT_CORES4_MEMORYPROFILE_INPUTSIZE100']
# Drop the labels, not necessary here
dfs = dfs.drop(labels=['label', 'label1core'], axis=1)
dfs['slowdown_hi'] = dfs['confidence_hi'] / dfs['mean1core']
dfs['slowdown_lo'] = dfs['confidence_lo'] / dfs['mean1core']
dfs

df100s = dfs[dfs['inputsize'] == 100]
df100_4s = df100s[df100s['cores'] == 4]
df100_4s = df100s[df100s['offset'] <= 20]
df100_4s = df100_4s.astype({'offset': 'int32'})
create_bar_plot(df100_4s, 'Mälardalen matmult on core 0 and linear array write on cores 1,2 and 3 --- inputsize 100', 1.09)
df100_4s
plt.savefig('/home/caspar/git/RTS-thesis/report/img/matmult-memoryprofile.png')


