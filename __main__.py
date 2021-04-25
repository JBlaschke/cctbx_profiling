from sys     import argv
from os      import walk
from os.path import join, basename, relpath
from shutil  import copytree
from pickle  import dump

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
    Parse debug filder
    """

    parser = prof.debug.DebugParser(debug_path)
    ds     = parser.parse()

    return ds



if len(argv) < 3:
    raise Exception("I need at least two inputs")


mode = argv[1]


if mode == 'pickle':

    targets = find_debug(argv[2])

    over = OverwriteLast()

    for i, run in enumerate(targets):
        over.print(f"Analyzing {i}/{len(targets)}: {run}")
        ds = analyze_debug(run)

        with open(join(run, "directory_stream.pkl"), "wb") as f:
            dump(ds, f)

    over.print("Analyzing: Done!")
    print("")


if mode == "archive":

    root    = argv[2]
    targets = find_debug(root)
    dest    = argv[3]

    over = OverwriteLast()

    for i, run in enumerate(targets):
        over.print(f"Copying {i}/{len(targets)}: {run} to {dest}")
        rp = relpath(run, root)
        copytree(run, join(dest, rp))

    over.print("Copying: Done!")
    print("")
