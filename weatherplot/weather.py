#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import matplotlib.pyplot as plt

from .gears        import reverse_timestamp
from .libtbx.phil  import parse
from .libtbx.utils import Sorry



message = ''' script to get a sense of the computational performance of every
rank while processing data.  End product is a plot of wall time vs MPI rank
number with every data point being that of a frame processed by
dials.stills_process. The information is read in from the debug files created
by dials.stills_process.  Example usage on cxic0415 processed demo data -
libtbx.python weather.py input_path=cxic0415/output/debug
'''



phil_scope = parse('''
  input_path = .
    .type = str
    .help = path to where the processing results are. For example path to XXX_rgYYYY
  num_nodes = 1
    .type = int
    .help = Number of nodes used to do data processing. Used in timing information
  num_cores_per_node = 72
    .type = int
    .help = Number of cores per node in the machine (default is for Cori KNL)
  wall_time = 3600
    .type = int
    .help = total wall time (seconds) taken for job to finish. Used for plotting node-partitioning
  plot_title = Computational weather plot
    .type = str
    .help = title of the computational weather plot
  show_plot = True
    .type = bool
    .help = flag to indicate if plot should be displayed on screen
  pickle_plot = False
    .type = bool
    .help = If True, will pickle matplotlib session so that it can be opened later for analysis/viewing \
            https://stackoverflow.com/questions/29160177/matplotlib-save-file-to-be-reedited-later-in-ipython
  pickle_filename = fig_object.pickle
    .type = str
    .help = Default name of pickled matplotlib plot saved to disk
''')



def params_from_phil(args):
    user_phil = []
    for arg in args:
        if os.path.isfile(arg):
            user_phil.append(parse(file_name=arg))
        else:
            try:
                user_phil.append(parse(arg))
            except Exception as e:
                raise Sorry("Unrecognized argument: %s"%arg)

    params = phil_scope.fetch(sources=user_phil).extract()
    return params



def combine_dir(data_dict):

    combined = {"good_total": list(),
                "fail_total": list(),
                "good_x": list(),
                "good_y": list(),
                "failed_x": list(),
                "failed_y": list(),
                "notok": list(),
                "notok_x": list(),
                "notok_y": list()}

    for file_name in data_dict:

        data = data_dict[file_name]

        combined["good_x"]   += data["good_x"]
        combined["good_y"]   += data["good_y"]
        combined["failed_x"] += data["failed_x"]
        combined["failed_y"] += data["failed_y"]

        combined["good_total"].append(data["good_total"])
        combined["fail_total"].append(data["fail_total"])

        if not data["ok"]:
            combined["notok"].append(file_name)
            combined["notok_x"] += data["notok_x"]
            combined["notok_y"] += data["notok_x"]



    return combined



def combine_totals(data_dict):

    good_total = 0
    fail_total = 0

    for file_name in data_dict:

        data = data_dict[file_name]

        good_total += data["good_total"]
        fail_total += data["fail_total"]

    return good_total, fail_total



def compute_deltas(data_dict):

    good_deltas   = list()
    failed_deltas = list()

    for file_name in data_dict:

        data = data_dict[file_name]

        good_t   = data["good_x"]
        failed_t = data["failed_x"]

        good_deltas += [
            good_t[i+1] - good_t[i] for i in range(len(good_t) - 1)
        ]
        failed_deltas += [
            failed_t[i+1] - failed_t[i] for i in range(len(failed_t) - 1)
        ]

    return good_deltas, failed_deltas



def parse_dir(**params):

    counter = 0
    reference = None
    root = params["input_path"]
    good_total = fail_total = 0

    data = dict();

    for filename in os.listdir(root):
        if os.path.splitext(filename)[1] != '.txt': continue
        if 'debug' not in filename: continue
        fail_timepoints = []
        good_timepoints = []

        rank = int(filename.split('_')[1].split('.')[0])
        counter += 1

        for line in open(os.path.join(root,filename)):

            try:
                hostname, psanats, ts, status, result = line.strip().split(',')
            except ValueError:
                continue

            if reference is None:
                sec, ms = reverse_timestamp(ts)
                reference = sec+ms*1e-3

            if status in ['stop','done','fail']:
                sec, ms = reverse_timestamp(ts)
                if status == 'done':
                    good_timepoints.append((sec + ms*1.e-3)-reference)
                else:
                    fail_timepoints.append((sec + ms*1.e-3)-reference)
                ok = True
            else:
                ok = False

        failed_x = fail_timepoints
        failed_y = [rank]*len(fail_timepoints)
        good_x   = good_timepoints
        good_y   = [rank]*len(good_timepoints)

        fail_total += len(fail_timepoints)
        good_total += len(good_timepoints)

        notok_x = None
        notok_y = None
        if not ok:
            sec, ms = reverse_timestamp(ts)
            notok_x = [(sec+ms*1e-3) - reference]
            notok_y = [rank]
        #if counter > 100: break

        data[filename] = {"good_total": good_total,
                          "fail_total": fail_total,
                          "good_x": good_x,
                          "good_y": good_y,
                          "failed_x": failed_x,
                          "failed_y": failed_y,
                          "ok": ok,
                          "notok_x": notok_x,
                          "notok_y": notok_y}

    return data



def run(**params):

    data          = parse_dir(params)
    combined_data = combine_dir(data)

    fig_object = plt.figure()
    plt.plot(combined_data["good_x"],   combined_data["good_y"], 'g.')
    plt.plot(combined_data["failed_x"], combined_data["failed_y"], "b.")

    if len(combined_data["notok"]) > 0:
        plt.plot(combined_data["notok_x"], combined_data["notok_y"], "rx")


    # fail_deltas = [fail_timepoints[i+1] - fail_timepoints[i] for i in range(len(fail_timepoints)-1)]
    # good_deltas = [good_timepoints[i+1] - good_timepoints[i] for i in range(len(good_timepoints)-1)]
    # if fail_deltas: print("Five number summary of %d fail image processing times:"%fail_total, five_number_summary(flex.double(fail_deltas)))
    # if good_deltas: print("Five number summary of %d good image processing times:"%good_total, five_number_summary(flex.double(good_deltas)))

    for i in range(params.num_nodes):
        plt.plot([0, params.wall_time],
                 [i*params.num_cores_per_node - 0.5,
                  i*params.num_cores_per_node - 0.5], "r-"
                 )

    plt.xlabel('Wall time (sec)')
    plt.ylabel('MPI Rank Number')
    plt.title(params.plot_title)

    if params.pickle_plot:
        from libtbx.easy_pickle import dump
        dump('%s'%params.pickle_filename, fig_object)

    if params.show_plot:
        plt.show()



def plot(*args, **kwargs):

    if len(args) > 0:
        params = params_from_phil(args)
        return run(params, **kwargs)

    return run(**kwargs)



def load_dir(*args, **kwargs):

    if len(args) > 0:
        params = params_from_phil(args)
        return parse_dir(**params.__dict__, **kwargs)

    return parse_dir(**kwargs)



if __name__ == '__main__':
    if '--help' in sys.argv[1:] or '-h' in sys.argv[1:]:
        print (message)
        exit()
    params = params_from_phil(sys.argv[1:])
    run(params)
