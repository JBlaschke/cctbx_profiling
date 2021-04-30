#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EventQueue(object):

    def to_delta(self, t1, t2):

        if self.end < self._eq[t1]:
            return 0.
        elif self.end > self._eq[t2]:
            return self._eq[t2] - self._eq[t1]
        else:
            return self.end - self._eq[t1]


    def __init__(self, eq, good, rank):

        self._steps = (
            "spin_up",
            "spotfind",
            "index",
            "refine",
            "integrate"
        )

        self._good = good
        self._rank = rank
        self._eq   = eq

        # Events can have any number of steps
        self._end_index = 1
        self._spin_up = (0, 1)
        if len(eq) > 2:
            self._spotfind = (1, 2)
            self._post     = self._spotfind
            self._end_index = 2
        if len(eq) > 3:
            self._index = (2, 3)
            self._post  = self._index
            self._end_index = 3
        if len(eq) > 4:
            self._refine = (3, 4)
            self._post   = self._refine
            self._end_index = 4
        if len(eq) > 5:
            self._integrate = (4, 5)
            self._post      = self._integrate
            self._end_index = 5

        self._start = eq[0]
        self._end   = eq[self._end_index]


    @property
    def event_queue(self):
        return self._eq


    @property
    def start(self):
        return self._start


    @property
    def end(self):
        return self._end


    @property
    def good(self):
        return self._good


    @property
    def rank(self):
        return self._rank


    @property
    def spin_up(self):
        return self.to_delta(*self._spin_up)


    @property
    def spotfind(self):
        return self.to_delta(*self._spotfind)


    @property
    def index(self):
        return self.to_delta(*self._index)


    @property
    def refine(self):
        return self.to_delta(*self._refine)


    @property
    def integrate(self):
        return self.to_delta(*self._integrate)


    @property
    def post(self):
        return self.to_delta(*self._post)


    @property
    def end_index(self):
        return self._end_index


    @property
    def steps(self):
        return [step for step in self._steps[:self.end_index]]
