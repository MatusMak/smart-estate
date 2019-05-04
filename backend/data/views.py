from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist

from datetime import time

from .models import *
from .detection.detector import Detector


def test(request):
    tests = Test.objects.all()
    return JsonResponse(serialize('json', tests), safe=False)


# Datum a cas; Parkoviste; Obsazenost; Kapacita
def analyze_data():
    with open('data3.txt', 'r') as f:
        data = {}
        for line in f.readlines():
            temp = line.split(';')

            timeblock = temp[0].split()[1].split(':')
            timeblock = time(int(timeblock[0]), int(timeblock[1]), 0)
            if timeblock >= time(21):
                timeslot = 'night'
            elif timeblock >= time(18):
                timeslot = 'evening'
            elif timeblock >= time(15):
                timeslot = 'afternoon'
            elif timeblock >= time(13):
                timeslot = 'noon'
            elif timeblock >= time(10):
                timeslot = 'forenoon'
            elif timeblock >= time(6):
                timeslot = 'morning'
            else:
                timeslot = 'night'

            name = temp[1][4:]
            full = int(temp[2])
            capacity = int(temp[3])

            try:
                usage = data[name]['usage']
            except(KeyError):
                usage = {}
                data[name] = {
                    'capacity': capacity,
                    'usage': {}
                }

            try:
                usage[timeslot][0] += full
                usage[timeslot][1] += 1
            except(KeyError):
                usage[timeslot] = [full, 1]

            data[name]['usage'] = usage

    for parking in data:
        p = Parking.objects.create(
            name=parking,
            capacity=data[parking]['capacity'],
        )

        for usage in data[parking]['usage']:
            t = Timeslot.objects.get(name=usage)
            Usage.objects.create(
                parking=p,
                timeslot=t,
                full=data[parking]['usage'][usage][0],
                weight=data[parking]['usage'][usage][1],
            )


def detect(request, lat, lon):
    detector = Detector()
    result = detector.detect(lat, lon)
    return JsonResponse(result, safe=False)
