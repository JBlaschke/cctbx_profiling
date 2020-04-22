#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DebugDB(object):

    def __init__(self, ds):
        self.directory_stream = ds


    @property
    def directory_stream(self):
        return self._ds


    @directory_stream.setter
    def directory_stream(self, value):
        self._ds = value

        self._ds.compute_stats()
        reference = self._ds.first.start

        # build internal database
        self._good_timers = list()
        self._good_ranks  = list()
        self._fail_timers = list()
        self._fail_ranks  = list()
        self._good_eqs    = list()
        self._fail_eqs    = list()
        for es in self.directory_stream:
            for ev in es:
                if ev.ok:
                    self._good_timers.append(ev.finish - reference)
                    self._good_ranks.append(es.rank)
                    eq = [ev.start - reference]
                    for offset in ev.event_offsets:
                        eq.append(ev.start - reference + offset)
                    eq.append(ev.finish - reference)
                    self._good_eqs.append(eq)
                else:
                    self._fail_timers.append(ev.finish - reference)
                    self._fail_ranks.append(es.rank)
                    eq = [ev.start - reference]
                    for offset in ev.event_offsets:
                        eq.append(ev.start - reference + offset)
                    eq.append(ev.finish - reference)
                    self._fail_eqs.append(eq)


    @property
    def good_timers(self):
        return self._good_timers


    @property
    def fail_timers(self):
        return self._fail_timers


    @property
    def good_ranks(self):
        return self._good_ranks


    @property
    def fail_ranks(self):
        return self._fail_ranks


    @property
    def good_eqs(self):
        return self._good_eqs


    @property
    def fail_eqs(self):
        return self._fail_eqs

