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


def create_bar_plot(df, title):
    fig, ax = plt.subplots(1,1, figsize=(10,5))
    ax.bar(df['offset'], df['slowdown'], label='Slowdown', alpha=0.5, width=0.5, yerr=(df['slowdown']-df['slowdown_lo']))
    ax.set_xlabel('offset')
    ax.set_ylabel('slowdown factor')
    ax.set_ylim([1, 2])
    ax.legend(loc='upper left', fontsize=12)
    plt.title(title)


# # Mälardalen matrix multiplication --- Raspberry Pi 4

# ## Mälardalen matrix multiplication --- 1 core

f='slowdown-factors-malardalen-matmult_pi4-20201002.csv'
df = pd.read_csv(f, sep=' ')
# Show overview of the experiments with one label
df = df[df['cores'] == 1]
# Drop one of the labels, for 1 core both labels are the same
df = df.drop(labels=['cores', 'label1core', 'mean1core', 'offset', 'slowdown', 'slowdown_wcet', 'wcet1core'], axis=1)
df

# ## Mälardalen matrix multiplication --- multiple cores

f='slowdown-factors-malardalen-matmult_pi4-20201002.csv'
df = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df = df[df['cores'] > 1]
# Drop the labels, not necessary here
df = df.drop(labels=['label', 'label1core'], axis=1)
df['slowdown_hi'] = df['confidence_hi'] / df['mean1core']
df['slowdown_lo'] = df['confidence_lo'] / df['mean1core']
df

# ## Inputsize 20, 4 cores

df20 = df[df['inputsize'] == 20]
create_bar_plot(df20, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 20')
df20

# ## Inputsize 50, 4 cores

df50 = df[df['inputsize'] == 50]
create_bar_plot(df50, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 50')
df50

# ## Inputsize 80, 4 cores

df80 = df[df['inputsize'] == 80]
create_bar_plot(df80, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 80')
df80

# ## Inputsize 90, 4 cores

df90 = df[df['inputsize'] == 90]
create_bar_plot(df90, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 90')
df90

# ## Inputsize 100, 2 and 3 and 4 cores

df100 = df[df['inputsize'] == 100]
create_bar_plot(df100, 'Mälardalen matmult on core 0 and linear array write on cores 1,2,3 --- inputsize 100')
df100
