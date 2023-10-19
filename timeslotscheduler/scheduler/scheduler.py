import itertools
from pprint import pprint
from collections import deque

# from . import test
import test


class Scheduler:
    def __init__(self) -> None:
        pass


# brute force algorithm
# input:
#       dictionary courses: {courseID: [[timeslot1, timeslot2, ...], [days]] ...}
#               where timeslot is of the form [startTime, endTime, days],
#               days is of the form, for example, [1, 2, 3, 7]
#                   for Mon, Tues, Wed, and Sun,
#               and startTime and endTime are in minutes [0, 1440)
#       list blockcades: [[start, end]]
#               of blockades
# output: {courseID: [timeslot, days]} (dict of timeslots with days in an optimal order)
# TODO: add tolerance, blockades, etc
def schedule(courses, tolerance, blockcades):
    values = list(courses.values())
    timeslot_list = []
    for [timeslots, days] in values:
        row = []
        for timeslot in timeslots:
            row.append((timeslot, days))
        timeslot_list.append(row)

    solns = list(itertools.product(*timeslot_list))
    # pprint(solns)
    minDistance = float("inf")
    optimal_soln = -1
    for i, soln in enumerate(solns):
        sorted_soln = sorted(soln, key=lambda x: x[0][0])  # x is [timeslot, day]
        total_dist = 0
        # pprint(soln)
        # print("\n")
        for day in range(1, 8):
            lastend = 0
            dist = 0
            for [interval, days] in sorted_soln:
                if day not in days:
                    continue
                if interval[0] < lastend:
                    dist = float("inf")
                    break
                dist += interval[0] - lastend
                lastend = interval[1]

            total_dist += dist

        if total_dist < minDistance:
            minDistance = total_dist
            optimal_soln = i

    if optimal_soln < 0:
        return None
    else:
        schedule = solns[optimal_soln]
        ret = {}
        for i, course_id in enumerate(courses.keys()):
            ret[course_id] = schedule[i]
        return ret


# lists = test.get_list1()
# ret = schedule(lists, None, None)
# pprint(ret)
