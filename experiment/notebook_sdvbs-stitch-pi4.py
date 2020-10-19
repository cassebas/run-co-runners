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
    fig, ax = plt.subplots(1,1, figsize=(15,8))
    ax.bar(df['offset'], df['slowdown'], color='red', edgecolor='black', label='Slowdown', alpha=0.5, width=0.75, yerr=(df['slowdown']-df['slowdown_lo']), capsize=5)
    ax.set_xlabel('offset', fontsize=24)
    ax.set_ylabel('slowdown factor', fontsize=24)
    ax.set_xticks(df['offset'])
    ax.set_xticklabels(df['offset'], fontsize=16)
    ax.set_ylim([1, ylim])
    ax.legend(loc='upper left', fontsize=20)


g = 'report/data/*.csv'
filenames = glob.glob(g)
flist = list(set(filenames))
flist.sort()
regex = re.compile(r'^.*cyclesdata-CIRCLE_PI4_BENCH_STITCH_([^-]*).*$')
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

# # SD-VBS stitch --- Raspberry Pi 4

# ## SD-VBS stitch --- 1 core

f='slowdown-factors-sdvbs-stitch_pi4-20201019.csv'
df = pd.read_csv(f, sep=' ')
# Show overview of the experiments with one label
df = df[df['cores'] == 1]
# Drop one of the labels, for 1 core both labels are the same
df = df.drop(labels=['cores', 'label1core', 'mean1core', 'offset', 'slowdown', 'slowdown_wcet', 'wcet1core'], axis=1)
df

# ## SD-VBS stitch --- 4 cores (complete attack)

f='slowdown-factors-sdvbs-stitch_pi4-20201019.csv'
df = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df = df[df['cores'] > 1]
# Drop the offsets > 1
df = df[df['offset'] == 0]
df = df[df['label'] != 'CIRCLE_PI4_BENCH_SDVBS_STITCH_CORES4_MEMORYPROFILE_INPUTSIZE100']
# Drop the labels, not necessary here
df = df.drop(labels=['label', 'label1core'], axis=1)
df['slowdown_hi'] = df['confidence_hi'] / df['mean1core']
df['slowdown_lo'] = df['confidence_lo'] / df['mean1core']
df

# # SD-VBS stitch --- 4 cores (Memory profile)

f='slowdown-factors-sdvbs-stitch_pi4-20201019.csv'
df = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df = df[df['cores'] > 1]
df = df[df['label'] == 'CIRCLE_PI4_BENCH_SDVBS_STITCH_CORES4_MEMORYPROFILE_INPUTSIZE100']
# Drop the labels, not necessary here
df = df.drop(labels=['label', 'label1core'], axis=1)
df['slowdown_hi'] = df['confidence_hi'] / df['mean1core']
df['slowdown_lo'] = df['confidence_lo'] / df['mean1core']
df

df100 = df[df['inputsize'] == 100]
df100_4 = df100[df100['cores'] == 4]
df100_4 = df100[df100['offset'] <= 20]
df100_4 = df100_4.astype({'offset': 'int32'})
create_bar_plot(df100_4, 'SD-VBS stitch on core 0 and linear array write on cores 1,2 and 3 --- inputsize 100', 1.075)
df100_4
plt.savefig('/home/caspar/git/RTS-thesis/report/img/stitch-memoryprofile.png')


