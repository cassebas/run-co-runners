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
import glob
from itertools import combinations
from itertools import combinations_with_replacement
from itertools import permutations
from itertools import product
import re


def create_bar_plot(df, title):
    fig, ax = plt.subplots(1,1, figsize=(10,5))
    ax.bar(df['offset'], df['slowdown'], label='Slowdown', alpha=0.5, width=0.5, yerr=(df['slowdown']-df['slowdown_lo']))
    ax.set_xlabel('offset')
    ax.set_ylabel('slowdown factor')
    ax.set_ylim([1, 3])
    ax.legend(loc='upper left', fontsize=12)
    plt.title(title)


g = 'report/data/*.csv'
filenames = glob.glob(g)
flist = list(set(filenames))
flist.sort()
regex = re.compile(r'^.*cyclesdata-XRTOS_PI3_BENCH_DISPARITY_([^-]*).*$')
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

# ## SD-VBS disparity --- 1 core

f='slowdown-factors-sdvbsdisparity-pi3.csv'
df = pd.read_csv(f, sep=' ')
# Show overview of the experiments with one label
df = df[df['cores'] == 1]
# Drop one of the labels, for 1 core both labels are the same
df = df.drop(labels=['cores', 'label1core', 'mean1core', 'offset', 'slowdown', 'slowdown_wcet', 'wcet1core'], axis=1)
df

# ## SD-VBS disparity --- multiple cores

f='slowdown-factors-sdvbsdisparity-pi3.csv'
df_slowdown = pd.read_csv(f, sep=' ')
# Delete the experiments with 1 core, slowdown factor with absense of co-runners is meaningless
df_slowdown = df_slowdown[df_slowdown['cores'] > 1]
# Drop the labels, not necessary here
df_slowdown = df_slowdown.drop(labels=['label1core'], axis=1)
df_slowdown['slowdown_hi'] = df_slowdown['confidence_hi'] / df_slowdown['mean1core']
df_slowdown['slowdown_lo'] = df_slowdown['confidence_lo'] / df_slowdown['mean1core']
df_slowdown

# ## Inputsize 32, 4 cores

df32 = df_slowdown[df_slowdown['inputsize'] == 32]
create_bar_plot(df32, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 32')
df32

# ## Inputsize 64, 4 cores

df64 = df_slowdown[df_slowdown['inputsize'] == 64]
create_bar_plot(df64, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 64')
df64

# ## Inputsize 96, 4 cores

df96 = df_slowdown[df_slowdown['inputsize'] == 96]
create_bar_plot(df96, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 96')
df96

df128 = df_slowdown[df_slowdown['inputsize'] == 128]
create_bar_plot(df128, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 128')
df128

# ## Inputsize 160, 4 cores

df160 = df_slowdown[df_slowdown['inputsize'] == 160]
create_bar_plot(df160, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 160')
df160

# ## Inputsize 196, 4 cores

df192 = df_slowdown[df_slowdown['inputsize'] == 192]
create_bar_plot(df192, 'SD-VBS disparity on core 0 and linear array write on cores 1,2,3 --- inputsize 192')
df192

# # Bus access and cycles ratio

# Bus access: 0x19
# Bus cycles: 0x1D
bus_access = '0x19'
bus_cycles = '0x1d'

# Read events data for disparity --- 1 core
f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES1_INPUTSIZE64-cores1-configseries3-configbench1-offset0.csv'
df = pd.read_csv(f, sep=' ')
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')

f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE64-cores4-configseries3111-configbench1222-offset0.csv'
df = pd.read_csv(f, sep=' ')
df = df[df['core'] == 0]
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')

# ### Input size 96

# Read events data for disparity --- 1 core
f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES1_INPUTSIZE96-cores1-configseries3-configbench1-offset0.csv'
df = pd.read_csv(f, sep=' ')
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')

f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE96-cores4-configseries3111-configbench1222-offset0.csv'
df = pd.read_csv(f, sep=' ')
df = df[df['core'] == 0]
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')

# ### Input size 128

# Read events data for disparity --- 1 core
f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES1_INPUTSIZE128-cores1-configseries3-configbench1-offset0.csv'
df = pd.read_csv(f, sep=' ')
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')

f = 'report/data/eventsdata-XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE128-cores4-configseries3111-configbench1222-offset0.csv'
df = pd.read_csv(f, sep=' ')
df = df[df['core'] == 0]
df1 = df[df['eventtype'] == bus_access]
df2 = df[df['eventtype'] == bus_cycles]
mean1 = df1['eventcount'].median()
mean2 = df2['eventcount'].median()
print(f'Ratio of bus cycles per bus access is {mean2/mean1}')
df

# # Bar charts for disparity

# +
df_slowdown0 = df_slowdown[df_slowdown['offset'] == 0]
df_slowdown0 = df_slowdown0.set_index(keys=['label'])

cores = range(1,5)
attacks = ['readattack linear', 'readattack random', 'writeattack linear', 'writeattack random']
disparity32lst = [
    [1, 
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE32', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE32', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE32', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE32', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE32', 'slowdown']]]
disparity64lst = [
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE64', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE64', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE64', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE64', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE64', 'slowdown']]]
disparity96lst = [
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE96', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE96', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE96', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE96', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE96', 'slowdown']]]
disparity128lst = [
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE128', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE128', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE128', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE128', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE128', 'slowdown']]]
disparity160lst = [
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE160', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE160', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE160', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE160', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE160', 'slowdown']]]
disparity192lst = [
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK1_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK1_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK1_INPUTSIZE192', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_READATTACK2_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_READATTACK2_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_READATTACK2_INPUTSIZE192', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK1_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK1_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK1_INPUTSIZE192', 'slowdown']],
    [1,
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES2_WRITEATTACK2_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES3_WRITEATTACK2_INPUTSIZE192', 'slowdown'],
     df_slowdown0.loc['XRTOS_PI3_BENCH_DISPARITY_CORES4_WRITEATTACK2_INPUTSIZE192', 'slowdown']]]

disparity32 = pd.DataFrame(disparity32lst)
disparity32 = disparity32.transpose()
disparity32.index = cores
disparity32.columns = attacks

disparity64 = pd.DataFrame(disparity64lst)
disparity64 = disparity64.transpose()
disparity64.index = cores
disparity64.columns = attacks

disparity96 = pd.DataFrame(disparity96lst)
disparity96 = disparity96.transpose()
disparity96.index = cores
disparity96.columns = attacks

disparity128 = pd.DataFrame(disparity128lst)
disparity128 = disparity128.transpose()
disparity128.index = cores
disparity128.columns = attacks

disparity160 = pd.DataFrame(disparity160lst)
disparity160 = disparity160.transpose()
disparity160.index = cores
disparity160.columns = attacks

disparity192 = pd.DataFrame(disparity192lst)
disparity192 = disparity192.transpose()
disparity192.index = cores
disparity192.columns = attacks
# -

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15, 8))
ax.set_title('Disparity + linear array access', fontsize=20)
ax.set_xticks(cores)
ax.plot(disparity32[attacks[0]], label='Linear array access, disparity 32x32', marker='o')
ax.plot(disparity64[attacks[0]], label='Linear array access, disparity 64x64', marker='o')
ax.plot(disparity96[attacks[0]], label='Linear array access, disparity 96x96', marker='o')
ax.plot(disparity128[attacks[0]], label='Linear array access, disparity 128x128', marker='o')
ax.plot(disparity160[attacks[0]], label='Linear array access, disparity 160x160', marker='o')
ax.plot(disparity192[attacks[0]], label='Linear array access, disparity 192x192', marker='o')
ax.set_xlabel('Number of cores', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.legend(loc=0, fontsize=14)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-lineararrayaccess.png')

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15, 8))
ax.set_xticks(cores)
ax.set_title('Disparity + random array access', fontsize=20)
ax.plot(disparity32[attacks[1]], label='Random array access, disparity 32x32', marker='o')
ax.plot(disparity64[attacks[1]], label='Random array access, disparity 64x64', marker='o')
ax.plot(disparity96[attacks[1]], label='Random array access, disparity 96x96', marker='o')
ax.plot(disparity128[attacks[1]], label='Random array access, disparity 128x128', marker='o')
ax.plot(disparity160[attacks[1]], label='Random array access, disparity 160x160', marker='o')
ax.plot(disparity192[attacks[1]], label='Random array access, disparity 192x192', marker='o')
ax.set_xlabel('Number of cores', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.legend(loc=0, fontsize=14)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-randomarrayaccess.png')

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15, 8))
ax.set_xticks(cores)
ax.set_title('Disparity + linear array write', fontsize=20)
ax.plot(disparity32[attacks[2]], label='Linear array write, disparity 32x32', marker='o')
ax.plot(disparity64[attacks[2]], label='Linear array write, disparity 64x64', marker='o')
ax.plot(disparity96[attacks[2]], label='Linear array write, disparity 96x96', marker='o')
ax.plot(disparity128[attacks[2]], label='Linear array write, disparity 128x128', marker='o')
ax.plot(disparity160[attacks[2]], label='Linear array write, disparity 160x160', marker='o')
ax.plot(disparity192[attacks[2]], label='Linear array write, disparity 192x192', marker='o')
ax.set_xlabel('Number of cores', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.legend(loc=0, fontsize=14)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-lineararraywrite.png')

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15, 8))
ax.set_xticks(cores)
ax.set_title('Disparity + random array write', fontsize=20)
ax.plot(disparity32[attacks[3]], label='Random array write, disparity 32x32', marker='o')
ax.plot(disparity64[attacks[3]], label='Random array write, disparity 64x64', marker='o')
ax.plot(disparity96[attacks[3]], label='Random array write, disparity 96x96', marker='o')
ax.plot(disparity128[attacks[3]], label='Random array write, disparity 128x128', marker='o')
ax.plot(disparity160[attacks[3]], label='Random array write, disparity 160x160', marker='o')
ax.plot(disparity192[attacks[3]], label='Random array write, disparity 192x192', marker='o')
ax.set_xlabel('Number of cores', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.legend(loc=0, fontsize=14)
plt.savefig('disparity-randomarraywrite')
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-randomarraywrite.png')

mem_sizes = ['32x32', '64x64', '96x96', '128x128', '160x160', '192x192']
slow_down = []
for i in range(4):
    slow_down.append([disparity32.loc[4, attacks[i]],
                      disparity64.loc[4, attacks[i]],
                      disparity96.loc[4, attacks[i]],
                      disparity128.loc[4, attacks[i]],
                      disparity160.loc[4, attacks[i]],
                      disparity192.loc[4, attacks[i]]])

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(10, 5))
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.bar(mem_sizes, slow_down[0], align='center', alpha=0.5, width=0.75)
ax.set_title('Disparity: Linear read attack on 4 cores', fontsize=20)
ax.set_xticks(mem_sizes)
ax.tick_params(labelrotation=45)

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(10, 5))
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.bar(mem_sizes, slow_down[1], align='center', alpha=0.5, width=0.75)
ax.set_title('Disparity: Random read attack on 4 cores', fontsize=20)
ax.set_xticks(mem_sizes)
ax.tick_params(labelrotation=45)

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(10, 5))
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.bar(mem_sizes, slow_down[2], align='center', alpha=0.5, width=0.75)
ax.set_title('Disparity: Linear write attack on 4 cores', fontsize=20)
ax.set_xticks(mem_sizes)
ax.tick_params(labelrotation=45)

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(10, 5))
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.bar(mem_sizes, slow_down[3], align='center', alpha=0.5, width=0.75)
ax.set_title('Disparity: Random write attack on 4 cores', fontsize=20)
ax.set_xticks(mem_sizes)
ax.tick_params(labelrotation=45)


# +
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

mem_sizes = ['32x32', '64x64', '96x96', '128x128', '160x160', '192x192']
index = np.arange(len(mem_sizes))
y_ticks = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
width = 0.3
# -

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15,6))
slowdown = []
for i in range(2, 5):
    slowdown.append([disparity32.loc[i, attacks[0]],
                     disparity64.loc[i, attacks[0]],
                     disparity96.loc[i, attacks[0]],
                     disparity128.loc[i, attacks[0]],
                     disparity160.loc[i, attacks[0]],
                     disparity192.loc[i, attacks[0]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='2 cores')
bars2 = ax.bar(index, slowdown[1], width, label='3 cores')
bars3 = ax.bar(index + width, slowdown[2], width, label='4 cores')
ax.legend(fontsize=18)
# ax.set_title('Disparity + Linear array access co-runners', fontsize=20)
ax.set_xlabel('Input size', fontsize=24)
ax.set_ylabel('Slowdown factor', fontsize=24)
ax.set_xticks(index)
ax.set_ylim([1.0, 2.0])
ax.set_xticklabels(mem_sizes, fontsize=20)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)
autolabel(ax, bars3)
fig.tight_layout()
plt.savefig('/home/caspar/local/sandbox/git/RTS-thesis/report/img/disparity-lineararrayaccess-bars.png')

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15,6))
slowdown = []
for i in range(2, 5):
    slowdown.append([disparity32.loc[i, attacks[1]],
                     disparity64.loc[i, attacks[1]],
                     disparity96.loc[i, attacks[1]],
                     disparity128.loc[i, attacks[1]],
                     disparity160.loc[i, attacks[1]],
                     disparity192.loc[i, attacks[1]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='2 cores')
bars2 = ax.bar(index, slowdown[1], width, label='3 cores')
bars3 = ax.bar(index + width, slowdown[2], width, label='4 cores')
ax.legend(fontsize=14)
ax.set_title('Disparity + Random array access co-runners', fontsize=20)
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.set_xticks(index)
ax.set_ylim([1.0, 2.0])
ax.set_xticklabels(mem_sizes, fontsize=14)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)
autolabel(ax, bars3)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-randomarrayaccess-bars.png')

mem_sizes = ['32x32', '64x64', '96x96', '128x128', '160x160', '192x192']
index = np.arange(len(mem_sizes))
width = 0.3

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15,8))
slowdown = []
for i in range(2, 5):
    slowdown.append([disparity32.loc[i, attacks[2]],
                     disparity64.loc[i, attacks[2]],
                     disparity96.loc[i, attacks[2]],
                     disparity128.loc[i, attacks[2]],
                     disparity160.loc[i, attacks[2]],
                     disparity192.loc[i, attacks[2]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='2 cores: 1 task, 1 co-runner')
bars2 = ax.bar(index, slowdown[1], width, label='3 cores: 1 task, 2 co-runners')
bars3 = ax.bar(index + width, slowdown[2], width, label='4 cores: 1 task, 3 co-runners')
ax.legend(fontsize=20)
# ax.set_title('Disparity + Linear array write co-runners', fontsize=28)
ax.set_xlabel('Input size', fontsize=28)
ax.set_ylabel('Slowdown factor', fontsize=24)
ax.set_ylim([1.0, 95.0])
ax.set_xticks(index)
ax.set_xticklabels(mem_sizes, fontsize=22)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)
autolabel(ax, bars3)
fig.tight_layout()
plt.savefig('/home/caspar/local/sandbox/git/RTS-thesis/report/img/disparity-lineararraywrite-bars.png')

fig, ax = plt.subplots(1, 1, sharey=True, figsize=(15,6))
slowdown = []
for i in range(2, 5):
    slowdown.append([disparity32.loc[i, attacks[3]],
                     disparity64.loc[i, attacks[3]],
                     disparity96.loc[i, attacks[3]],
                     disparity128.loc[i, attacks[3]],
                     disparity160.loc[i, attacks[3]],
                     disparity192.loc[i, attacks[3]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='2 cores')
bars2 = ax.bar(index, slowdown[1], width, label='3 cores')
bars3 = ax.bar(index + width, slowdown[2], width, label='4 cores')
ax.legend(fontsize=14)
ax.set_title('Disparity + Random array write co-runners', fontsize=20)
ax.set_xlabel('Input size', fontsize=18)
ax.set_ylabel('Slowdown factor', fontsize=18)
ax.set_ylim([1.0, 75.0])
ax.set_xticks(index)
ax.set_xticklabels(mem_sizes, fontsize=14)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)
autolabel(ax, bars3)
fig.tight_layout()
plt.savefig('/home/caspar/git/RTS-thesis/talks/midterm-20200701/img/disparity-randomarraywrite-bars.png')

mem_sizes = ['32x32', '64x64', '96x96', '128x128', '160x160', '192x192']
index = np.arange(len(mem_sizes))
width = 0.4

# +
fig, ax = plt.subplots(figsize=(12,8))
slowdown = []
for i in range(2, 4):
    slowdown.append([disparity32.loc[2, attacks[i]],
                     disparity64.loc[2, attacks[i]],
                     disparity96.loc[2, attacks[i]],
                     disparity128.loc[2, attacks[i]],
                     disparity160.loc[2, attacks[i]],
                     disparity192.loc[2, attacks[i]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='Linear write attack')
bars2 = ax.bar(index, slowdown[1], width, label='Random write attack')

ax.legend()
ax.set_title('Write attack - 2 cores')
ax.set_xlabel('Input size')
ax.set_ylabel('Slowdown factor')
ax.set_xticks(index)
ax.set_xticklabels(mem_sizes)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)

# +
fig, ax = plt.subplots(figsize=(12,8))
slowdown = []
for i in range(2, 4):
    slowdown.append([disparity32.loc[3, attacks[i]],
                     disparity64.loc[3, attacks[i]],
                     disparity96.loc[3, attacks[i]],
                     disparity128.loc[3, attacks[i]],
                     disparity160.loc[3, attacks[i]],
                     disparity192.loc[3, attacks[i]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='Linear write attack')
bars2 = ax.bar(index, slowdown[1], width, label='Random write attack')

ax.legend()
ax.set_title('Write attack - 3 cores')
ax.set_xlabel('Input size')
ax.set_xticks(index)
ax.set_xticklabels(mem_sizes)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)

# +
fig, ax = plt.subplots(figsize=(12,8))
slowdown = []
for i in range(2, 4):
    slowdown.append([disparity32.loc[4, attacks[i]],
                     disparity64.loc[4, attacks[i]],
                     disparity96.loc[4, attacks[i]],
                     disparity128.loc[4, attacks[i]],
                     disparity160.loc[4, attacks[i]],
                     disparity192.loc[4, attacks[i]]])
bars1 = ax.bar(index - width, slowdown[0], width, label='Linear write attack')
bars2 = ax.bar(index, slowdown[1], width, label='Random write attack')

ax.legend()
ax.set_title('Write attack - 4 cores')
ax.set_xlabel('Input size')
ax.set_xticks(index)
ax.set_xticklabels(mem_sizes)
ax.tick_params(labelrotation=45)
autolabel(ax, bars1)
autolabel(ax, bars2)


fig.suptitle('Disparity benchmark Write attacks')
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
