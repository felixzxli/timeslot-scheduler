import requests
from django.conf import settings

API_ROOT = "https://openapi.data.uwaterloo.ca/v3/"

HEADERS = {"accept": "application/json", "x-api-key": settings.WATERLOO_API_KEY}


def to_minutes(hour, minutes):
    return 60 * hour + minutes


def get_current_term():
    url = API_ROOT + "Terms/current"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data["termCode"]
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


# input:
#       list of string courses: [subject ID (eg "CS 486"), ...]
# output: {courseID: [[timeslot, days]]} (dict of timeslots with days in an optimal order)
#               where timeslot is of the form [startTime, endTime],
#               days is of the form, for example, [1, 2, 3, 7]
#                   for Mon, Tues, Wed, and Sun,
#               and startTime and endTime are in minutes [0, 1440)
def get_class_info_list(course_list, term_code):
    if not term_code:
        term_code = get_current_term()

    res = {}
    for course in course_list:
        [subject, id] = course.split("_")
        url = API_ROOT + "ClassSchedules/" + term_code + "/" + subject + "/" + id
        print("url: " + url)
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            row = []
            data = response.json()
            for section in data:
                component = section["courseComponent"]
                if component != "LEC":
                    continue

                section_num = section["classSection"]
                start = section["scheduleData"][0]["classMeetingStartTime"]
                start_arr_str = start.split("T")[1].split(":")[0:2]
                start_arr = [int(x) for x in start_arr_str]
                start_min = to_minutes(start_arr[0], start_arr[1])

                end = section["scheduleData"][0]["classMeetingEndTime"]
                end_arr_str = end.split("T")[1].split(":")[0:2]
                end_arr = [int(x) for x in end_arr_str]
                end_min = to_minutes(end_arr[0], end_arr[1])

                days_str = section["scheduleData"][0]["classMeetingWeekPatternCode"]
                days = []
                for i, char in enumerate(days_str):
                    if char == "Y":
                        days.append(i + 1)  # 0 corresponds to Monday

                row.append([[start_min, end_min], days])

            res[course] = row

        else:
            print(
                f"Request failed with status code: {response.status_code} and message: {response.reason}"
            )
            return None

    return res
