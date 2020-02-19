#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Webcron repeatedly sends http requests in predefined time intervals to predefined urls.
"""

import json
import time
import datetime
import urllib.request
import urllib.error

# loads the jobs.json file
def LoadJobs():
    with open('config/jobs.json', 'r') as jobsFile:
        return json.load(jobsFile)

# prints the jobs to the console
def PrintJobs(jobs: list):
    print("Jobs:")
    for job in jobs:
        print(" - {0}: {1}s \"{2}\"".format(job['name'], str(job['interval']), job['url']))

# prints the iterations to the console
def PrintIterations(iterations: list, interval: int):
    print("Iterations:")
    idx = 0
    for iteration in iterations:
        print(" - {0} ({1}s)".format(idx, idx*interval), end = '')
        for job in iteration:
            print(" {0},".format(job['name']), end = '')

        print()
        idx += 1

# calculates the gcd for 2 numbers
def Gcd(x: int, y: int):
   while(y):
       x, y = y, x % y

   return x

# calculates the gcd for a list of numbers
def GcdFromList(values: list):
    while len(values) > 1:
        # get the gcd form the first 2 elements
        value1 = values[0]
        value2 = values[1]
        gcd = Gcd(value1, value2)

        # remove all elements that are equal to the used values to compute the gcd and the gcd itself
        values = [x for x in values if x != value1]
        values = [x for x in values if x != value2]
        values = [x for x in values if x != gcd]

        # readd one element with the value of the gcd
        values = values + [gcd]

    # return the last existing value
    return values[0]

# build a 2 dimensional list that contains a list of jobs that should be executed per iteration
def BuildIterations(jobs: list, interval: int, maxInterval: int):
    iterations = []
    iteration = 1
    while iteration*interval <= maxInterval:
        iterations.append([job for job in jobs if job['interval']%(interval*iteration) == 0])
        iteration += 1

    return iterations

def SendRequest(url: str):
    print(" -> {0} => ".format(url), end = '')
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        print("{0}".format(response.getcode()))
    except urllib.error.HTTPError as e:
        print("{0}".format(e.getcode()))
    except urllib.error.URLError as e:
        print("{0}".format(e))

def main():
    jobs = LoadJobs()
    PrintJobs(jobs)

    # get a list of intervals
    intervals = []
    for job in jobs:
        intervals = intervals + [job['interval']]

    # get the maximum interval length, that hits every given interval
    interval = GcdFromList(intervals)

    # build the list of iterations of the interval
    iterations = BuildIterations(jobs, interval, max(intervals))
    PrintIterations(iterations, interval)

    print("Start sending the request. Interation interval = {0}s".format(interval))
    iteration = 0
    while True:
        date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("Iteration: {0}, Time: {1}".format(str(iteration), date))
        startTime = time.time()
        for job in iterations[iteration]:
            SendRequest(job['url'])

        duration = time.time() - startTime
        if (interval - duration > 0):
            time.sleep(interval-duration)
        else:
            print("WARNING: Sending the requests took longer than the interval time. Interval = {:.2f}s, Duration = {:.2f}s".format(interval, duration))

        iteration = (iteration+1)%len(iterations)

if __name__ == '__main__':
    main()