import requests
from django.conf import settings

API_ROOT = "https://openapi.data.uwaterloo.ca/v3/"


def get_current_term():
    url = API_ROOT + "Terms/current"
    headers = {"accept": "application/json", "x-api-key": settings.WATERLOO_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data["termCode"]
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None


# input:
#       list of string courses: [subject ID (eg "CS 486"), ...]
# output: {courseID: [timeslot, days]} (dict of timeslots with days in an optimal order)
#       dictionary courses: {courseID: [[timeslot1, timeslot2, ...], [days]] ...}
#               where timeslot is of the form [startTime, endTime, days],
#               days is of the form, for example, [1, 2, 3, 7]
#                   for Mon, Tues, Wed, and Sun,
#               and startTime and endTime are in minutes [0, 1440)
def get_class_info_list(course_list):
    res = {}
    for course in course_list:
        requests.get("external_api_url")


get_current_term()
