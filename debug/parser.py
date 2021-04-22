#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from .event import Event, EventStream
from .gears import reverse_timestamp
from .directory import DirectoryStream



class EventParser(object):

    @staticmethod
    def scan_event(lines):

        parse_ok    = True
        end_index   = 0
        event_lines = list()

        if len(lines) == 0:
            parse_ok = False

        for i, line in enumerate(lines):
            line_fields = line.strip().split(',')
            if len(line_fields) == 5:
                hostname, psanats, ts, status, result = line_fields
            else:
                # I/O error mangled the file => de-validate the entire entry
                parse_ok = False
                continue

            event_lines.append((hostname, psanats, ts, status, result))

            if status in ("stop", "done", "fail"):
                end_index = i
                break

        return end_index, parse_ok, event_lines



    @staticmethod
    def get_time(ts):
        sec, ms = reverse_timestamp(ts)
        return sec + ms*1.e-3


    def __init__(self, root, file_name):

        self._stages = (
                "start",
                "spotfind_start",
                "index_start",
                "refine_start",
                "integrate_start"
            )

        self._valid     = False
        self._file_name = file_name
        self._root      = root

        if os.path.splitext(file_name)[1] != '.txt': return
        if 'debug' not in file_name: return

        self._valid = True
        self._rank  = int(file_name.split('_')[1].split('.')[0])

        with open(os.path.join(self.root, self.file_name)) as f:
            self._lines = f.readlines()

        self.scan_lines()
        self.scan_index()
        self.validate_lines()


    def scan_lines(self):

        # FMT: (True, is_start, is_end, N, hostname, psanats, ts, status, result)
        #  OR: (False, -1, line)
        self._idx = list()
        for i, line in enumerate(self.lines):
            line_fields = line.strip().split(',')
            if len(line_fields) == 5:
                hostname, psanats, ts, status, result = line_fields
            else:
                # I/O error mangled the file => de-validate the entire entry
                self._idx.append([False, -1, line])
                continue

            event_start = True if result == "start" else False
            event_end = True if status in ("stop", "done", "fail") else False

            time_stamp = EventParser.get_time(ts)

            self._idx.append(
                    [True, event_start, event_end, -1,
                        hostname, psanats, time_stamp , status, result
                    ]
                )


    def scan_index(self):

        self._idx_start = list()
        for i, idx in enumerate(self._idx):
            if idx[0] and idx[1]:
                self._idx_start.append(i)

        self._idx_end = list()
        for idx in self._idx_start[1:]:
            self._idx_end.append(idx - 1)
        self._idx_end.append(len(self.lines) - 1)


    def validate_event(self, i, n_evt):

        evt_ok = True
        start  = self._idx_start[i]
        end    = self._idx_end[i]
        for j in range(start, end+1):
            idx = self._idx[j]
            if not idx[0]:
                evt_ok = False
                break

        if not evt_ok:
            for j in range(start, end+1):
                self._idx[j][0] = False
            return 0

        for j in range(start, end+1):
            self._idx[j][3] = n_evt

        return 1



    def validate_lines(self):

        n_evt = 0
        for i in range(len(self._idx_start)):
            n_evt += self.validate_event(i, n_evt)


    @property
    def valid(self):
        return self._valid


    @property
    def file_name(self):
        return self._file_name


    @property
    def root(self):
        return self._root


    @property
    def rank(self):
        return self._rank


    @property
    def lines(self):
        return self._lines


    def __repr__(self):
        if self.valid:
            return f"EventParser({self.root}, {self.file_name} | {self.rank}, {self.valid})"
        else:
            return f"EventParser({self.root}, {self.file_name} | {self.valid})"


    def parse(self):

        events = EventStream(self.rank)

        for i, (start, end) in enumerate(zip(self._idx_start, self._idx_end)):
            if not self._idx[start][0]:
                continue

            start_time = self._idx[start][6]
            end_time   = self._idx[end][6]

            ev = Event(start_time, end_time)
            ev.hostname = self._idx[start][4]
            ev.psanats  = self._idx[start][5]
            ev.status   = self._idx[end][7]
            ev.result   = self._idx[end][8]

            for j, stage_idx in enumerate(range(start+1, end), 1):
                setattr(ev, self._stages[j], self._idx[stage_idx][6])

            ev.lock()
            events.add(ev)

        # TODO: what will we do with "broken" events?

        return events



class DebugParser(object):

    def __init__(self, root, verbose=False):
        self._root = root
        self._directory_stream = DirectoryStream(root)
        self.verbose = verbose


    def parse(self):
        directory_stream = DirectoryStream(self.root)

        for file_name in os.listdir(self.root):
            par = EventParser(self.root, file_name)

            if par.valid:
                directory_stream.add(par.parse())
            else:
                if self.verbose:
                    print(f"Skipping: {par}")

        return directory_stream


    @property
    def root(self):
        return self._root


    @root.setter
    def root(self, value):
        self._root = value
        self._directory_stream = DirectoryStream(self.root)
