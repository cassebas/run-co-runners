import click
import click_log
import logging
import glob
import os
# from os.path import basename, isfile, join
from os.path import isfile, join
import subprocess
from subprocess import CalledProcessError
import numpy as np
import pandas as pd
import re
import time
from enum import Enum
# import signal
from threading import Thread
import serial
# from warnings import warn
import sys
import scipy
import scikits.bootstrap as bootstrap


benchmark_list = [
    ['linear array access',
     'linear array write',
     'random array access',
     'random array write'],
    ['malardalen bsort100',
     'malardalen ns',
     'malardalen matmult',
     'fir'],
    ['sd-vbs disparity',
     'sd-vbs mser',
     'sd-vbs svm',
     'sd-vbs stitch']]


logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def remove_quotes(string):
    string = re.sub(r'^\'', '', string)
    string = re.sub(r'\'$', '', string)
    return string


class Fields(Enum):
    NUMBER = 1
    PLATFORM = 2
    RASPBERRYPI = 3
    CONFIG_SERIES = 4
    CONFIG_BENCH = 5
    ENABLE_MMU = 6
    ENABLE_SCREEN = 7
    NO_CACHE_MGMT = 8
    EXP_LABEL = 9
    PMU_CORE0 = 10
    PMU_CORE1 = 11
    PMU_CORE2 = 12
    PMU_CORE3 = 13
    INPUTSIZE_CORE0 = 14
    INPUTSIZE_CORE1 = 15
    INPUTSIZE_CORE2 = 16
    INPUTSIZE_CORE3 = 17
    DELAY_STEP_COUNTDOWN = 18


flds = {
    Fields.NUMBER: 'experiment number',
    Fields.PLATFORM: 'platform',
    Fields.RASPBERRYPI: 'raspberrypi',
    Fields.CONFIG_SERIES: 'benchmark series',
    Fields.CONFIG_BENCH: 'benchmark configuration',
    Fields.ENABLE_MMU: 'enable mmu',
    Fields.ENABLE_SCREEN: 'enable screen',
    Fields.NO_CACHE_MGMT: 'no cache management',
    Fields.EXP_LABEL: 'experiment label',
    Fields.PMU_CORE0: 'pmu core 0',
    Fields.PMU_CORE1: 'pmu core 1',
    Fields.PMU_CORE2: 'pmu core 2',
    Fields.PMU_CORE3: 'pmu core 3',
    Fields.INPUTSIZE_CORE0: 'input size core0',
    Fields.INPUTSIZE_CORE1: 'input size core1',
    Fields.INPUTSIZE_CORE2: 'input size core2',
    Fields.INPUTSIZE_CORE3: 'input size core3',
    Fields.DELAY_STEP_COUNTDOWN: 'delay step countdown',
}


def get_check_inputsize(label, inputsize=None):
    regex = re.compile('^.*_INPUTSIZE([0-9]+)$')
    m = regex.match(label)
    if (m):
        label_inputsize = m.group(1)
        if inputsize is None:
            return label_inputsize
        elif label_inputsize == inputsize:
            return inputsize
        else:
            logger.warning(f'Inputsize {inputsize} is not equal to the ' +
                           f'retrieved from label {label}!')
            return label_inputsize
    else:
        logger.warning(f'Inputsize could not be retrieved from label {label}!')
        logger.warning('Label does not follow format /.*_INPUTSIZE[0-9]+$/')
        return None


def get_experiment_labels(input_file):
    df = pd.read_excel(input_file, skiprows=[0])

    # first pass, extract all 1-core experiments that are baseline
    # to the other experiments
    exp_keys = {}
    exp_mapping = {}
    for idx, row in df.iterrows():
        exp_nr = row[flds[Fields.NUMBER]]
        config_series = row[flds[Fields.CONFIG_SERIES]]
        config_bench = row[flds[Fields.CONFIG_BENCH]]

        # remove quotes from strings (if present)
        config_series = remove_quotes(config_series)
        config_bench = remove_quotes(config_bench)

        if len(config_series) != len(config_bench):
            # Illegal combination of lengths config_series and config_bench,
            # they must be of equal length
            logger.warning('Illegal lengths of series and benchmarks ' +
                           'configuration!')
            logger.warning('Skipping experiment number {}'.format(exp_nr))
            continue

        if len(config_series) == 1:
            # This is a 1-core experiment, remember the experiment by making
            # a hash key that contains the configuration and the parameters
            # of the experiment.
            # This key will be used for matching against the multiple core
            # experiments with the same parameters.
            exp_key = str(config_series) + str(config_bench) + '_'
            exp_key += str(row[flds[Fields.PLATFORM]]) + '_'
            exp_key += str(row[flds[Fields.RASPBERRYPI]]) + '_'
            exp_key += str(row[flds[Fields.ENABLE_MMU]]) + '_'
            exp_key += str(row[flds[Fields.ENABLE_SCREEN]]) + '_'
            exp_key += str(row[flds[Fields.NO_CACHE_MGMT]]) + '_'
            exp_key += str(row[flds[Fields.INPUTSIZE_CORE0]])
            # In the experiments, the experiment label is pre-pended
            # with the platform + raspberry pi version:
            label = (str(row[flds[Fields.PLATFORM]]).upper() + '_PI' +
                     str(row[flds[Fields.RASPBERRYPI]]) + '_' +
                     row[flds[Fields.EXP_LABEL]])
            exp_keys[exp_key] = label

    # second pass, extract all n-core experiments that have co-runners
    for idx, row in df.iterrows():
        config_series = row[flds[Fields.CONFIG_SERIES]]
        config_bench = row[flds[Fields.CONFIG_BENCH]]

        # remove quotes from strings (if present)
        config_series = remove_quotes(config_series)
        config_bench = remove_quotes(config_bench)

        # Retrieve inputsize from label, and verify its correctness with
        # the inputsize present in the Excel sheet
        inputsize = str(row[flds[Fields.INPUTSIZE_CORE0]])
        exp_label = row[flds[Fields.EXP_LABEL]]
        inputsize = get_check_inputsize(exp_label, inputsize)

        # Construct the hash key for matching against the 1-core
        # experiment with the same parameters.
        # Note that the 1-core experiment will also be matched to itself.
        exp_key = str(config_series[0]) + str(config_bench[0]) + '_'
        exp_key += str(row[flds[Fields.PLATFORM]]) + '_'
        exp_key += str(row[flds[Fields.RASPBERRYPI]]) + '_'
        exp_key += str(row[flds[Fields.ENABLE_MMU]]) + '_'
        exp_key += str(row[flds[Fields.ENABLE_SCREEN]]) + '_'
        exp_key += str(row[flds[Fields.NO_CACHE_MGMT]]) + '_'
        exp_key += inputsize
        # In the experiments, the experiment label is pre-pended
        # with the platform + raspberry pi version:
        label = (str(row[flds[Fields.PLATFORM]].upper()) + '_PI' +
                 str(row[flds[Fields.RASPBERRYPI]]) + '_' +
                 row[flds[Fields.EXP_LABEL]])
        if exp_key in exp_keys:
            exp_mapping[label] = exp_keys[exp_key]

    exp_list = []
    for key, val in exp_mapping.items():
        exp_list.append([key, val])
    df_mapping = pd.DataFrame.from_records(exp_list,
                                           columns=['label',
                                                    'label1core'])
    return df_mapping


def get_ci(data):
    # Compute confidence interval
    interval = bootstrap.ci(data,
                            statfunction=scipy.mean,
                            alpha=0.05)
    logger.debug(f'Interval is ({interval[0]}, {interval[1]})')
    return interval


def get_experiment_data(csv_dir, csv_file_prefix):
    df = pd.DataFrame()
    dfs = pd.DataFrame()
    infiles = glob.glob(join(csv_dir, csv_file_prefix + '*-cycles.csv'))
    for f in infiles:
        logger.debug(f'Reading input file {f}')
        df = pd.read_csv(f)
        # Drop rows with 1 core and offset > 0
        df = df[(df['cores'] > 1) | (df['offset'] == 0)]
        # Drop rows with offset > 10
        # NO: do NOT drop these! df = df[df['offset'] <= 10]

        df_pivot = pd.pivot_table(df,
                                  index=['label', 'cores',
                                         'config_series', 'config_benchmarks',
                                         'offset'],
                                  columns=['benchmark', 'core'],
                                  values='cycles',
                                  aggfunc={'cycles': [np.median,
                                                      np.mean,
                                                      np.std,
                                                      np.max]})
        df_pivot = df_pivot.rename(columns={0: 'core0',
                                            1: 'core1',
                                            2: 'core2',
                                            3: 'core3'})
        dfs = pd.concat([dfs, df_pivot])
    dfs.sort_index(inplace=True)
    return dfs


def get_experiment_results(exp_labels, exp_data, data_dir):
    exp_results = pd.DataFrame()

    # Extend the experiments dataframe with result data
    for idx, row in exp_labels.iterrows():
        label = row['label']
        inputsize = get_check_inputsize(label)
        logger.debug(f'Inputsize {inputsize} retrieved from label={label}')
        try:
            df_tmp = exp_data.loc[label,
                                  (slice(None), slice(None), ['core0'])]
            if len(df_tmp.index) > 0:
                cores = df_tmp.index.get_level_values(0)[0]
                config_series = df_tmp.index.get_level_values(1)[0]
                config_bench = df_tmp.index.get_level_values(2)[0]
                # remove quotes from strings (if present)
                config_series = remove_quotes(config_series)
                config_bench = remove_quotes(config_bench)

                benchmarks = [benchmark_list[int(tup[0])-1][int(tup[1])-1]
                              for tup in zip(config_series, config_bench)]
                benchmark = benchmarks[0]

                # strip whitespace from benchmark name
                benchmark = re.sub(r' ', '', benchmark)
                # strip '-' from benchmark name
                benchmark = re.sub(r'-', '', benchmark)
                offset_list = df_tmp.index.get_level_values(3)
                logger.debug('offset list is {}'.format(offset_list))

                for offset in offset_list:
                    df_tmp_offset = df_tmp.loc[(slice(None),
                                                slice(None),
                                                slice(None),
                                                offset),
                                               (slice(None),
                                                [benchmark],
                                                ['core0'])]

                    # To obtain the confidence interval, we now have to
                    # read a different file, containing the data instead of
                    # the summary information we have in df_tmp (it's a pivot
                    # table). The data file is obtained from data_dir
                    try:
                        infile = '{}{}-{}-'.format('cycles', 'data', label)
                        infile += 'cores{}-'.format(cores)
                        infile += 'configseries{}-'.format(config_series)
                        infile += 'configbench{}'.format(config_bench)
                        infile += '-{}{}.csv'.format('offset', offset)
                        infile = join(data_dir, infile)
                        data_df = pd.read_csv(infile, sep=' ')
                        data_df = data_df[data_df['core'] == 0]
                        conf_interval = get_ci(data_df['cycles'])
                    except FileNotFoundError:
                        logger.warning(f'Could not open {infile} for' +
                                       ' computing confidence interval.')
                        conf_interval = (None, None)

                    # dftmp_offset now contains one row, 4 cols
                    # (amax, mean, median, std)
                    print(df_tmp_offset)
                    wcet = df_tmp_offset.iloc[0, 0]
                    mean = df_tmp_offset.iloc[0, 1]
                    median = df_tmp_offset.iloc[0, 2]
                    std = df_tmp_offset.iloc[0, 3]

                    label1core = row['label1core']
                    df1_tmp = exp_data.loc[label1core,
                                           (slice(None),
                                            [benchmark],
                                            ['core0'])]
                    if len(df1_tmp.index) > 0:
                        # df1_tmp now contains one row, 4 cols
                        # (amax, mean, median, std)
                        print(df1_tmp)
                        wcet1 = df1_tmp.iloc[0, 0]
                        mean1 = df1_tmp.iloc[0, 1]
                        # median1 = df1_tmp.iloc[0, 2]
                        # std1 = df1_tmp.iloc[0, 3]

                        if mean != 0:
                            slowdown = mean / mean1
                        else:
                            slowdown = None

                        if wcet1 != 0:
                            slowdown_wcet = wcet / wcet1
                        else:
                            slowdown_wcet = None

                        logger.debug(f'Label:{label}' +
                                     f'offset:{offset} ' +
                                     f'slowdown factor:{slowdown} ' +
                                     f'slowdown factor wcet:{slowdown_wcet}')
                        ps = pd.Series({'label': label,
                                        'label1core': label1core,
                                        'cores': cores,
                                        'benchmark': benchmark,
                                        'inputsize': inputsize,
                                        'offset': offset,
                                        'mean': mean,
                                        'confidence_lo': conf_interval[0],
                                        'confidence_hi': conf_interval[1],
                                        'mean1core': mean1,
                                        'slowdown': slowdown,
                                        'wcet': wcet,
                                        'wcet1core': wcet1,
                                        'slowdown_wcet': slowdown_wcet,
                                        'median': median,
                                        'stdev': std})
                        exp_results = exp_results.append(ps, ignore_index=True)
        except KeyError:
            logger.debug('Caught KeyError for label {}'.format(label))

    return exp_results


@click.command()
@click.option('--input-file',
              required=True,
              help=('Path and filename of the input Excel file containing' +
                    ' the experiments.'))
@click.option('--output-file',
              required=True,
              help='Path and filename of the output file.')
@click.option('--csv-dir',
              default='output',
              help='Path of the directory where the CSV logs are stored.')
@click.option('--csv-file-prefix',
              required=True,
              help=('Prefix of input CSV filenames to be analysed.'))
@click.option('--data-dir',
              default='report/data',
              help='Path of the directory where the data files are stored.')
@click_log.simple_verbosity_option(logger)
def main(input_file, output_file, csv_dir, csv_file_prefix, data_dir):
    if not isfile(input_file):
        logger.error('Error: input file {} '.format(input_file) +
                     'does not exist!')
        exit(1)
    if isfile(output_file):
        logger.error('Error: output file {} '.format(output_file) +
                     'already exists!')
        exit(1)

    # First get all labels of the experiments, mapped to their
    # corresponding single run (no co-runners) experiments.
    logger.info('Reading experiment labels from excel file ' +
                ' "{}".'.format(input_file))
    exp_labels = get_experiment_labels(input_file)

    logger.info('Reading experiment data from CSV files found ' +
                'in directory "{}".'.format(csv_dir))
    exp_data = get_experiment_data(csv_dir, csv_file_prefix)

    logger.info('Combining label mappings with experiment data...')
    exp_results = get_experiment_results(exp_labels, exp_data, data_dir)
    logger.info('Writing resulting slowdown factors to CSV ' +
                'output file "{}".'.format(output_file))
    exp_results.to_csv(output_file, index=False, sep=' ')


if __name__ == "__main__":
    main()
