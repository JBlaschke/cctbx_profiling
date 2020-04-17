#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from .event import Event
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
            end_index, event_ok, event_lines = self.scan_event(self.lines[offset:], offset)

            if event_ok:
                events_raw.append(event_lines)

            offset += end_index + 1
            if offset > len(self.lines):
                break

        return events_raw
