#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from weatherplot import weather

data_path = sys.argv[1]
data      = weather.load_dir(input_path=data_path)

good_deltas, failed_deltas = weather.compute_deltas(data)
n_good,      n_failed      = weather.combine_totals(data)

min_good = np.min(good_deltas)
max_good = np.max(good_deltas)
avg_good = np.mean(good_deltas)
std_good = np.std(good_deltas)

min_failed = np.min(failed_deltas)
max_failed = np.max(failed_deltas)
avg_failed = np.mean(failed_deltas)
std_failed = np.std(failed_deltas)

print(f"Successfully indexed: {n_good}")
print(f"min,  max = {min_good}, {max_good}")
print(f"mean, std = {avg_good}, {std_good}")

print("")
print(f"Failed to be indexed: {n_failed}")
print(f"min,  max = {min_failed}, {max_failed}")
print(f"mean, std = {avg_failed}, {std_failed}")
