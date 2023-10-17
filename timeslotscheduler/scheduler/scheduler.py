import itertools
from pprint import pprint
from collections import deque
from test import get_lists


class Scheduler:
    def __init__(self) -> None:
        pass


# brute force algorithm
# input:
#       dictionary courses: {courseID: [timeslot1, timeslot2, ...] ...}
#               where timeslot is of the form [startTime, endTime]
#               and startTime and endTime are in minutes [0, 1440)
#       list blockcades: [[start, end]]
#               of blockades
# output: {courseID: timeslot} (array of timeslots in an optimal order)
def schedule(courses, tolerance, blockcades):
    timeslot_list = list(courses.values())
    solns = list(itertools.product(*timeslot_list))
    minDistance = float("inf")
    optimal_soln = -1
    for i, soln in enumerate(solns):
        soln = sorted(soln, key=lambda x: x[0])
        lastend = 0
        dist = 0
        # pprint(soln)
        # print("\n")
        for interval in soln:
            if interval[0] < lastend:
                dist = float("inf")
                break
            dist += interval[0] - lastend
            lastend = interval[1]

        if dist < minDistance:
            minDistance = dist
            optimal_soln = i

    if optimal_soln < 0:
        return None
    else:
        schedule = solns[optimal_soln]
        ret = {}
        for i, course_id in enumerate(courses.keys()):
            ret[course_id] = schedule[i]
        pprint(ret)
        return ret


courses = {
    "cs": [[500, 600], [100, 200]],
    "math123": [[100, 200], [300, 400]],
}
schedule(courses, None, None)

# lists = get_lists()
# pprint(lists)
# schedule(lists, None, None)
