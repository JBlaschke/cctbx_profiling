#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .db        import DebugDB
from matplotlib import collections as mc


class DebugPlot(object):

    def __init__(self, db, good_color="g", fail_color="b",
                 line_width=0.1, marker_size=0.2):

        self._db = db

        # settings and stuff
        self._good_color  = good_color
        self._fail_color  = fail_color
        self._line_width  = line_width
        self._marker_size = marker_size


    @property
    def db(self):
        return self._db


    @property
    def lines(self):
        _lines  = list()
        _colors = list()
        for rank, eq in zip(self.db.good_ranks, self.db.good_eqs):
            # assumes that self.good_eqs[:] each have a lenght of 5
            _lines += [
                ((eq[0], rank), (eq[1], rank)),
                ((eq[1], rank), (eq[2], rank)),
                ((eq[2], rank), (eq[3], rank)),
                ((eq[3], rank), (eq[4], rank))
            ]
            _colors += [
                (1, 0, 0, 1),
                (0, 1, 0, 1),
                (0, 0, 1, 1),
                (0, 0, 0, 1)
            ]

        return mc.LineCollection(_lines, colors=_colors,
                                 linewidths=self._line_width)


    def weatherplot(self, ax):
        ax.plot(self.db.good_timers, self.db.good_ranks,
                f"{self._good_color}.",
                linewidth=self._line_width,
                markersize=self._marker_size)

        ax.plot(self.db.fail_timers, self.db.fail_ranks,
                f"{self._fail_color}.",
                linewidth=self._line_width,
                markersize=self._marker_size)


    def lineplot(self, ax):
        ax.add_collection(self.lines)
        ax.autoscale()
        ax.margins(0.1)
