from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import *


def test(request):
    tests = Test.objects.all()
    return JsonResponse(serialize('json', tests), safe=False)


# Datum a cas; Parkoviste; Obsazenost; Kapacita
def analyze_data():
    pass
