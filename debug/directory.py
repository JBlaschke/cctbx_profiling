#!/usr/bin/env python
# -*- coding: utf-8 -*-



class DirectoryStream(object):

    def __init__ (self, root):
        self._root          = root
        self._event_streams = list()
        self._first         = None


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


    def __repr__(self):
        n_events = len(self.event_streams)

        str_repr =  f"DirectoryStream({self.root}):"
        str_repr += f"\n +-> containing {n_events} EventStreams"
        str_repr += f"\n |=> first Event:"
        str_repr += f"{self.first}"

        return str_repr