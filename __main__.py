from sys      import argv
from os       import walk
from os.path  import join, basename, relpath
from shutil   import copytree
from argparse import ArgumentParser

import json   as js
import pickle as pkl

import profiling as prof



class OverwriteLast:
    """
    A status printer that overwrites the previous output.
    """

    def __init__(self):
        self.last = 0


    def print(self, s):

        if self.last:
            print(' '*self.last, end='\r')
        self.last = len(s)
        print(s, end='\r')



def find_debug(data_root):
    """
    Find all the debud directories under data_root
    """

    over = OverwriteLast()
    debug_dirs = list()
    for root, dirs, files in walk(data_root):
        over.print(f"Scanning: {root}")
        if basename(root) == "debug":
            debug_dirs.append(root)

    over.print("Scanning: Done!")
    print("")

    return debug_dirs



def analyze_debug(debug_path):
    """
    Parse debug files
    """

    parser = prof.debug.DebugParser(debug_path)
    ds     = parser.parse()

    return ds



def load_debug(debug_path):
    """
    Load previously parserd debug files
    """

    with open(join(debug_path, "directory_stream.pkl"), "rb") as f:
        return pkl.load(f)



def run_pickle_debug(parser, args):
    """
    Go over debug hireachy, parse the directory streams, and pickle the result
    in the same directory.
    """

    targets = find_debug(args.path)

    over = OverwriteLast()

    for i, run in enumerate(targets):
        over.print(f"Analyzing {i}/{len(targets)}: {run}")
        ds = analyze_debug(run)

        with open(join(run, "directory_stream.pkl"), "wb") as f:
            pkl.dump(ds, f)

    over.print("Analyzing: Done!")
    print("")



def run_archive(parser, args):
    """
    Go over the debug hireachy, and copy all debug directories to a new location.
    """

    parser.add_argument("dest", type=str)
    args, _ = parser.parse_known_args()

    root    = args.path
    targets = find_debug(root)
    dest    = args.dest

    over = OverwriteLast()

    for i, run in enumerate(targets):
        over.print(f"Copying {i}/{len(targets)}: {run} to {dest}")
        rp = relpath(run, root)
        copytree(run, join(dest, rp))

    over.print("Copying: Done!")
    print("")



def run_statistics(parser, args):
    """
    Go over the debug hirearchy and compute statistics
    """

    parser.add_argument("--pickle", action="store_true")
    args, _ = parser.parse_known_args()

    targets = find_debug(args.path)

    over = OverwriteLast()

    stats = {
        "start": 0,
        "spotfind_start": 0, 
        "index_start": 0,
        "refine_start": 0,
        "integrate_start": 0,
        "ok": 0
    }

    for i, run in enumerate(targets):
        over.print(f"Analyzing {i}/{len(targets)}: {run}")

        if args.pickle:
            ds = load_debug(run)
        else:
            ds = analyze_debug(run)

        for es in ds.event_streams:
            for ev in es:
                stats["start"] += 1
                for eo in ev.event_order:
                    stats[eo] += 1
                if ev.ok:
                    stats["ok"] += 1


    over.print("Analyzing: Done!")
    print("")

    with open("stats.json", "w") as f:
        js.dump(stats, f)

    for elt in stats:
        print(f"{elt: <16}: {stats[elt]}")



parser = ArgumentParser()
parser.add_argument("mode", type=str)
parser.add_argument("path", type=str)


args, _ = parser.parse_known_args()
mode = args.mode


if mode == "pickle":
    run_pickle_debug(parser, args)

if mode == "archive":
    run_archive(parser, args)

if mode == "statistics":
    run_statistics(parser, args)
