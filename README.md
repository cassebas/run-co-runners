# What is this and what does this do?
This is the work done for my master's thesis project on the improvement of
real-time systems. It is a collection of platforms and tools with which
together experiments can be defined and run, to measure timing properties
of software. This is important for real-time systems, where the application
faces deadlines.

A more extensive explanation of the thesis background can be found in the thesis report,
which is located [here](http://resolver.tudelft.nl/uuid:073e1182-8af3-4deb-91cb-87ba9f3009fa).

The text below is the appendix chapter of the report, in which details of specific
components of the tool can be found.

# Implementation details

This chapter describes the details of the implemented tool. Our tool is
open source and publicly available on GitHub[^1]. With the description
below, users should be able to use the tool and extend it for their own
research purposes.

## Technical overview

Globally speaking, our parametric WCET estimation tool consists of four
components. These are:

-   **Raspberry Pi** --- This is the hardware on which the experiments
    are performed.

-   **Computer** --- The computer acts like the control center, from
    which the experiments are run.

-   **Arduino** --- The Arduino serves as an extension to the computer,
    with which the Raspberry Pi can be reset.

-   **TFTP server** --- The TFTP server contains the runtime binary that
    is downloaded by the Raspberry Pi through the network.

These components are graphically illustrated in and are further
described below.

![Main components that together form the
tool](img/techdesign_schematic.png)

### Raspberry Pi

In the project, two versions of the Raspberry Pi computer form the heart
of the experiments. They were chosen for the quad processors that they
contain, the ARM Cortex A53 (Raspberry Pi 3) and the ARM Cortex A72
(Raspberry Pi 4).

The connections from and to the Raspberry Pi are:

-   Raspberry Pi $\longleftrightarrow$ TFTP server --- This is a network
    connection made with a UTP cable.

-   Raspberry Pi $\longleftrightarrow$ Arduino --- This is a 2-wire
    connection made from the Raspberry Pi's `RUN` header to the
    Arduino's pin 13 (high/low voltage) and the Arduino's GND (low
    voltage).

-   Raspberry Pi $\longleftrightarrow$ Computer --- This is a serial
    connection, made with a USB to TTL serial cable. On the Raspberry
    Pi, the cable is connected to the `UART0_TXD` and `UART0_RXD` with
    `GPIO14` and `GPIO15`, respectively. The black `GND` wire in the
    cable is connected to `GND`, but the red power wire is not
    connected, since the Raspberry Pi is powered by the official power
    adapter.

### Arduino

The Arduino was added to the experimental platform, to be used as a
proxy on behalf of the computer's control center. The Arduino runs a
simple program. It will continuously set pin 13 to high and listen to
the serial port to receive a character. When the character 'r' is
received, it will set pin 13 to low. This will be cause the connected
Raspberry Pi's RUN pins to become low, effectively making the Raspberry
Pi perform a system reset.

### TFTP server

The Raspberry Pi features several options for loading the runtime binary
upon power up. The most obvious and easiest alternative is to boot from
a microSD card. This method is very simple, it only involves copying the
boot files onto a microSD card, put it into the microSD card slot and
power on the Raspberry Pi.

Obviously, when doing many experiments, this method quickly becomes
infeasible because for each experiment a newly compiled runtime binary
is to be copied onto the microSD card. Another solution is to program
the Raspberry Pi with a JTAG capable programmer. While the JTAG
programmer could be used halt the processor and start a debug session,
the method is complex and too involved for just booting the Raspberry
Pi.

Finally, there is the possibility for the Raspberry Pi to boot from the
network. This method is straightforward and has been used in this
project. For this method to work, a TFTP server is necessary which
serves the necessary boot files. The TFTP server could be hosted in the
local LAN on a physical device (possibly another Raspberry Pi), but in
this project a virtualization platform is used. A virtual machine was
created by the use of `vagrant` with `virtualbox` as the provider of the
virtual machine.

Details of the implemented TFTP server solution can be found on
GitHub[^2].

### Computer

The computer acts as the control center, on which all experiments are
created and run. The experimental platform that runs on the computer is
discussed in more detail below.

The computer's connections are:

-   Computer $\longleftrightarrow$ TFTP server --- Depending on the
    location of the TFTP server, this could either be a network
    connection, or it could be just local file copy in the case of a
    virtualized TFTP server that runs on the same computer.

-   Computer $\longleftrightarrow$ Arduino --- This connection is a
    serial connection, which is made with the standard blue Arduino USB
    cable.

## Implementation of system and benchmarks

Two target platforms are used for running the
experiments. Both platforms feature a Raspberry Pi computer, a 'bare
metal'-like operating system and the benchmarks that were ported to the
platforms. The platforms are described below.

### Raspberry Pi 3 + `xRTOS`

The `xRTOS`[^3] operating system was especially written for the
multicore Raspberry Pi to serve as a basic real-time operating system.
The Raspberry Pi versions 2 and 3 are supported. Its implementation is a
combination of assembly and C. It features a preemptive scheduler, which
in its basic implementation only draws progress bars onto the screen.
For the purposes of this project, the preemptive scheduler was modified
to allow for non-preemptive execution of the benchmarks. The `xRTOS`
repository was forked to apply our experimental additions.[^4]

### Raspberry Pi 4 + `circle`

The `circle`[^5] platform is a bare metal programming environment for
the Raspberry Pi. It was written to serve as a educational tool, which
can be tried and tested and extended. It supports the Raspberry Pi
versions 2, 3, 4 and Zero. It is written in a combination of assembly
and C++. `Circle` features a lot of demo programs. Also, it contains a
structure in which the user's own program can be added with ease.
Multi-threaded execution on multiple cores is supported. The `circle`
repository was forked to apply our own experimental additions.[^6]

### The `benchmark_config.m4` script

Both `xRTOS` and `circle` have been extended/modified to continuously
run selected benchmarks, while measuring the execution cycles from start
to end. The porting and addition of the benchmarks' source code has been
done with the requirements of extensibility and maintainability in mind.
For this, the use of `m4` macros was chosen.

With the use of `m4` macros, the experiments are configurable can be
extended with new benchmarks or programs relatively easy. The main
source code does not need be changed for configuration or addition of
benchmarks. The way this works is by generation of source code with the
use of the `benchmark_config.m4` script. Examples of important macros
that are generated are:

-   `BENCH_INIT1_CORE0` --- This macro will generate code that typically
    declares or defines variables, which in this case run on core 0. The
    `INIT1` part in the name stands for the fact that the generated
    content by this macro is executed once, before the main control loop
    of the core running the benchmark.

-   `BENCH_INIT2_CORE0` --- This macro will typically initialize
    variables, on core 0 in this case. The `INIT2` part in the name
    stands for the fact that the generated content is executed as part
    of the main control loop of the core running the benchmark.

-   `DO_BENCH_CORE0` --- This macro will start the actual execution of
    the benchmark, that is configured to run in core 0. It is executed
    on each iteration of the main control loop, thereby generating
    repeated executions of the same benchmark.

An example usage of the `benchmark_config.m4` script is:

``` shell
  $ m4 -Dconfig_series=3111 -Dconfig_benchmarks=1444 -Dinputsize_core0=32 \
  -Dinputsize_core1=1024 -Dinputsize_core2=1024 -Dinputsize_core3=1024 \
  -Dexp_label=DISPARITY_4CORE_TEST benchmark_config.m4 > benchmark_config.h
```

The result of the `m4` command above is written to the
`benchmark_config.h` file. This C header file contains the configution
of the benchmarks, like the specific benchmarks to run on which core,
memory sizes and so forth. To include the `benchmark_config.h` header
file, the environment variable `BENCHMARK_CONFIG` must be set to
`-DBENCHMARK_CONFIG_M4` in the make process. This way the C preprocessor
knows that it must include the header file.

Below the `benchmark_config.m4` script parameters are described.

#### Parameters of `benchmark_config.m4`

::: tabular
m0.03wc0.2wc0.2wc0.2 & 1 & 2 & 3\
& linear array access & mälardalen bsort100 & sd-vbs disparity\
& linear array write & mälardalen ns & sd-vbs mser\
& random array access & mälardalen matmult & sd-vbs svm\
& random array write & mälardalen fir & sd-vbs stitch\
:::

The `benchmark_config.m4` can take the following parameters:

-   `exp_label` --- Set the label for the experiment, which will be used
    in the reported log lines. The label is of importance in the data
    processing step, which is described in .

-   `config_series` --- In the reference implementation of the tool,
    three types of benchmark series have been implemented. These are
    **(1)** synthetic benchmarks, **(2)** benchmarks from the Mälardalen
    benchmark suite and **(3)** the SD-VBS benchmark suite. The
    selection of the benchmarks series to run is encoded in the
    `config_series` string, where the length of the string specifies the
    number of cores that is used in the experiment and the $i^{th}$
    digit in the string specifies the series number that is to be run on
    core $i$ (where $0 <= i <= 3$).

-   `config_benchmarks` --- The `config_benchmarks` string encodes the
    benchmark to run. Like in the `config_series` string, its length
    specifies the number of cores to run. The $i^{th}$ digit in the
    string specifies the benchmark to be run on core $i$ (where
    $0 <= i <= 3$). See for the list of implemented benchmarks and their
    corresponding numbers.

-   `inputsize_core_n` --- This parameter specifies the input size of
    the benchmark that is to run on core number $n$ ($0 <= n <= 3$).

-   `pmu_core_n` --- The `pmu_core_n` specifies the event types that are
    to be monitored by the ARM performance monitor on core number $n$.
    The `pmu_core_n` parameter is a string, where the length of the
    string is equal to the number of events that must be monitored. The
    string is encoded by the use of a mapping from an event code (0
    to 9) to the event number specified by ARM. The $i^{th}$ position of
    the string specifies the $i^{th}$ event number to be monitored. See
    table for the supported event types that can by monitored by the
    PMU. Currently, the maximum number of events that can be encoded in
    the string is 4.

    ::: tabular
    wc0.1wc0.2m0.34 Event code & ARM event number & Event name\
    & 0x03 & L1 Data cache refill\
    & 0x04 & L1 Data cache access\
    & 0x05 & L1 Data TLB refill\
    & 0x13 & Data memory access\
    & 0x15 & L1 Data cache Write-back\
    & 0x16 & L2 Data cache access\
    & 0x17 & L2 Data cache refill\
    & 0x18 & L2 Data cache Write-back\
    & 0x19 & Bus access\
    & 0x1D & Bus cycles\
    :::

-   `mmu_enable` --- \[`xRTOS` only\] This parameter configures the MMU
    (memory management unit) to be enabled. Without specifying this
    parameter, the MMU will not be enabled (on the `xRTOS` platform).

-   `screen_enable` --- \[`xRTOS` only\] This parameter configures the
    screen to be enabled. Without specifying this parameter, the screen
    will not be used (on the `xRTOS` platform).

-   `delay_step_countdown` --- The `countdown` function is a simple
    function written in assembly that is designed to make the processor
    spinlock for a specific number of processor cycles. In order to
    create (reasonably) precise delays in the start time of the
    co-runners' execution, the `countdown` function is used in
    combination with the `delay_step_countdown` parameter. This is
    further explained in .

-   `report_cycles_countdown` ---Since the number of cycles that is
    spent on each countdown step depends on the specific processor and
    operating system, the `report_cycles_countdown` parameter can be
    used to test the `countdown` function and print the number of cycles
    that is used for the `countdown` function.

-   `synbench_repeat` --- This parameter allows the co-runners to have
    an extended duration of execution time, to be able to keep stressing
    the task under study when the task is running for a very long time.
    When not specified, `synbench_repeat` is defined as 1.

-   `debug_enable` --- This parameter enabled debug information to be
    printed to the serial port.

## Experimental setup

In this section, the main components of the experimental setup are
described. First, there is the definition of the experiments by the use
of a spreadsheet. Second, the `run_experiments.py` Python script reads
the experiments definition and automatically runs multiple experiments
and logs all incoming data to an output file. These components are
discussed next.

### Experiments definition

In this section, the way the experiments are defined is explained. First
of all, an important concept for the delayed execution of co-runners is
explained.

#### Delayed execution of co-runners

The parametric WCET estimation tool runs the task and its co-runners
both in synchronized fashion and with delayed execution of the
co-runners. The idea behind the delayed execution is as follows. Because
we want to be able to control the length of the delay, the baseline WCET
is conceptually divided in time intervals. The baseline WCET is the
maximum measured number of cycles that the task needs to complete its
task when run in isolation.

The time intervals are called *delay steps*. When the baseline WCET is
conceptually divided into 10 delay steps, a delayed execution of 10
delay steps effectively means that the task and co-runners are executed
consecutively, instead of in parallel.

The controlling of the delayed execution is done by the parameters
`delay step countdown`, `measured wcet baseline` and `cycles per count`
parameters in the experiment definition. These parameters and all other
parameters are described below.

#### Explanation of the spreadsheet

For defining the experiments, an Excel spreadsheet is used. On each row,
one experiment can be defined, where the columns contain the parameters
that define the specifics of the experiment.

The columns with the parameter definitions are:

-   `experiment number` --- The number of this experiment, this number
    serves as an identifier for the experiment and is used for selection
    by the\
    `run_experiments.py` script.

-   `platform` --- The platform on which the experiment is to be run.
    This can by either `xRTOS` or `circle`. Please note that currently,
    all experiments defined in one spreadsheet must run on the same
    platform.

-   `raspberry pi` --- The Raspberry Pi version to run the experiment
    on. This can either be 3 or 4, for running on the Raspberry Pi 3 or
    Raspberry Pi 4, respectively. Please note that currently, all
    experiments defined in one spreadsheet must run on the same
    Raspberry Pi.

-   `benchmark_series` --- Currently, three types of benchmark series
    have been implemented. These are **(1)** synthetic benchmarks,
    **(2)** benchmarks from the Mälardalen benchmark suite and **(3)**
    the SD-VBS benchmark suite. The selection of the benchmarks series
    to run is encoded here, where the length of the string specifies the
    number of cores that is used in the experiment and the $i^{th}$
    digit in the string specifies the series number that is to be run on
    core $i$ (where $0 <= i <= 3$).

    See for an overview of the benchmark series that can be used. Please
    note that the string is surrounded by quotes (**not** smart quotes),
    to force a string data type in Excel.

-   `benchmark_configuration` --- The `benchmark_configuration` string
    encodes the benchmarks to run. Like in the `benchmark_series`
    parameter, its length specifies the number of cores to run. The
    $i^{th}$ digit in the string specifies the benchmark to be run on
    core $i$ (where $0 <= i <= 3$).

    See for the list of implemented benchmarks and their corresponding
    numbers. Please note that the string is surrounded by quotes
    (**not** smart quotes), to force a string data type in Excel.

-   `enable mmu` --- Wheter or not to enable the MMU (memory management
    unit). This parameter must be `TRUE` or `FALSE`. Please note that
    this parameter is only supported for the `xRTOS` platform running on
    the Raspberry Pi 3.

-   `enable screen` --- Whether or not the enable the screen. This
    parameter can either be `TRUE` or `FALSE`. Please note that this
    parameter is only supported for the `xRTOS` platform running on the
    Raspberry Pi 3.

-   `no cache management` --- Each experiment is repeated for a multiple
    iterations (the minimum of which can be specified on the command
    line when using the `run_experiments.py` script). The default
    behavior is to clean the instruction and data caches before running
    each benchmark, in an attempt to create equal conditions between
    each iteration. The `no cache management` parameter can be used to
    disable the cache cleaning.

-   `experiment label` --- Define the experiment label for the
    experiment, which is used in the data processing step (further
    described in\
    ).

-   `pmu core_n` --- The `pmu core_n` parameter specifies the event
    types that are to be monitored by the ARM performance monitor on
    core number $n$. The `pmu core_n` parameter is a string, where the
    length of the string is equal to the number of events that must be
    monitored. The string is encoded by the use of a mapping from an
    event code (0 to 9) to the event number specified by ARM. The
    $i^{th}$ position of the string specifies the $i^{th}$ event number
    to be monitored. See table for the supported event types that can by
    monitored by the PMU. Currently, the maximum number of events that
    can be encoded in the string is 4.

-   `inputsize core_n` --- This parameter specifies the input size of
    the benchmark that is to run on core number $n$ ($0 <= n <= 3$).

-   `delay step countdown` --- The `countdown` function is a simple
    function written in assembly that is designed to make the processor
    spinlock for a specific number of processor cycles. In order to
    create (reasonably) precise delays in the start time of the
    co-runners' execution, the `countdown` function is used in
    combination with the `delay step countdown` parameter.

    This parameter specifies the number of times the `countdown`
    function must be called, to create one delay step. Please note that
    this parameter is auto filled in by a formula.

-   `measured wcet baseline` --- To determine the number of times the\
    `countdown` function must be called for one delay step, the length
    of the baseline WCET in cycles must be specified. This implies that
    to correctly create delay offsets for the co-runners, the
    specification of the experiments is like a 2-stage rocket. First the
    benchmarks must be run in isolation, to determine the estimation of
    the baseline WCET (cycles). This number must then be put into the
    experiment definitions, to be able to compute the number of calls to
    the `countdown` function to create one delay step.

-   `cycles per count` --- The number of cycles that is spent for one
    execution of the `countdown` function. Since the number of cycles
    that is spent on each countdown call depends on the specific
    processor and operating system, the `report_cycles_countdown`
    parameter of the `benchmark_config.m4` script can be used to test
    the `countdown` function and print the number of cycles that is used
    for the `countdown` function.

-   `synbench_repeat` --- This parameter allows the co-runners to have
    an extended duration of execution time, to be able to keep stressing
    the task under study when the task is running for a very long time.
    When not specified, `synbench_repeat` is defined as 1.

An important concept of the Excel spreadsheet is that one spreadsheet
should contain both the experiment with the task run in isolation, as
well as the experiment(s) with the same task running with one to three
co-runners. This way, the `slowdown_factors.py` script () is able to
match each co-runners experiment to its task-in-isolation counterpart.

### The run_experiments.py script

The `run_experiments.py` Python script is used to automatically run
multiple experiments in one go. The script reads the experiments
definition from a spreadsheet, and writes the received log output to a
specified output file.

An example usage of the `run_experiments.py` script is:

``` shell
$ python run_experiments.py --working-directory-circle=../../circle/app/corunners \
  --input-file xlsx/experiments_SD-VBS_stitch_circle_pi4.xlsx \
  --output-file output/experiments_SD-VBS_stitch_circle_pi4_exp11.log \
  --min-observations 200 --experiment-begin 11 --experiment-count 1
```

The parameters of the of the `run_experiments.py` script are:

-   `--input-file` --- The path and name of the Excel input file
    containing the experiment definitions.

-   `--output-file` --- The path and name of the output file, to which
    all logs must be written.

-   `--working-directory-xrtos` --- The path of the directory where the
    `xRTOS` system is located. The `xRTOS` system is a submodule of the\
    `run-co-runners` Git repository, by default this parameter is set
    to\
    `../platforms/raspberrypi/Raspberry-Pi-Multicore/xRTOS_MMU_SEMAPHORE`

-   `--working-directory-circle` --- The path of the directory where the
    `circle` system is located. The `circle` system is a submodule of
    the `run-co-runners` Git repository, by default this parameter is
    set to\
    `../platforms/raspberrypi/circle/app/corunners`

-   `--tty-reset` --- Serial port to which the Arduino is connected. It
    is the path and name of the serial port that is used for the
    resetting the Raspberry Pi. By default, it is set to `/dev/ttyUSB0`.

-   `--tty-logging` --- Serial port to which the Raspberry Pi is
    connected. It is the path and name of the serial port that is used
    to receive all logging information sent by the Raspberry Pi. By
    default, it is set to `/dev/ttyUSB1`.

-   `--min-observations` --- Minimum number of observations that must be
    seen in the logs received from the Raspberry Pi, before the next
    experiment can be selected and the Raspberry Pi can receive a reset
    signal.

-   `--experiment-begin` --- The experiment identifier of the experiment
    with which to begin running the experiments.

-   `--experiment-count` --- The number of experiments that must be run
    consecutively, starting from the first experiment specified by
    identifier `--experiment-begin`.

-   `-v, --verbosity` --- Define the verbosity for the program, which
    can be either CRITICAL, ERROR, WARNING, INFO or DEBUG. By default,
    the verbosity level is set to INFO.

-   `--help` --- Print usage information and exit program.

## Data processing

In this section the data processing step is discussed. The experiments
output log data to the serial port, which is captured by the
`run_experiments.py` script. This output is converted to several other
output formats, such as CSV files and graphical output of measured
cycles and PMU events.

### Overview of the data processing step

A major part of the data processing is done automatically, by the use of
a `Makefile` script that executes the scripts one by one. These scripts
are explained in detail below. Here, an overview of the data conversion
is described.

The output of the experiments are plain text log files. Each line
contains one measurement of the experiment, this can either be a cycles
measurement or one of the PMU performance event counter measurements.
The plain text log files are first converted to CSV format. They are
split into cycles data CSV files and events data CSV files. By default,
the log files and CSV files are located in the
`run-co-runners/experiment/output` directory.

The above log files and CSV files contain multiple experiments' data in
a single file. These files are further separated into files containing
the data of only one experiment. Two types of CSV file are created, one
containing all data measurements (cycles or events) for one experiment,
and the other containing aggregated summary information of the
measurements for one experiment (cycles only). The aggregated values are
the median, mean and maximum values, including their standard
deviations. By default, the location of the CSV files with single
experiments is the `run-co-runners/experiment/report/data` directory.

Next, for each experiment a data visualization is generated, using as
input the data CSV files containing the cycles measurements. When PMU
events data for the same experiment is present in the same directory,
these data will be included in the data visualization.

A separate step is the generation of a PDF report containing graphical
output of the aggregated cycles data information. The generation is done
using LaTeX templates, which are in itself generated by `m4` macros. The
figures in the PDF are generated using the PGFPlots package.[^7]

### Description of data processing scripts

In the following, the scripts that convert the log data are explained.
Most scripts are included in a `Makefile` for automatic processing,
except for the `slowdown_factors.py` script.

#### log2csv-cyclecount.awk

The output log file contains the raw data, where both cycles data and
performance events are present. The `log2csv-cyclecount.awk` script
captures the cycles data and converts the data to CSV format.

An example execution of the `log2csv-cyclecount.awk` is:

``` shell
  awk -f log2csv-cyclecount.awk \
  output/experiments_SD-VBS_stitch_circle_pi4-exp11.log
```

#### log2csv-eventcount.awk

The `log2csv-eventcount.awk` script captures the performance events data
and converts the data to CSV format.

An example execution of the `log2csv-eventcount.awk` is:

``` shell
  awk -f log2csv-eventcount.awk \
  output/experiments_SD-VBS_stitch_circle_pi4-exp11.log
```

#### data2linearchart.py

The `data2linearchart.py` script outputs a CSV input file containing a
single experiment to a graphical data visualization. In the graphic, the
iteration numbers are placed on the `x`-axis and their corresponding
cycles data is placed on the `y`-axis. If PMU events data is present for
the experiments, it will be plotted together with the cycles data (using
a twin axis). See for an example output image.

An example execution of the `data2linearchart.py` is:

``` shell
  python data2linearchart.py \
  --input-file=report/data/cyclesdata-core3-configseries211-configbench322-offset10.csv \
  --output-directory=report/img \
  --maximum-observations=250 --movingaverage-window=0 \
  --process-events=True
```

The options of the `data2linearchart.py` script are:

-   `--input-file` --- Path and filename of the input CSV file
    containing the experiment cycles data.

-   `--output-file` --- Path of the directory where to place the output
    PNG files.

-   `--maximum-observations` --- Maximum number of observations to
    include in the output plot.

-   `--movingaverage-window` --- Size of the moving average window to
    plot, instead of the actual cycles data. The default is a moving
    average window of 0, which means do not plot the moving average.

-   `--process-events` --- Whether or not to process the events data, by
    default the events data are processed.

-   `-v, --verbosity` --- Define the verbosity for the program, which
    can be either CRITICAL, ERROR, WARNING, INFO or DEBUG. By default,
    the verbosity level is set to INFO.

#### log2data_and_summaries.py

The `log2data_and_summaries.py` script takes the CSV files which are
generated by the `awk` scripts, and splits these files into files
containing single experiments. Several output options are possible,
which are described below.

An example execution of the `log2data_and_summaries.py` script is:

``` shell
python log2data_and_summaries.py \
  --input-file=output/experiments_Mälardalen_matmult_circle_pi4-2-cycles.csv \
  --output-directory=report/data --output-mode=data --metric=cycle
```

The options of the `log2data_and_summaries.py` script are:

-   `--input-file` --- Path and filename of the CSV input file
    containing the cycles data or events data, where several experiments
    (may be) combined in one file.

-   `--output-directory` --- Path of the output directory, to where the
    output CSV files containing single experiments must be written.

-   `--output-mode` --- The output mode determines whether an aggregated
    `summary` of the experiment must be generated, or whether the `data`
    must be written to the output file.

-   `--metric` --- Whether the `cycles` are to be converted to a single
    experiment file, or `data` are to be converted to a single file.
    This option can only work for output-mode equal to `data`.

-   `-v, --verbosity` --- Define the verbosity for the program, which
    can be either CRITICAL, ERROR, WARNING, INFO or DEBUG. By default,
    the verbosity level is set to INFO.

#### slowdown_factors.py

The `slowdown_factors.py` script computes the slowdown factors for the
experiments. For this, the experiment definition Excel file is read, to
be able to match the experiment with co-runners to its counterpart
without co-runners.

An example run of the `slowdown_factors.py` script is:

``` shell
  python slowdown_factors.py \
  --input-file xlsx/experiments_SD-VBS_stitch_circle_pi4.xlsx \
  --output-file slowdown-factors-sdvbs-stitch_pi4-20201019.csv \
  --csv-file-prefix=experiments_SD-VBS_stitch_circle_pi4
```

The options of the `slowdown_factors.py` script are:

-   `--input-file` --- Path and filename of the input Excel file
    containing the experiment definitions.

-   `--output-file` --- Path and filename of the CSV output file.

-   `--csv-dir` --- Path of the directory where the input CSV files are
    stored, which contain the log data to be analyzed.

-   `--csv-file-prefix` --- Prefix of the input CSV filenames to be
    analyzed. The prefix acts as a filter, to make the script not read
    non-relevant CSV files.

-   `--data-dir` --- Path of the directory where the data files are
    stored. This directory contains the CSV files which were already
    separated per experiment.

-   `-v, --verbosity` --- Define the verbosity for the program, which
    can be either CRITICAL, ERROR, WARNING, INFO or DEBUG. By default,
    the verbosity level is set to INFO.

#### maketex-cyclessummaries.m4

A separate step is the generation of a PDF report containing graphical
output of the aggregated cycles summary information. The generation is
done using LaTeX templates, which are in itself generated by the
`maketex-cyclessummaries.m4` script.

An example execution of the `maketex-cyclessummaries.m4` script is:

``` shell
  m4 -Dfilename=data/cyclessummary-DISPARITY_CORES4_INPUTSIZE32.csv \
  -Dconfig_series=3111 -Dconfig_benchmarks= \
  -Dlabel=DISPARITY_CORES4_INPUTSIZE32 maketex-cyclesummaries.m4
```

Normally, the `maketex-cyclessummaries.m4` script is executed by the\
`Makefile` which was mentioned above. Another `Makefile`, which is
located in the `run-co-runners/experiment/report` directory, generates
the final PDF containing the PGFPlots figures.

### Jupyter notebook files

Jupyter[^8] is a web application in which users can create documents
('notebooks') in which code (e.g. Python) is mixed with documentation.
The code within the notebook can be executed to generate output, such as
data visualizations. In this project, the `jupytext`[^9] extension has
been used for an automatic conversion of the Jupyter notebooks to Python
scripts, which can be committed to Git.

Several Jupyter notebook files have been created, in which output data
is read and transformed to various data visualizations. These notebooks
are part of the `run-co-runners` Git repository, and serve as examples
of how the log data can be transformed to more meaningful information on
the experiments. Please note that the `jupytext` extension is needed to
convert the example notebooks from Python to the Jupyter notebook format
(with `.ipynb` extension).

The example Jupyter notebooks are:

-   `notebook_mälardalen-bsort-pi3.py` --- This notebook contains the
    results of the experiments with the Mälardalen `bsort` benchmark. It
    contains boxplot visualizations of the experiments with varying
    input data sizes, and the computation of the Mann-Whitney U
    hypothesis tests.

-   `notebook_sdvbs-stitch-pi4.py` --- This notebook reports on the
    results of the SD-VBS `stitch` benchmark. It reads the slowdown
    factors from the CSV file
    `slowdown-factors-sdvbs-stitcho_pi4-20201019.csv`, and\
    prints `pandoc` data frames from the data. A data visualization is
    generated containing slowdown effects in relation to the size of the
    delayed execution.

-   `notebook_sdvbs-disparity-pi3.py` --- This notebook features various
    data visualizations from the experiments with the SD-VBS `disparity`
    benchmark. Slowdown factors are read from the corresponding CSV file
    and printed in the form of data frames. Several output graphics are
    created by the use of matplotlib.

-   `notebook_sdvbs-disparity-pi4.py` --- This notebook contains the
    same data visualizations like the above notebook, but for the
    experiments that were run on the Raspberry Pi 4.

-   `notebook_mälardalen-matmult-pi3.py` --- This notebook contains data
    visualizations of experiments with the Mälardalen `matmult`
    benchmark. Slowdown factors are printed and visualizations are
    created showing the effects of delayed execution of the co-runners.

-   `notebook_mälardalen-matmult-pi4.py` --- This notebook contains the
    same data visualizations as the notebook described above, but for
    the experiments that were run on the Raspberry Pi 4.

### Known limitations and gotchas

In the following, some known limitations of our tool are reported.

-   System freezes --- In rare cases, a core running a task would hang.
    The cause for this behavior has not been found. The environment in
    which the tasks run is difficult to debug, because of multiple cores
    running simultaneously in a bare metal environment. The
    `run_experiments.py` script works around this problem, by resetting
    the Raspberry Pi upon a timeout. This timeout is generated when no
    data has been received from the Raspberry Pi for a long period of
    time.

-   Booting the Raspberry Pi --- Sometimes, the Raspberry Pi 3 would not
    boot from the network. Again, the `run_experiments.py` script uses
    the timeout mechanism to detect a failure to boot, and will reset
    the Raspberry Pi if no data is not received for a long period of
    time.

-   Users should be aware of the fact that, to be able to automatically
    reset the Raspberry Pi, some header pins may need to be soldered on
    the RUN header of the Raspberry Pi.

-   While testing on multiple computers, sometimes the virtualized TFTP
    server could not be used to boot from the virtual network created by
    VirtualBox. A solution is to place the TFTP server in the local LAN.

[^1]: https://github.com/cassebas/run-co-runners.git

[^2]: https://github.com/cassebas/Raspberry-Pi-Networkboot.git

[^3]: https://github.com/LdB-ECM/Raspberry-Pi-Multicore.git

[^4]: https://github.com/cassebas/Raspberry-Pi-Multicore.git ---
    `experiment` branch

[^5]: https://github.com/rsta2/circle.git

[^6]: https://github.com/cassebas/circle.git --- `experiment` branch

[^7]: http://pgfplots.net

[^8]: https://jupyter.org

[^9]: https://jupytext.readthedocs.io
