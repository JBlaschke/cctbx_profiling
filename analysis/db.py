#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .eq import EventQueue



class DebugDB(object):

    def __init__(self, ds):

        ds.compute_stats()
        if not ds.empty:
            self._reference = ds.first.start
        else:
            self._reference = 0.

        ds_data = list()

        for es in ds:
            for ev in es:
                ev_start  = ev.start - self._reference
                ev_steps  = tuple(ev_start + offset for offset in ev.event_offsets)
                ev_finish = ev.finish - self._reference
                ev_rank   = es.rank
                ev_good   = ev.ok
                ds_data.append((ev_good, ev_rank, ev_start, ev_finish, ev_steps))

        self._data = tuple(ds_data)


    @property
    def reference(self):
        return self._reference


    @property
    def data(self):
        return self._data


    @property
    def good_timers(self):
        return tuple(finish for good, _, _, finish, _ in self._data if good)


    @property
    def fail_timers(self):
        return tuple(finish for good, _, _, finish, _ in self._data if not good)


    @property
    def good_ranks(self):
        return tuple(rank for good, rank, _, _, _ in self._data if good)


    @property
    def fail_ranks(self):
        return tuple(rank for good, rank, _, _, _ in self._data if not good)


    @property
    def good_eqs(self):
        return tuple(tuple([s, *ss, f]) for g, _, s, f, ss in self._data if g)


    @property
    def fail_eqs(self):
        return tuple(tuple([s, *ss, f]) for g, _, s, f, ss in self._data if not g)



class EventQueueDB(DebugDB):

    def __init__(self, ds):
        super().__init__(ds)

        self.__good_eqs       = list()
        self.__good_starts    = list()
        self.__good_finishes  = list()
        for eq, rank in zip(super().good_eqs, super().good_ranks):
            self.__good_eqs.append(EventQueue(eq, True, rank))
            self.__good_starts.append(eq[0])
            self.__good_finishes.append(eq[-1])

        self.__fail_eqs       = list()
        self.__fail_starts    = list()
        self.__fail_finishes  = list()
        for eq, rank in zip(super().fail_eqs, super().fail_ranks):
            self.__fail_eqs.append(EventQueue(eq, False, rank))
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
