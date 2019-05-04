from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from datetime import time

from .models import *


def test(request):
    tests = Test.objects.all()
    return JsonResponse(serialize('json', tests), safe=False)


# Datum a cas; Parkoviste; Obsazenost; Kapacita
def analyze_data():
    with open('data3.txt', 'r') as f:
        for line in f.readlines():
            temp = line.split(';')

            timeblock = temp[0].split()[1].split(':')
            timeblock = time(int(timeblock[0]), int(timeblock[1]), 0)
            timeslot = Timeslot.objects.filter(
                start__lte=timeblock,
                end__gte=timeblock,
            )
            print(timeblock)
            print(timeslot)

            name = temp[1][4:]
            full = int(temp[2])
            capacity = int(temp[3])
