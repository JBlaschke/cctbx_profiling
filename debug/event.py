#!/usr/bin/env python
# -*- coding: utf-8 -*-



class WriteToLockedEventError(Exception):
    pass


class Event(object):


    def __init__(self, start_time, finish_time):
        self._start  = start_time
        self._finish = finish_time
        self._locked = False

        self._inner_steps = [
            "spotfind_start",
            "index_start",
            "refine_start",
            "integrate_start"
        ]

        self._isgood = lambda x: x.status == "done"


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
        return self._isgood(self)


    @property
    def isgood(self):
        """ Lambda function used to test if an event is good """
        return self._isgood


    @isgood.setter
    def isgood(self, value):
        self._isgood = value


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


    @property
    def event_order(self):

        # get list of steps that actually are in this event
        steps = list()
        for step in self._inner_steps:
            if hasattr(self, step):
                steps.append(step)

        # sort steps
        steps.sort(key = lambda x:getattr(self, x))

        return steps


    @property
    def event_offsets(self):
        times = list()
        for step in self.event_order:
            times.append(getattr(self, step) - self.start)

        return times


    def __repr__(self):

        str_repr =  f"Event({self.start}, {self.finish})"

        for step in self._inner_steps:
            # Bit of a hack to build an f-string
            step_string = lambda field: "\n  +-> {step} = {self."+field+"}"
            if hasattr(self, step):
                step_str = step_string(step)
                str_repr += eval(f'f"""{step_str}"""')  # ergch

        if hasattr(self, "hostname"):
            str_repr += f"\n  +-> hostname = {self.hostname}"

        if hasattr(self, "psanats"):
            str_repr += f"\n  +-> psanats = {self.psanats}"

        if hasattr(self, "status"):
            str_repr += f"\n  +-> status = {self.status}"

        str_repr += f"\n  +-> is locked = {self.locked}"

        return str_repr


    def __lt__(self, other):
        """ This is true if self started before other """
        return self.start < other.start

    @property
    def duration(self):
        """ This returns the duration of the Event """
        return self.finish - self.start


    def __sub__(self, other):
        """ This returns the time between two events """

        # using this order to make it look like "minus" when doing:
        #   ev[1] - ev[0]
        return self.start - other.finish



class EventStream(object):

    def __init__(self, rank):
        self._rank   = rank
        self._events = list()

        # gets set once the first event has been added
        self._first = None;

        # gets set to True after the first run or `compute_stats`
        self._has_stats = False;


    def add(self, event):
        # track first element
        if self.first == None:
            self._first = event
        else:
            if event < self.first:
                self._first = event

        self._events.append(event)


    def sort(self):
        self._events.sort(key=lambda x: x.start)


    @property
    def rank(self):
        return self._rank


    @property
    def events(self):
        return self._events


    @property
    def first(self):
        return self._first


    @property
    def has_stats(self):
        return self._has_stats


    @property
    def diff(self):
        return self._diff


    @property
    def duration(self):
        return self._duration


    @property
    def good_total(self):
        return self._good_total


    @property
    def fail_total(self):
        return self._fail_total


    def compute_stats(self):
        # make sure that events are sorted
        self.sort()

        self._diff = list()
        self._good_total = 0
        self._fail_total = 0

        prev = self.events[0]
        for ev in self.events[1:]:
            delta = ev - prev
            prev  = ev
            self._diff.append(delta)


        self._duration = list()
        for ev in self.events:
            self._duration.append(ev.duration)
            if ev.ok:
                self._good_total += 1
            else:
                self._fail_total += 1

        self._has_stats = True


    def __repr__(self):
        str_repr = f"Events on {self.rank}: ["
        for event in self.events:
            str_repr += f"\n{event}"
        str_repr += "]"

        if hasattr(self, "first"):
            str_repr += f"\n|=> First Event:\n{self.first}"

        return str_repr


    def __len__(self):
        return len(self.events)


    def __getitem__(self, key):
        return self._events[key]
