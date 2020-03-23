#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import strptime



def reverse_timestamp(timestamp):
    """Reverse of the xfel.cxi.cspad_ana.cspad_tbx.evt_timestamp()
    function.  From a string representation of a timestamp, @p
    timestamp, return the Unix time as a tuple of seconds and
    milliseconds.

    @param timestamp Human-readable ISO 8601 timestamp in string
                   representation
    @return          Tuple of the Unix time in seconds and milliseconds
    """

    tokens = timestamp.split('.')
    gmtime_tuple = strptime(tokens[0] + " UTC", '%Y-%m-%dT%H:%MZ%S %Z')
    return (timegm(gmtime_tuple), float(tokens[1]))
