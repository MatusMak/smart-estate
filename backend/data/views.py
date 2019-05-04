from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import *
from .detection.detector import Detector


def test(request):
    tests = Test.objects.all()
    return JsonResponse(serialize('json', tests), safe=False)

# Datum a cas; Parkoviste; Obsazenost; Kapacita
def analyze_data():
    pass

def detect(request, lat, lon):
    detector = Detector()
    result = detector.detect(lat, lon)
    return JsonResponse(result, safe=False)
