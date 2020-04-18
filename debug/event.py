#!/usr/bin/env python
# -*- coding: utf-8 -*-



class WriteToLockedEventError(Exception):
    pass


class Event(object):


    def __init__(self, start_time, finish_time):
        self._start  = start_time
        self._finish = finish_time
        self._locked = False


    def lock(self):
        self._locked = True


    @property
    def locked(self):
        return self._locked


    @property
    def start(self):
        return self._start


    @property
    def finish(self):
        return self._finish


    @property
    def ok(self):
        return self._ok


    @ok.setter
    def ok(self, value):
        if not self._locked:
            self._ok = value
        else:
            raise WriteToLockedEventError()


    @property
    def spotfind_start(self):
        return self._spotfind_start


    @spotfind_start.setter
    def spotfind_start(self, value):
        if not self._locked:
            self._spotfind_start = value
        else:
            raise WriteToLockedEventError()


    @property
    def index_start(self):
        return self._index_start


    @index_start.setter
    def index_start(self, value):
        if not self._locked:
            self._index_start = value
        else:
            raise WriteToLockedEventError()


    @property
    def refine_start(self):
        return self._refine_start


    @refine_start.setter
    def refine_start(self, value):
        if not self._locked:
            self._refine_start = value
        else:
            raise WriteToLockedEventError()


    @property
    def integrate_start(self):
        return self._integrate_start


    @integrate_start.setter
    def integrate_start(self, value):
        if not self._locked:
            self._integrate_start = value
        else:
            raise WriteToLockedEventError()


    @property
    def hostname(self):
        return self._hostname


    @hostname.setter
    def hostname(self, value):
        if not self._locked:
            self._hostname = value
        else:
            raise WriteToLockedEventError()


    @property
    def psanats(self):
        return self._psanats


    @psanats.setter
    def psanats(self, value):
        if not self._locked:
            self._psanats = value
        else:
            raise WriteToLockedEventError()


    @property
    def status(self):
        return self._status


    @status.setter
    def status(self, value):
        if not self._locked:
            self._status = value
        else:
            raise WriteToLockedEventError()


    def __repr__(self):

        str_repr =  f"Event({self.start}, {self.finish})"

        if hasattr(self, "spotfind_start"):
            str_repr += f"\n  +-> spotfind_start = {self.spotfind_start}"

        if hasattr(self, "index_start"):
            str_repr += f"\n  +-> index_start = {self.index_start}"

        if hasattr(self, "refine_start"):
            str_repr += f"\n  +-> refine_start = {self.refine_start}"

        if hasattr(self, "integrate_start"):
            str_repr += f"\n  +-> integrate_start = {self.integrate_start}"

        if hasattr(self, "hostname"):
            str_repr += f"\n  +-> hostname = {self.hostname}"

        if hasattr(self, "psanats"):
            str_repr += f"\n  +-> psanats = {self.psanats}"

        if hasattr(self, "status"):
            str_repr += f"\n  +-> status = {self.status}"

        str_repr += f"\n  +-> is locked = {self.locked}"

        return str_repr


    def __lt__(self, other):
        return self.start < other.start



class EventStream(object):

    def __init__(self, rank):
        self._rank   = rank
        self._events = list()
        self._first  = None;


    def add(self, event):
        self._events.append(event)


    @property
    def rank(self):
        return self._rank


    @property
    def events(self):
        return self._events


    def __repr__(self):
        str_repr = f"Events on {self.rank}: ["
        for event in self.events:
            str_repr += f"\n{event}"
        str_repr += "]"

        return str_repr


    def __getitem__(self, key):
        return self._events[key]

