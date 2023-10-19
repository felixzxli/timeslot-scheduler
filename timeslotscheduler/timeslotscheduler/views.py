from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from . import waterloo
from scheduler import scheduler, test


@api_view(["GET", "POST"])
def schedule(request):
    if request.method == "GET":
        # expect a list of course codes
        course_codes = request.query_params.getlist("course")
        term_code = waterloo.get_current_term()
        classes = waterloo.get_class_info_list(course_codes, term_code)
        schedule = scheduler.schedule(classes, None, None)
        return Response(schedule)

    elif request.method == "POST":
        return Response("nothing at the moment", status=status.HTTP_400_BAD_REQUEST)
