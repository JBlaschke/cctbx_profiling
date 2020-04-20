#!/usr/bin/env python
# -*- coding: utf-8 -*-


#TODO: change name => "stream" is not appropriate
class DirectoryStream(object):

    def __init__ (self, root):
        self._root          = root
        self._event_streams = list()

        # gets set once the first event has been added
        self._first = None

        # gets set to True after the first run or `compute_stats`
        self._has_stats = False;



    def add(self, event_stream):
        # track first element
        if self.first == None:
            self._first = event_stream.first
        else:
            if event_stream.first < self.first:
                self._first = event_stream.first

        self._event_streams.append(event_stream)


    @property
    def root(self):
        return self._root


    @property
    def event_streams(self):
        return self._event_streams


    @property
    def first(self):
        return self._first

    @property
    def has_stats(self):
        return self._has_stats


    @property
    def good_diff(self):
        return self._good_diff


    @property
    def failed_diff(self):
        return self._failed_diff


    @property
    def good_duration(self):
        return self._good_duration


    @property
    def failed_duration(self):
        return self._failed_duration


    def compute_stats(self):

        isgood   = lambda x: x.status == "done"

        self._good_diff       = list()
        self._good_duration   = list()
        self._failed_diff     = list()
        self._failed_duration = list()

        for es in self.event_streams:
            es.compute_stats()

            for i in range(len(es) - 1):
                if isgood(es[i]) and isgood(es[i + 1]):
                    self._good_diff.append(es.diff[i])
                else:
                    self._failed_diff.append(es.diff[i])

            for ev in es:
                if isgood(ev):
                    self._good_duration.append(ev.duration)
                else:
                    self._failed_duration.append(ev.duration)

        self._has_stats = True


    def __repr__(self):
        n_events = len(self.event_streams)

        str_repr =  f"DirectoryStream({self.root}):"
        str_repr += f"\n +-> containing {n_events} EventStreams"
        str_repr += f"\n |=> first Event:"
        str_repr += f"{self.first}"

        return str_repr

    def __getitem__(self, key):
        return self._event_streams[key]
