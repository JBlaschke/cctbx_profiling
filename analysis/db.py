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
    def timers(self):
        return tuple(finish for _, _, _, finish, _ in self._data)


    @property
    def good_timers(self):
        return tuple(finish for good, _, _, finish, _ in self._data if good)


    @property
    def fail_timers(self):
        return tuple(finish for good, _, _, finish, _ in self._data if not good)


    @property
    def ranks(self):
        return tuple(rank for _, rank, _, _, _ in self._data)


    @property
    def good_ranks(self):
        return tuple(rank for good, rank, _, _, _ in self._data if good)


    @property
    def fail_ranks(self):
        return tuple(rank for good, rank, _, _, _ in self._data if not good)


    @property
    def eqs(self):
        return tuple(tuple([s, *ss, f]) for _, _, s, f, ss in self._data)


    @property
    def good_eqs(self):
        return tuple(tuple([s, *ss, f]) for g, _, s, f, ss in self._data if g)


    @property
    def fail_eqs(self):
        return tuple(tuple([s, *ss, f]) for g, _, s, f, ss in self._data if not g)



class EventQueueDB(DebugDB):

    def __init__(self, ds):
        super().__init__(ds)

        self._eqs = tuple(
                EventQueue(tuple([start, *steps, finish]), good, rank)
                for good, rank, start, finish, steps in self._data
            )

        self._end = -1  # TODO: use a max value instead


    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, value):
        self._end = value
        for eq in self._eqs:
            eq.end = value


    @property
    def starts(self):
        return tuple(eq.start for eq in self._eqs)


    @property
    def good_starts(self):
        return tuple(eq.start for eq in self._eqs if eq.good)


    @property
    def finishes(self):
        return tuple(eq.end for eq in self._eqs)


    @property
    def good_finishes(self):
        return tuple(eq.end for eq in self._eqs if eq.good)


    @property
    def fail_starts(self):
        return tuple(eq.start for eq in self._eqs if not eq.good)


    @property
    def fail_finishes(self):
        return tuple(eq.end for eq in self._eqs if not eq.good)


    @property
    def eqs(self):
        return tuple(eq for eq in self._eqs)


    @property
    def good_eqs(self):
        return tuple(eq for eq in self._eqs if eq.good)


    @property
    def fail_eqs(self):
        return tuple(eq for eq in self._eqs if not eq.good)
