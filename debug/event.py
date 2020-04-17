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
