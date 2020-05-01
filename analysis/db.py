#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .eq import EventQueue



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



class EventQueueDB(DebugDB):

    def __init__(self, ds):
        super().__init__(ds)

        self.__good_eqs       = list()
        self.__good_starts    = list()
        self.__good_finishes  = list()
        for eq in super().good_eqs:
            self.__good_eqs.append(EventQueue(eq, True))
            self.__good_starts.append(eq[0])
            self.__good_finishes.append(eq[-1])

        self.__fail_eqs       = list()
        self.__fail_starts    = list()
        self.__fail_finishes  = list()
        for eq in super().fail_eqs:
            self.__fail_eqs.append(EventQueue(eq, False))
            self.__fail_starts.append(eq[0])
            self.__fail_finishes.append(eq[-1])

        self._end = -1  # TODO: use a max value instead


    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, value):
        self._end = value
        for eq in self.__good_eqs:
            eq.end = value
        for eq in self.__fail_eqs:
            eq.end = value


    @property
    def good_starts(self):
        return self.__good_starts


    @property
    def good_finishes(self):
        return self.__good_starts


    @property
    def fail_starts(self):
        return self.__fail_starts


    @property
    def fail_finishes(self):
        return self.__fail_starts


    @property
    def good_eqs(self):
        return self.__good_eqs


    @property
    def fail_eqs(self):
        return self.__fail_eqs
