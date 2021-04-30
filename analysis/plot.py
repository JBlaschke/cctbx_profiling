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

        # currently this only works with up to 5 colors
        color_map = [
            (1,   0,   0,   1),
            (0,   1,   0,   1),
            (0,   0,   1,   1),
            (0,   0.5, 0.5, 1),
            (0,   0,   0,   1)
        ]

        _lines  = list()
        _colors = list()

        for rank, eq in zip(self.db.good_ranks, self.db.good_eqs):
            for i in range(len(eq) - 1):
                _lines.append(
                    ((eq[i], rank), (eq[i+1], rank))
                )
                _colors.append(color_map[i])

        for rank, eq in zip(self.db.fail_ranks, self.db.fail_eqs):
            for i in range(len(eq) - 1):
                _lines.append(
                    ((eq[i], rank), (eq[i+1], rank))
                )
                _colors.append(color_map[i])

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
