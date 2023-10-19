from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from . import waterloo
from scheduler import scheduler, test


# request.data should contain courses
@api_view(["GET", "POST"])
def schedule(request):
    if request.method == "GET":
        # TODO: replace with scraper call
        # expect a list of course codes
        course_codes = request.query_params.getlist("course")
        classes = test.get_list1()
        schedule = scheduler.schedule(classes, None, None)
        term_code = waterloo.get_current_term()
        classes = waterloo.get_class_info_list()
        print(course_codes)

        # return Response(json.dumps(schedule))
        # return Response(course_codes)
        return Response(course_codes)

    elif request.method == "POST":
        return Response("nothing at the moment", status=status.HTTP_400_BAD_REQUEST)
