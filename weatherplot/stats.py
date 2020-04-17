#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WeatherStats(object):
    
    @staticmethod
    def compute_deltas(data_dict):

        good_deltas   = list()
        failed_deltas = list()

        for file_name in data_dict:

            data = data_dict[file_name]

            good_t   = data["good_x"]
            failed_t = data["failed_x"]

            good_deltas += [
                good_t[i+1] - good_t[i] for i in range(len(good_t) - 1)
            ]
            failed_deltas += [
                failed_t[i+1] - failed_t[i] for i in range(len(failed_t) - 1)
            ]

        return good_deltas, failed_deltas


    def __init__(self, data_dict):
        self.good_deltas, self.failed_deltas = self.compute_deltas(data_dict)
