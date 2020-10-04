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

# # Mälardalen matrix multiplication PI 4

f='slowdown-factors-malardalen-matmult_pi4-20201002.csv'
df = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df = df[df['cores'] > 1]
# Drop the labels, not necessary here
df = df.drop(labels=['label', 'label1core'], axis=1)

# ## Inputsize 20

df20 = df[df['inputsize'] == 20]
df20

df50 = df[df['inputsize'] == 50]
df50

df80 = df[df['inputsize'] == 80]
df80

df90 = df[df['inputsize'] == 90]
df90

# ## Inputsize 100

df100 = df[df['inputsize'] == 100]

# ### 2 cores

df100_2cores = df100[df100['cores'] == 2]
df100_2cores

# ### 3 cores

df100_3cores = df100[df100['cores'] == 3]
df100_3cores

# ### 4 cores

df100_4cores = df100[df100['cores'] == 4]
df100_4cores

fig, ax = plt.subplots(1,1, figsize=(10,5))  # 1 row, 2 columns
ax2 = ax.twinx()
ax.bar(df100_4cores['offset'], df100_4cores['wcet'], label='WCET', alpha=0.5, width=0.5)
ax.set_xlabel('offset')
ax.set_ylabel('WCET cycles')
ax.set_ylim([6400000, 8000000])
ax2.plot(df100_4cores['offset'], df100_4cores['slowdown_factor'], label='slowdown', color='green')
ax2.set_ylabel('slowdown factors')
ax.legend(loc='upper left', fontsize=12)
ax2.legend(loc='upper right', fontsize=12)
ax2.set_ylim([1,2])
plt.title('Mälardalen matmult on core 0 and linear array write on cores 1,2,3')
