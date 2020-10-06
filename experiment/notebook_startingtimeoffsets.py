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

infiles = glob.glob('output/*-cycles.csv')
infiles

# # Mälardalen matmult input size 100x100 on core 0, 1 co-runner
# Below figure shows an experiment with the Mälardalen matrix multiplication benchmark running on core 0. There is one co-runner, which is stressing the memory system by continuously writing to an array.
#
# The experiment is repeated 100 times, each iteration performs the exact same configuration of tasks on cores.
# After 100 iterations, the co-runner's starting time is delayed by 1/10th of the baseline WCET. The same principle is applied after 200 iterations, etc.
# The figure clearly shows the effect of the delayed starting times. After 600 iterations, the delay is greater than the baseline WCET. This results in a 'normal' execution time for the matmult benchmark, since there is no co-runner anymore.

# +
df = pd.read_csv('output/experiments_Mälardalen-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 2)]

fig, ax = plt.subplots(1,2, figsize=(16,5))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration')
ax[0].set_ylabel('number of cycles')
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset')
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen matmult on core 0 and linear array write on core 1')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 2), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.3])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen matmult: 1 linear write co-runner', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
# -

# # Mälardalen matmult input size 100x100 on core 0, 2 co-runners
# Below figure shows an experiment with the Mälardalen matrix multiplication benchmark running on core 0, this time with two co-runners, which are again stressing the memory system by continuously writing to an array.

# + jupyter={"source_hidden": true}
df = pd.read_csv('output/experiments_Mälardalen-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 3)]

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen matmult on core 0 and linear array write on cores 1 and 2')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 3), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 10])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen matmult: 2 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
# -

# # Mälardalen matmult input size 100x100 on core 0, 3 co-runners
# Below figure shows an experiment with the Mälardalen matrix multiplication benchmark running on core 0, this time with three co-runners, which are again stressing the memory system by continuously writing to an array.

# + jupyter={"source_hidden": true}
df = pd.read_csv('output/experiments_Mälardalen-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 4)]

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen matmult on core 0 and linear array write on cores 1, 2 and 3')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 4), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 30])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen matmult: 3 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()

# + [markdown] jupyter={"source_hidden": true}
# # Mälardalen bsort input size 2000 on core 0, 1 co-runner

# + jupyter={"outputs_hidden": true, "source_hidden": true}
df = pd.read_csv('output/experiments_Mälardalen-20200725-5-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[df1['label'] == 'BENCH_MÄLARDALEN_BSORT100_CORES2_WRITEATTACK1_INPUTSIZE2000']

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen bsort on core 0 and linear array write on core 1')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[('BENCH_MÄLARDALEN_BSORT100_CORES2_WRITEATTACK1_INPUTSIZE2000', 2), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.0005])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen bsort: 1 linear write co-runner', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()

# + [markdown] jupyter={"source_hidden": true}
# # Mälardalen bsort input size 2000 on core 0, 2 co-runners

# + jupyter={"outputs_hidden": true, "source_hidden": true}
df = pd.read_csv('output/experiments_Mälardalen-20200725-5-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[df1['label'] == 'BENCH_MÄLARDALEN_BSORT100_CORES3_WRITEATTACK1_INPUTSIZE2000']

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset cores 1 and 2', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen bsort on core 0 and linear array write on cores 1 and 2')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[('BENCH_MÄLARDALEN_BSORT100_CORES3_WRITEATTACK1_INPUTSIZE2000', 3), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.0005])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen bsort: 2 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()

# + [markdown] jupyter={"source_hidden": true}
# # Mälardalen bsort input size 2000 on core 0, 3 co-runners

# + jupyter={"outputs_hidden": true, "source_hidden": true}
df = pd.read_csv('output/experiments_Mälardalen-20200725-5-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[df1['label'] == 'BENCH_MÄLARDALEN_BSORT100_CORES4_WRITEATTACK1_INPUTSIZE2000']

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset cores 1, 2 and 3', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen bsort on core 0 and linear array write on cores 1, 2 and 3')

df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[('BENCH_MÄLARDALEN_BSORT100_CORES4_WRITEATTACK1_INPUTSIZE2000', 4), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.0005])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen bsort: 3 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
# -

# # SD-VBS disparity input size 64x64 on core 0, 1 co-runner
# Below figure shows an experiment with the SD-VBS disparity benchmark running on core 0. There is one co-runner, which is stressing the memory system by continuously writing to an array.
#
# The experiment is repeated 100 times, each iteration performs the exact same configuration of tasks on cores.
# After 100 iterations, the co-runner's starting time is delayed by 1/10th of the baseline WCET. The same principle is applied after 200 iterations, etc.
# The figure clearly shows the effect of the delayed starting times. After 600 iterations, the delay is greater than the baseline WCET. This results in a 'normal' execution time for the disparity benchmark, since there is no co-runner anymore.

# + jupyter={"source_hidden": true}
df = pd.read_csv('output/experiments_SD-VBS-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 2)]

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('SD-VBS disparity on core 0 and linear array write on core 1')

df2 = pd.read_csv('slowdown-factors-sdvbs.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 2), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.5])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('SD-VBS disparity: 1 linear write co-runner', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
# -

# # SD-VBS disparity input size 64x64 on core 0, 2 co-runners
# Below figure shows an experiment with the SD-VBS disparity benchmark running on core 0, this time with two co-runners, which are again stressing the memory system by continuously writing to an array.

# + jupyter={"source_hidden": true}
df = pd.read_csv('output/experiments_SD-VBS-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 3)]

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset cores 1 and 2', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('SD-VBS disparity on core 0 and linear array write on cores 1 and 2')

df2 = pd.read_csv('slowdown-factors-sdvbs.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 3), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 40])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('SD-VBS disparity: 2 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
# -

# # SD-VBS disparity input size 64x64 on core 0, 3 co-runners
# Below figure shows an experiment with the Mälardalen matrix multiplication benchmark running on core 0, this time with three co-runners, which are again stressing the memory system by continuously writing to an array.

# + jupyter={"source_hidden": true}
df = pd.read_csv('output/experiments_SD-VBS-20200725-2-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] < 700)]
df1 = df1[(df1['cores'] == 4)]

fig, ax = plt.subplots(1,2, figsize=(18,6))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration', fontsize=18)
ax[0].set_ylabel('number of cycles', fontsize=18)
ax2.plot(df1['iteration'], df1['offset'], label='offset cores 1, 2 and 3', color='green')
ax2.set_ylabel('starting time offset', fontsize=14)
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('SD-VBS disparity on core 0 and linear array write on cores 1, 2 and 3')

df2 = pd.read_csv('slowdown-factors-sdvbs.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 4), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 75])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('SD-VBS disparity: 3 linear write co-runners', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()

# +
df = pd.read_csv('output/experiments_Mälardalen_matmult_circle_pi4-3-cycles.csv', sep=',')
df1 = df[df['core'] == 0]
df1 = df1[(df1['iteration'] <= 700)]
df1 = df1[(df1['cores'] == 4)]
df1 = df1[(df1['label'] == 'CIRCLE_PI4_BENCH_MÄLARDALEN_MATMULT_CORES4_WRITEATTACK1_INPUTSIZE100')]

fig, ax = plt.subplots(1,2, figsize=(16,5))  # 1 row, 2 columns
ax2 = ax[0].twinx()
ax[0].plot(df1['iteration'], df1['cycles'], label='cycles core 0')
ax[0].set_xlabel('iteration')
ax[0].set_ylabel('number of cycles')
ax2.plot(df1['iteration'], df1['offset'], label='offset core 1', color='green')
ax2.set_ylabel('starting time offset')
ax[0].legend(loc='upper center', fontsize=12)
ax2.legend(loc='right', fontsize=12)
plt.title('Mälardalen matmult on core 0 and linear array write on core 1')

# +
df2 = pd.read_csv('slowdown-factors-malardalen.csv', sep=' ')
df2 = df2[df2['offset'] <= 12]
df2 = df2.set_index(keys=['label', 'cores'])
df2cores = df2.loc[(slice(None), 2), :]
# Select the first label, which in this case should be the write attack 1
label = df2cores.index.get_level_values(0)[1]
df2cores = df2cores.loc[label, :]
offsets = list(df2cores['offset'])

ax[1].set_xlabel('Start time offset', fontsize=18)
ax[1].set_ylabel('Slowdown factor', fontsize=18)
ax[1].set_ylim([1, 1.3])
ax[1].bar(offsets, df2cores['slowdown_factor'], align='center', alpha=0.5, width=0.75)
ax[1].set_title('Mälardalen matmult: 1 linear write co-runner', fontsize=20)
ax[1].set_xticks([0, 2, 4, 6, 8, 10, 12])
ax[1].tick_params(labelrotation=0)
plt.tight_layout()
plt.show()
