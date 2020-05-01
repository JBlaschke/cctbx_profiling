#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EventQueue(object):

    def to_delta(self, t_in):
        if self.end < t_in[0]:
            return 0.
        elif self.end > t_in[1]:
            return t_in[1] - t_in[0]
        else:
            return self.end - t_in[0]


    def __init__(self, eq, good):
        self._good = good
        # self._good = not len(eq) == 6
        # initialize based on EQ from DebugDB
        self._spin_up  = (eq[0], eq[1])
        self._spotfind = (eq[1], eq[2])
        if self.good:
            self._index     = (eq[2], eq[3])
            self._refine    = (eq[3], eq[4])
            self._integrate = (eq[4], eq[5])
            self._post      = self._integrate
            self._end       = eq[5]
        else:
            self._index = (eq[1], eq[2])
            self._post  = self._index
            self._end   = eq[2]


    @property
    def end(self):
        return self._end


    @end.setter
    def end(self, value):
        self._end = value


    @property
    def good(self):
        return self._good


    @property
    def spin_up(self):
        return self.to_delta(self._spin_up)


    @property
    def spotfind(self):
        return self.to_delta(self._spotfind)


    @property
    def index(self):
        return self.to_delta(self._index)


    @property
    def refine(self):
        return self.to_delta(self._refine)


    @property
    def integrate(self):
        return self.to_delta(self._integrate)


    @property
    def post(self):
        return self.to_delta(self._post)

