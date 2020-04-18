#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from .event import Event, EventStream
from .gears import reverse_timestamp



class EventParser(object):

    @staticmethod
    def scan_event(lines, offset):

        event_ok    = True
        end_index   = 0
        event_lines = list()

        for i, line in enumerate(lines, offset):

            try:
                hostname, psanats, ts, status, result = line.strip().split(',')
            except ValueError:
                # I/O error mangled the file => de-validate the entire entry
                event_ok = False
                continue

            event_lines.append((hostname, psanats, ts, status, result))

            if status in ['stop', 'done', 'fail']:
                end_index = i
                break

        return end_index, event_ok, event_lines


    @staticmethod
    def filter_result(event_data, target):

        for hostname, psanats, ts, status, result  in event_data:
            if result in target:
                return hostname, psanats, ts, status, result

        return None


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

        self._valid = False

        if os.path.splitext(file_name)[1] != '.txt': return
        if 'debug' not in file_name: return

        self._file_name = file_name
        self._root      = root
        self._rank      = int(file_name.split('_')[1].split('.')[0])

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


    def parse(self):

        offset     = 0
        events_raw = list()

        while True:
            end_index, event_ok, event_lines \
                = self.scan_event(self.lines[offset:], offset)

            if event_ok:
                events_raw.append(event_lines)

            offset += end_index + 1  # +1 => point the offest at the _next_ index
            if offset > len(self.lines):
                break

        events = EventStream(self.rank)

        for event_raw in events_raw:

            hostname, psanats, ts_start, status, result \
                = self.filter_result(event_raw, "start")

            start_time = self.get_time(ts_start)

            hostname, psanats, ts_finish, status, result \
                = self.filter_status(event_raw, ["stop", "done", "fail"])

            finish_time = self.get_time(ts_finish)

            ev = Event(start_time, finish_time)
            ev.hostname = hostname
            ev.psanats  = psanats
            ev.status   = status

            hostname, psanats, ts, status, result \
                = self.filter_result(event_raw, "spotfind_start")
            ev.spotfind_start = self.get_time(ts)

            hostname, psanats, ts, status, result \
                = self.filter_result(event_raw, "index_start")
            ev.index_start = self.get_time(ts)

            hostname, psanats, ts, status, result \
                = self.filter_result(event_raw, "refine_start")
            ev.refine_start = self.get_time(ts)

            hostname, psanats, ts, status, result \
                = self.filter_result(event_raw, "integrate_start")
            ev.integrate_start = self.get_time(ts)

            ev.ok = True
            ev.lock()

            events.add(ev)


        # TODO: what will we do with "broken" events?


        return events



class DirectoryStream(object):

    def __init__ (self, root):
        self._root = root
        self._event_streams = list()


    def add(self, event_stream):
        self._event_streams.append(event_stream)


    @property
    def root(self):
        return self._root


    @property
    def event_streams(self):
        return self._event_streams



class DebugParser(object):

    def __init__(self, root):
        self._root = root
        self._directory_stream = DirectoryStream(root)


    def parse(self):

        par = parser.EventParser(self.root, "debug_2.txt")


    @property
    def root(self):
        return self._root


    @root.setter
    def root(self, value):
        self._root = value
