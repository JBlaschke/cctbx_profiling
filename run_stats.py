#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import statistics as stat
import debug

data_path = sys.argv[1]



def get_stats(data, n_data):
    min_data = -1
    max_data = -1
    avg_data = -1
    std_data = -1

    if n_data > 0:
        min_data = min(data)
        max_data = max(data)
        avg_data = stat.mean(data)
    if n_data > 1:
        std_data = stat.stdev(data)

    return min_data, max_data, avg_data, std_data



# parse the profiling data in debug
parser = debug.DebugParser(data_path)
ds     = parser.parse()

# compute stats
ds.compute_stats()

n_good = ds.good_total

min_good_diff, max_good_diff, avg_good_diff, std_good_diff =\
    get_stats(ds.good_diff, n_good)
min_good_len, max_good_len, avg_good_len, std_good_len =\
    get_stats(ds.good_duration, n_good)

n_fail = ds.fail_total

min_fail_diff, max_fail_diff, avg_fail_diff, std_fail_diff =\
    get_stats(ds.failed_diff, n_fail)
min_fail_len, max_fail_len, avg_fail_len, std_fail_len =\
    get_stats(ds.failed_duration, n_fail)


# output results for user
print(f"+--------------------------------------------------------------------+")
print(f"|             Successfully indexed: {n_good:11}                      |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"|                   | min                   |  max                   |")
print(f"|                   | mean                  |  standard deviation    |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"| Event Durations   | {min_good_len:20.8f}  | {max_good_len:20.8f}   |")
print(f"|                   | {avg_good_len:20.8f}  | {std_good_len:20.8f}   |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"| Event Diffs       | {min_good_diff:21.8f} | {max_good_diff:21.8f}  |")
print(f"|                   | {avg_good_diff:21.8f} | {std_good_diff:21.8f}  |")
print(f"+-------------------+-----------------------+------------------------+")
print("")
print(f"+--------------------------------------------------------------------+")
print(f"|             Failed to be indexed: {n_fail:11}                      |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"|                   | min                   |  max                   |")
print(f"|                   | mean                  |  standard deviation    |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"| Event Durations   | {min_fail_len:20.8f}  | {max_fail_len:20.8f}   |")
print(f"|                   | {avg_fail_len:20.8f}  | {std_fail_len:20.8f}   |")
print(f"+-------------------+-----------------------+------------------------+")
print(f"| Event Diffs       | {min_fail_diff:21.8f} | {max_fail_diff:21.8f}  |")
print(f"|                   | {avg_fail_diff:21.8f} | {std_fail_diff:21.8f}  |")
print(f"+-------------------+-----------------------+------------------------+")
