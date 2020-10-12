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
            try:
                hostname, psanats, ts, status, result = line.strip().split(',')
            except ValueError:
                # I/O error mangled the file => de-validate the entire entry
                parse_ok = False
                continue

            event_lines.append((hostname, psanats, ts, status, result))

            if status in ["stop", "done", "fail"]:
                end_index = i
                break

        return end_index, parse_ok, event_lines


    @staticmethod
    def has_result(event_data, target):

        for hostname, psanats, ts, status, result  in event_data:
            if result in target:
                return True

        return False


    @staticmethod
    def filter_result(event_data, target):

        for hostname, psanats, ts, status, result  in event_data:
            if result in target:
                return hostname, psanats, ts, status, result

        return None


    @staticmethod
    def has_status(event_data, target):

        for hostname, psanats, ts, status, result  in event_data:
            if status in target:
                return True

        return False


    @staticmethod
    def filter_status(event_data, target):

        for hostname, psanats, ts, status, result  in event_data:
            if status in target:
                return hostname, psanats, ts, status, result

        return None


    @staticmethod
    def get_time(ts):
        sec, ms = reverse_timestamp(ts)
        return sec + ms*1.e-3


    def __init__(self, root, file_name):

        self._valid     = False
        self._file_name = file_name
        self._root      = root

        if os.path.splitext(file_name)[1] != '.txt': return
        if 'debug' not in file_name: return

        self._valid = True
        self._rank  = int(file_name.split('_')[1].split('.')[0])

        with open(os.path.join(self.root, self.file_name)) as f:
            self._lines = f.readlines()


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

        offset     = 0
        events_raw = list()

        while True:
            end_index, parse_ok, event_lines \
                = self.scan_event(self.lines[offset:])

            if parse_ok:
                events_raw.append(event_lines)

            # TODO: collect stats on events that could not be parsed

            offset += end_index + 1  # +1 => point the offest at the _next_ index
            if offset > len(self.lines):
                break

        events = EventStream(self.rank)

        for event_raw in events_raw:
            result = self.filter_result(event_raw, ["start"])
            if result is None:
                continue
            hostname, psanats, ts_start, status, result = result

            start_time = self.get_time(ts_start)

            status = self.filter_status(event_raw, ["stop", "done", "fail"])
            if status is None:
                continue
            hostname, psanats, ts_finish, status, result = status

            finish_time = self.get_time(ts_finish)

            ev = Event(start_time, finish_time)
            ev.hostname = hostname
            ev.psanats  = psanats
            ev.status   = status

            if self.has_result(event_raw, ["spotfind_start"]):
                hostname, psanats, ts, status, result \
                    = self.filter_result(event_raw, ["spotfind_start"])
                ev.spotfind_start = self.get_time(ts)

            if self.has_result(event_raw, ["index_start"]):
                hostname, psanats, ts, status, result \
                    = self.filter_result(event_raw, ["index_start"])
                ev.index_start = self.get_time(ts)

            if self.has_result(event_raw, ["refine_start"]):
                hostname, psanats, ts, status, result \
                    = self.filter_result(event_raw, ["refine_start"])
                ev.refine_start = self.get_time(ts)

            if self.has_result(event_raw, ["integrate_start"]):
                hostname, psanats, ts, status, result \
                    = self.filter_result(event_raw, ["integrate_start"])
                ev.integrate_start = self.get_time(ts)

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
