#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import collections as mc


class DebugPlot(object):

    def __init__(self, ds, good_color="g", fail_color="b",
                 line_width=0.1, marker_size=0.2):

        self.directory_stream = ds

        # settings and stuff
        self._good_color  = good_color
        self._fail_color  = fail_color
        self._line_width  = line_width
        self._marker_size = marker_size


    @property
    def directory_stream(self):
        return self._ds


    @directory_stream.setter
    def directory_stream(self, value):
        self._ds = value

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
                    self._good_eqs.append(eq)
                else:
                    self._fail_timers.append(ev.finish - reference)
                    self._fail_ranks.append(es.rank)
                    eq = [ev.start - reference]
                    for offset in ev.event_offsets:
                        eq.append(ev.start - reference + offset)
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


    @property
    def lines(self):
        _lines  = list()
        _colors = list()
        for rank, eq in zip(self.good_ranks, self.good_eqs):
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
        ax.plot(self.good_timers, self.good_ranks,
                f"{self._good_color}.",
                linewidth=self._line_width,
                markersize=self._marker_size)

        ax.plot(self.fail_timers, self.fail_ranks,
                f"{self._fail_color}.",
                linewidth=self._line_width,
                markersize=self._marker_size)


    def lineplot(self, ax):
        ax.add_collection(self.lines)
        ax.autoscale()
        ax.margins(0.1)
