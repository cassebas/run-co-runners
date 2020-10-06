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
from os.path import isfile, join
from itertools import combinations
from itertools import combinations_with_replacement
from itertools import permutations
from itertools import product
import scipy
import scikits.bootstrap as bootstrap

# + jupyter={"outputs_hidden": true}
g = 'report/data/*.csv'
filenames = glob.glob(g)
filenames

# +
benchmarks = ['1', '2', '3', '4', '5', '6']
flist = []
for cores in range(1, 5):
    prod = product(benchmarks, repeat=cores)
    for p in prod:
        bench = ''.join(p)
        g = 'report/data/*.csv'.format(cores, bench)
        filenames = glob.glob(g)
        flist += filenames

flist = list(set(flist))
flist.sort()
regex = re.compile(r'^.*cyclesdata-([^-]*).*$')
for f in flist:
    m = regex.match(f)
    if m:
        label = m.group(1)
        df = pd.read_csv(f, sep=' ')
        df = df[df['core'] == 0]
        for offset in range(0, 11):
            df_offset = df[df['offset'] == offset]
            if len(df_offset.index) > 0:
                maximum = df_offset['cycles'].max()
                median = df_offset['cycles'].median()
                print('Experiment:{}\tWCET:{:10.0f}\t\tMedian:{:10.0f}\tFactor:{:8.3f}\toffset:{}'.format(label, maximum, median, maximum/median, offset))
# -

infiles = glob.glob('output/*.csv')
infiles

# +
f='output/experiments_Mälardalen_matmult_circle_pi4-2-cycles.csv'

df = pd.read_csv(f, sep=',')
df = df[(df['label'] == 'CIRCLE_PI4_BENCH_MÄLARDALEN_MATMULT_CORES4_WRITEATTACK1_INPUTSIZE80') |
        (df['label'] == 'CIRCLE_PI4_BENCH_MÄLARDALEN_MATMULT_CORES4_WRITEATTACK1_INPUTSIZE100')]

# Drop rows with 1 core and offset > 0
df = df[(df['cores'] > 1) | (df['offset'] == 0)]
# Drop rows with offset > 10
df = df[df['offset'] <= 10]


pv = pd.pivot_table(df,
                    index=['label', 'cores', 'config_series', 'config_benchmarks', 'offset'],
                    columns=['benchmark', 'core'],
                    values='cycles',
                    aggfunc={'cycles': [np.median,
                                        np.mean,
                                        np.std,
                                        np.max]})
pv = pv.rename(columns={0: 'core0',
                        1: 'core1',
                        2: 'core2',
                        3: 'core3'})

pv.sort_index(inplace=True)
pv.index.get_level_values(0) # cores
pv.index.get_level_values(1) # configuration
pv.index.get_level_values(2) # data assignment
pv.index.get_level_values(3) # alignment pattern

df_tmp = pv.loc[slice(None),
                (slice(None), slice(None), ['core0'])]
df_tmp

# + jupyter={"outputs_hidden": true}
df = pd.read_csv('output/log-20200309.csv')
df
# -

pv = pd.pivot_table(df,
                    index=['cores', 'configuration', 'dassign', 'pattern'],
                    columns=['benchmark', 'core'],
                    values='cycles',
                    aggfunc={'cycles': [np.median, np.std]})
pv = pv.rename(columns={0: 'core0',
                        1: 'core1',
                        2: 'core2',
                        3: 'core3'})
pv.sort_index(inplace=True)
pv
pv.loc[(2, "'44'", "'01'", slice(None)), (slice(None))]
pv.columns.to_series().str.join('-')
#pv.columns

# Output files to temporary directory tmp
output_directory = 'tmp'
#benchmarks = ['malardalenbsort100',
#              'lineararrayaccess',
#              'syntheticbench1',
#              'randomarrayaccess']
    for cores in range(1, 5):
        cidx = ['core'+str(i) for i in range(cores)]
        for config in set(pvs.index.get_level_values(1)):
            for dassign in set(pvs.index.get_level_values(2)):
                pv_summary = pvs.loc[(cores, [config], dassign, slice(None)), (slice(None), slice(None), cidx)]
                pv_summary.dropna(axis=0, how='all', inplace=True)
                pv_summary.dropna(axis=1, how='all', inplace=True)
                if len(pv_summary.index) > 0:
                    print('cidx ={}'.format(cidx))
                    print('config={}, dassign={}'.format(config, dassign))
                    print('length pv_summary={}'.format(len(pv_summary.index)))
                    pv_summary.columns = pv_summary.columns.to_series().str.join('-')
                    output_filename = 'cycles-{}core-config{}-dassign{}.csv'.format(cores, config, dassign)
                    outfile = join(output_directory, output_filename)
                    pv_summary.to_csv(outfile, index=True, sep=' ')
            for pattern in set(pvs.index.get_level_values(3)):
                print('pattern={}'.format(pattern))
                pv_summary = pvs.loc[(cores, [config], slice(None), pattern),
                                     (slice(None), slice(None), cidx)]
                pv_summary.dropna(axis=0, how='all', inplace=True)
                pv_summary.dropna(axis=1, how='all', inplace=True)
                if len(pv_summary.index) > 0:
                    print('cidx ={}'.format(cidx))
                    print('config={}, pattern={}'.format(config, pattern))
                    print('length pv_summary={}'.format(len(pv_summary.index)))
                    pv_summary.columns = pv_summary.columns.to_series().str.join('-')
                    output_filename = 'cycles-{}core-config{}-pattern{}.csv'.format(cores, config, pattern)
                    outfile = join(output_directory, output_filename)
                    pv_summary.to_csv(outfile, index=True, sep=' ')


benchmarks = ['malardalenbsort100',
              'lineararrayaccess',
              'syntheticbench1',
              'randomarrayaccess']
pvs_cb = pvs.loc[2, (slice(None), benchmarks, ['core0', 'core1'])]
print('malardalenbsort100' in pvs_cb.columns.get_level_values(1))
print('syntheticbench1' in pvs_cb.columns.get_level_values(1))
#pvs_cb
#pvs_tmp = pvs_cb.loc[:, (slice(None), benchmarks[2], ['core0', 'core1'])].dropna(how='all')
#pvs_tmp

pvs1 = pvs.loc[1, (slice(None), 'randomarrayaccess', 'core0')]
pvs1.dropna(how='all', inplace=True)
pvs1

pvs1.columns = pvs1.columns.to_series().str.join('-')
pvs1

pvs2 = pvs.loc[2, (slice(None), 'lineararrayaccess', ['core0', 'core1'])].dropna(how='any')
pvs2.columns = pvs2.columns.to_series().str.join('-')
pvs2

pvs3 = pvs.loc[3, (slice(None), 'lineararrayaccess', ['core0', 'core1', 'core2'])]
pvs3.dropna(how='any', inplace=True)
pvs3

pvs4 = pvs.loc[4, (slice(None), 'lineararrayaccess', slice(None))]
pvs4.dropna(how='any', inplace=True)
pvs4

pvs2_0 = pvs.loc[2, (slice(None), ['lineararrayaccess','malardalenbsort100'], ['core0', 'core1'])]
pvs2_0.dropna(how='all', inplace=True)
pvs2_0

pvs2_1 = pvs2_0.loc[:, (slice(None), ['lineararrayaccess'], ['core0', 'core1'])].dropna(how='all')
pvs2_1 = pvs2_1[pvs2_1.isnull().any(1)]
pvs2_1 = pvs2_1.loc[:, (slice(None), 'lineararrayaccess', 'core1')]
pvs2_1

pvs2_2 = pvs2_0.loc[:, (slice(None), ['malardalenbsort100'], ['core0', 'core1'])].dropna(how='all')
pvs2_2 = pvs2_2[pvs2_2.isnull().any(1)]
pvs2_2 = pvs2_2.loc[:, (slice(None), 'malardalenbsort100', 'core0')]
pvs2_2

pvs_merge = pd.merge(pvs2_1, pvs2_2, left_index=True, right_index=True)
pvs_merge

# +
pvs2_0 = pvs.loc[2, (slice(None), ['lineararrayaccess','malardalenbsort100'], ['core0', 'core1'])]
pvs2_0.dropna(how='all', inplace=True)

pvs2_3 = pvs2_0.loc[:, (slice(None), 'lineararrayaccess', ['core0', 'core1'])].dropna(how='all')
pvs2_3 = pvs2_3[pvs2_3.isnull().any(1)]
pvs2_3 = pvs2_3.loc[:, (slice(None), 'lineararrayaccess', 'core1')]
print(len(pvs2_3.index))

pvs2_4 = pvs2_0.loc[:, (slice(None), 'malardalenbsort100', ['core0', 'core1'])].dropna(how='all')
pvs2_4 = pvs2_4[pvs2_4.isnull().any(1)]
pvs2_4 = pvs2_4.loc[:, (slice(None), 'malardalenbsort100', 'core0')]
print(len(pvs2_4.index))

pvs_merge = pd.merge(pvs2_3, pvs2_4, left_index=True, right_index=True).dropna(how='any')
if len(pvs_merge.index) > 0:
    print(True)
else:
    print(False)
print(pvs2_3)
# -

pvstmp = pvs.loc[3, (slice(None), ['lineararrayaccess','malardalenbsort100'], ['core0', 'core1', 'core2'])]
pvstmp1 = pvstmp.loc[:, (slice(None), 'lineararrayaccess', ['core0', 'core1', 'core2'])].dropna(how='all')
#pvstmp = pvstmp[pvstmp.isnull().any(1)]
pvstmp1

print(pvs2_3.columns)
print(pvs2_3.index)

pv1 = pd.read_csv('report/data/cycles-2core-malardalenbsort100-lineararrayaccess.csv', sep=' ')
pv1

pv2 = pd.read_csv('report/data/cycles-2core-malardalenbsort100-lineararrayaccess.csv2', sep=' ')
pv2

pv3 = pd.read_csv('report/data/cycles-3core-malardalenbsort100-lineararrayaccess-malardalenbsort100.csv', sep=' ')
pv3

pv4 = pd.read_csv('report/data/cycles-3core-malardalenbsort100-syntheticbench1-malardalenbsort100.csv', sep=' ')
pv4

pv4 = pd.read_csv('report/data/cycles-3core-syntheticbench1.csv', sep=' ')
pv4
